import os
import shlex
import subprocess
from numbers import Number
from typing import Dict

import git
import prefect
from prefect.executors import DaskExecutor
from prefect.run_configs import KubernetesRun
from prefect.storage import Docker
from prefect.utilities.graphql import with_args

from .logger import logger


class DockerBaseImage:
    """Helper class for building and pushing base docker image for use with prefect"""

    def __init__(
        self,
        az_registry_url,
        project_base_path,
        base_docker_image,
        skip_login=False,
    ):
        self.az_registry_url = az_registry_url
        self.project_base_path = project_base_path
        self.base_docker_image = base_docker_image
        self.skip_login = skip_login

    def build_and_push(self):
        if not self.skip_login:
            self.login()
        self.pull()
        self.build()
        self.push()

    def login(self):
        az_docker_registry_name = self.az_registry_url.split(".")[0]
        logger.info(
            f"Logging into Azure (running `az acr login --name {az_docker_registry_name}`)"
        )
        subprocess.run(
            f"az acr login --name {az_docker_registry_name}".split(), check=True
        )

    def pull(self):
        logger.info("Pulling existing base image")
        try:
            subprocess.run(
                [
                    "docker",
                    "pull",
                    self.base_docker_image,
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            # We're pulling it only because if there is a recent build, the old layers
            # can be re-used. So, it is not critical if this failed.
            logger.warn("Failed to pull existing base image. Continuing anyway...")

    def build(self):
        logger.info("Building base image")

        run_cmd = [
            "docker",
            "buildx",
            "build",
            "--platform",
            "linux/amd64",
            "--pull",
            "-t",
            self.base_docker_image,
            "-f",
            os.path.join(self.project_base_path, "Dockerfile"),
            self.project_base_path,
        ]

        run_cmd = " ".join([shlex.quote(run_arg) for run_arg in run_cmd])

        subprocess.check_output(
            run_cmd,
            shell=True,
        )

    def push(self):
        logger.info("Uploading base image")
        subprocess.run(
            [
                "docker",
                "push",
                self.base_docker_image,
            ],
            check=True,
        )


def create_docker_storage(
    project_base_path: str,
    az_docker_registry_url: str,
    az_docker_image_base_name: str,
    env_vars: Dict,
    skip_login: bool = False,
) -> prefect.storage.Docker:
    """
    Build docker image to be used as a base for deploying prefect flow. Only supports
    Azure Container Service.

    Args:
        project_base_path (str):
            Docker build direction; the Dockerfile is expected in this path.
        az_docker_registry_url (str):
            Azure registry url to be used for the docker image.
        az_docker_image_base_name (str):
            Image name to be used as the base image.
        env_vars (typing.Dict):
            Dictionary of environment variables to be embedded in the docker image.
        skip_login (bool):
            Skip logging in to docker (assumes that it is already logged in by other
            means).

    Returns:
        prefect.storage.Docker:
            prefect Docker storage object to be used with prefect flow.
    """

    base_docker_image = f"{az_docker_registry_url}/{az_docker_image_base_name}"
    DockerBaseImage(
        az_docker_registry_url,
        project_base_path,
        base_docker_image,
        skip_login,
    ).build_and_push()

    git_info = _get_git_info()
    env_vars = {**env_vars, **git_info}

    return Docker(
        registry_url=az_docker_registry_url,
        env_vars=env_vars,
        base_image=base_docker_image,
    )


def deploy_flow(
    flow: prefect.Flow,
    schedule: prefect.schedules.Schedule,
    docker_storage: prefect.storage.Docker,
    prefect_project_name: str,
    mem_limit_gb: Number = None,
) -> None:
    """Deploy the Prefect flow

    Build and deploy a given prefect flow.

    Args:
        flow (prefect.Flow):
            prefect flow to deploy
        schedule (prefect.schedules.Schedule):
            schedule to run the deployed flow
        docker_storage (prefect.storage.Docker):
            docker storage to store the flow to
        prefect_project_name (typing.Dict):
            prefect project name to deploy the flow to
        mem_limit_gb (Number, optional):
            override the default memory limit for docker image in the dask cluster
    """

    flow.storage = docker_storage

    if schedule:
        flow.schedule = schedule

    flow.run_config = KubernetesRun()

    if mem_limit_gb:
        flow.executor = DaskExecutor(
            cluster_kwargs=dict(memory_limit="%sGi" % mem_limit_gb), debug=True
        )
    else:
        flow.executor = DaskExecutor(debug=True)

    create_project_if_not_exist(prefect_project_name)

    flow.register(project_name=prefect_project_name)


def create_project_if_not_exist(project_name, prefect_client=None):
    """Create prefect project if it doesn't already exist

    project_name is mandatory in prefect version 0.13.0 and higher when registering a
    flow. So, it needs to be created.
    """

    if prefect_client is None:
        prefect_client = prefect.client.Client()

    query_project = {
        "query": {
            with_args("project", {"where": {"name": {"_eq": project_name}}}): {
                "id": True
            }
        }
    }

    project = prefect_client.graphql(query_project).data.project
    if not project:
        prefect_client.create_project(project_name)


def _get_git_info():
    """Return the Git information"""
    repo = git.Repo(search_parent_directories=True)

    try:
        branch = str(repo.active_branch)
    except TypeError:
        branch = ""

    tags = [
        str(tag)
        for tag in repo.tags
        if tag is not None and tag.commit == repo.head.commit
    ]

    return {
        "GIT_COMMIT_ID": repo.head.commit.hexsha,
        "GIT_IS_DIRTY": str(repo.is_dirty()),
        "GIT_BRANCH": branch,
        "GIT_TAGS": ", ".join(tags),
    }
