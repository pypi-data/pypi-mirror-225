import pathlib
from typing import Optional

from pydantic import BaseModel


class GitLabCustomDriver(BaseModel):
    name: str
    version: str


class GitLabCustomDriverConfig(BaseModel):
    builds_dir: Optional[pathlib.Path]
    cache_dir: Optional[pathlib.Path]
    builds_dir_is_shared: Optional[bool]
    hostname: Optional[str]
    driver: Optional[GitLabCustomDriver]
    job_env: Optional[dict]
