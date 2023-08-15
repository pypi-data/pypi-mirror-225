# mypy: disable-error-code="import"
"""Defines a launcher training models on AWS SageMaker.

This model is similar to the Slurm launcher. We first package up all the
Python code for running the model, then use the SageMaker Python SDK to
launch a training job on AWS.

The SageMaker PyTorch estimator uses an Amazon-built Docker container to execute
functions defined in a given entry point, which is just a Python script.

It's useful to set some environment variables, to avoid manually specifying
them in your config:

- ``SAGEMAKER_DEFAULT_INSTANCE``: The default instance type (e.g., ``ml.p3.2xlarge``).
- ``SAGEMAKER_DEFAULT_ROLE``: The default IAM role.
- ``SAGEMAKER_DEFAULT_BUCKET``: The default S3 bucket to use for output.
"""

import datetime
import functools
import logging
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import torch
from omegaconf import II, MISSING, DictConfig, OmegaConf
from packaging import version

from ml.core.config import conf_field
from ml.core.env import get_stage_dir, set_data_dir, set_ml_config_path, set_model_dir
from ml.core.registry import Objects, project_dirs, register_launcher, register_trainer
from ml.launchers.base import BaseLauncher, BaseLauncherConfig
from ml.scripts.train import train_main
from ml.utils.staging import stage_environment
from ml.utils.torch_distributed import MultiprocessConfig, launch_subprocesses

logger = logging.getLogger(__name__)

LAUNCH_METHOD = "forkserver"

# If the PyTorch version being used is greater than this version, then this
# version is used instead.
MAX_FRAMEWORK_VERSION = "2.0.0"

DEFAULT_PY_VERSION = "py310"


@dataclass
class SagemakerLauncherConfig(BaseLauncherConfig):
    iam_role: str = conf_field(MISSING, help="The SageMaker role to use")
    instance_count: int = conf_field(1, help="The number of instances to use")
    instance_type: str = conf_field(MISSING, help="The training instance type")
    output_bucket: str = conf_field(MISSING, help="The S3 bucket for outputs")
    output_prefix: str = conf_field(II("ml.exp_name:job"), help="The S3 prefix to use for output")
    max_framework_version: str = conf_field(MAX_FRAMEWORK_VERSION, help="The maximum PyTorch version to use")
    py_version: str = conf_field(DEFAULT_PY_VERSION, help="The Python version to use")
    use_spot_instances: bool = conf_field(
        II("oc.decode:${oc.env:SAGEMAKER_DEFAULT_SPOT_INSTANCES,0}"),
        help="Whether or not to use spot instances",
    )
    max_num_seconds: int = conf_field(24 * 60 * 60, help="The maximum number of seconds to run")
    additional_requirements: list[str] = conf_field([], help="Additional requirements to install")
    sync_fit: bool = conf_field(False, help="If set, block on fitting")


def set_if_missing(c: Any, ck: str, key: str) -> None:  # noqa: ANN401
    if OmegaConf.is_missing(c, ck):
        if key in os.environ:
            setattr(c, ck, os.environ[key])
        else:
            raise KeyError(f"Missing `{ck}` or '{key}' environment variable.")


