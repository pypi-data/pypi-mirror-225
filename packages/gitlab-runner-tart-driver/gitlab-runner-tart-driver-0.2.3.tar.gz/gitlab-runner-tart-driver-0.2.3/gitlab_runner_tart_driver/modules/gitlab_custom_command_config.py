from typing import Optional

from pydantic import BaseSettings
from pydantic import Field


class GitLabCustomCommandConfig(BaseSettings):
    """Config parameters needed throughout the process read from the environment"""

    ci_job_image: Optional[str]
    ci_pipeline_id: Optional[str]
    ci_job_id: Optional[str]
    ci_concurrent_id: Optional[str]
    ci_concurrent_project_id: Optional[str]
    ci_runner_short_token: Optional[str]
    ci_project_name: Optional[str]
    ci_registry: Optional[str]
    ci_registry_user: Optional[str]
    ci_registry_password: Optional[str]

    tart_registry_username: Optional[str]
    tart_registry_password: Optional[str]
    tart_registry: Optional[str]

    tart_ssh_username: Optional[str] = Field(default="admin")
    tart_ssh_password: Optional[str] = Field(default="admin")
    tart_max_vm_count: Optional[int] = Field(default=2)
    tart_pull_policy: Optional[str] = Field(default="if-not-present")
    tart_executor_softnet_enabled: Optional[str] = Field(default="false")
    tart_executor_headless: Optional[str] = Field(default="true")
    tart_executor_vnc_enabled: Optional[str] = Field(default="false")
    tart_executor_install_gitlab_runner: Optional[str] = Field(default="false")
    tart_executor_shell: Optional[str] = Field(default="/bin/zsh")
    tart_executor_timeout: Optional[int] = Field(default=60)
    tart_executor_display: Optional[str] = Field(default="1920x1200")

    class Config:
        """Define the prefix used by GitLab for all environment variables passed to a custom driver.
        see https://docs.gitlab.com/runner/executors/custom.html#stages
        """

        env_prefix = "CUSTOM_ENV_"

    def vm_name(self):
        """Creates a unique name for a VM"""
        return f"{self.vm_name_prefix}-{self.ci_project_name}-{self.ci_pipeline_id}-{self.ci_job_id}-{self.ci_concurrent_id}"

    @property
    def vm_name_prefix(self):
        return "grtd"

    @property
    def softnet_enabled(self) -> bool:
        return self.tart_executor_softnet_enabled.lower() == "true"

    @property
    def vnc_enabled(self) -> bool:
        return self.tart_executor_vnc_enabled.lower() == "true"

    @property
    def headless(self) -> bool:
        return self.tart_executor_headless.lower() == "true"

    @property
    def shell(self) -> Optional[str]:
        return self.tart_executor_shell

    @property
    def display(self) -> Optional[str]:
        return self.tart_executor_display

    @property
    def install_gitlab_runner(self) -> bool:
        return self.tart_executor_install_gitlab_runner.lower() == "true"

    @property
    def timeout(self) -> Optional[int]:
        return self.tart_executor_timeout

    @property
    def ssh_username(self) -> Optional[str]:
        return self.tart_ssh_username

    @property
    def ssh_password(self) -> Optional[str]:
        return self.tart_ssh_password

    @property
    def pull_policy(self) -> Optional[str]:
        return self.tart_pull_policy

    @property
    def registry_username(self) -> Optional[str]:
        return self.tart_registry_username

    @property
    def registry_password(self) -> Optional[str]:
        return self.tart_registry_password

    @property
    def registry(self) -> Optional[str]:
        return self.tart_registry