@register_launcher("sagemaker", SagemakerLauncherConfig)
class SagemakerLauncher(BaseLauncher[SagemakerLauncherConfig]):
    def launch(self) -> None:
        try:
            import sagemaker
            import sagemaker.debugger.debugger
            import sagemaker.pytorch.estimator
        except ModuleNotFoundError:
            raise ModuleNotFoundError("`sagemaker` package not installed; install it with `pip install sagemaker`")

        set_if_missing(self.config, "iam_role", "SAGEMAKER_DEFAULT_ROLE")
        set_if_missing(self.config, "instance_type", "SAGEMAKER_DEFAULT_INSTANCE")
        set_if_missing(self.config, "output_bucket", "SAGEMAKER_DEFAULT_BUCKET")

        # Stages all files to a new directory.
        staged_env = stage_environment(project_dirs.paths[1:], get_stage_dir())

        # Set up the SageMaker session and role
        sagemaker_session = sagemaker.Session()

        # Parses PyTorch version.
        framework_version = version.parse(torch.__version__)
        max_version = version.parse(self.config.max_framework_version)
        if framework_version > max_version:
            framework_version = max_version

        # Saves the config file to the staging directory.
        config_path = staged_env / "config.yaml"
        OmegaConf.save(self.raw_config, config_path)

        cur_time = datetime.datetime.now()
        day_str = cur_time.strftime("%Y-%m-%d")

        # Base S3 bucket prefix.
        s3_prefix = f"s3://{self.config.output_bucket}/{self.config.output_prefix}/{day_str}"

        # Writes all Python dependenices to a requirements.txt file.
        all_requirements: set[str] = set()
        for project_dir in project_dirs.paths:
            if (requirements_file := project_dir / "requirements.txt").is_file():
                with open(requirements_file, "r", encoding="utf-8") as f:
                    all_requirements.update(f.read().splitlines())
        all_requirements.update(self.config.additional_requirements)
        all_requirements = {requirement for requirement in all_requirements}

        # Writes the requirements.txt file.
        dependencies = []
        if all_requirements:
            dependencies.append("requirements.txt")
            with open(staged_env / "requirements.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(list(sorted(all_requirements))))

        # Builds the tensorboard logging directory.
        trainer_cfg = register_trainer.build_config(self.raw_config)
        tensorboard_output_config: sagemaker.debugger.debugger.TensorBoardOutputConfig | None
        if trainer_cfg is None:
            tensorboard_output_config = None
        else:
            tensorboard_output_config = sagemaker.debugger.debugger.TensorBoardOutputConfig(
                s3_output_path=f"{s3_prefix}/{trainer_cfg.log_dir_name}/tensorboard",
                # container_local_output_path=f"{trainer_cfg.log_dir_name}/tensorboard",
            )

        # Cleans up the job name to satisfy constraints.
        job_name = self.config.output_prefix
        cleaned_job_name = re.sub(r"[^a-zA-Z0-9-]+", "-", job_name)

        # Change to the staging directory.
        original_dir = os.getcwd()
        os.chdir(staged_env)

        estimator = sagemaker.pytorch.estimator.PyTorch(
            entry_point="ml/launchers/sagemaker.py",
            framework_version=framework_version.base_version,
            py_version=self.config.py_version,
            source_dir=str(staged_env),
            role=self.config.iam_role,
            instance_count=self.config.instance_count,
            instance_type=self.config.instance_type,
            sagemaker_session=sagemaker_session,
            use_spot_instances=self.config.use_spot_instances,
            max_run=self.config.max_num_seconds,
            base_job_name=cleaned_job_name,
            output_path=s3_prefix,
            code_location=s3_prefix,
            dependencies=dependencies,
            distribution={
                "smdistributed": {
                    "dataparallel": {
                        "enabled": self.config.instance_count > 1,
                    },
                },
                "mpi": {
                    "enabled": True,
                },
            },
            tensorboard_output_config=tensorboard_output_config,
        )

        estimator.fit(wait=self.config.sync_fit)

        os.chdir(original_dir)


def sagemaker_train_proc_main(config_path: Path) -> None:
    config = cast(DictConfig, OmegaConf.load(config_path))
    if not OmegaConf.is_dict(config):
        raise ValueError(f"Expected a dict config, got: {config}")

    assert (trainer := register_trainer.build_entry(config)) is not None
    trainer.add_lock_file("running", exists_ok=True)
    trainer.remove_lock_file("scheduled", missing_ok=True)

    objs = Objects(config, trainer=trainer)
    train_main(config, objs)


def sagemaker_main() -> None:
    # Adds any directories to `project_dirs`.
    for subdir in Path.cwd().iterdir():
        if subdir.is_dir():
            project_dirs.add(subdir)

    # Parses the hosts from the environment.
    hosts_str = os.environ["SM_HOSTS"]
    hosts = list(sorted(re.findall(r'"(.*?)"', hosts_str)))
    cur_host = os.environ["SM_CURRENT_HOST"]
    assert len(hosts) > 0, f"Unexpected value for `SM_HOSTS`: {hosts_str}"
    assert cur_host in hosts, f"Unexpected value for `SM_CURRENT_HOST`: {cur_host}"
    master_addr = hosts[0]
    cur_host_idx = hosts.index(cur_host)

    num_gpus = int(os.environ["SM_NUM_GPUS"])
    world_size = max(len(hosts) * num_gpus, 1)

    # Determines a master port by hashing the hosts.
    master_port = 10_000 + hash(tuple(hosts)) % 10_000

    # Sets environment variables from SageMaker environment variables.
    sm_model_dir = Path(os.environ["SM_MODEL_DIR"])
    sm_input_dir = Path(os.environ["SM_INPUT_DIR"])
    set_model_dir(sm_model_dir / "models")
    set_data_dir(sm_input_dir)

    # Moves the "config.yaml" file to the `sm_model_dir`.
    shutil.move("config.yaml", (config_path := sm_model_dir / "config.yaml"))
    set_ml_config_path(config_path)

    cfg = MultiprocessConfig(
        world_size=world_size,
        local_world_size=num_gpus,
        master_addr=master_addr,
        master_port=master_port,
    )

    func = functools.partial(sagemaker_train_proc_main, config_path=config_path)
    launch_subprocesses(func, cfg, rank_offset=cur_host_idx * num_gpus)


if __name__ == "__main__":
    sagemaker_main()
