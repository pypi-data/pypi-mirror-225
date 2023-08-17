"""Configuration settings."""
import shlex

from pydantic import BaseModel, HttpUrl, constr, validator
from typing import Literal, Optional

from .packs.code_server import Pack as CodeServerPack
from .packs.jupyterlab import Pack as JupyterLabPack
from .packs.mariadb import Pack as MariaDBPack
from .packs.nbclassic import Pack as NBClassicPack
from .packs.tutorial_server import Pack as TutorialServerPack


class Module(BaseModel):
    """Settings for the module configuration."""

    code: constr(min_length=1)
    presentation: constr(min_length=1)


class Image(BaseModel):
    """Settings for the Docker image configuration."""

    base: constr(min_length=1) = "python:3.10-bullseye"
    user: constr(min_length=1) = "ou"


class Server(BaseModel):
    """Settings for the core server configuration."""

    default_path: constr(min_length=1) = "/"
    access_token: str | None = None
    wrapper_host: str | None = None


class Content(BaseModel):
    """Settings for the content configuration."""

    source: constr(min_length=1)
    target: str = ""
    overwrite: Literal["always"] | Literal["never"] | Literal["if-unchanged"]


class AptDebLine(BaseModel):
    """Settings for an APT deb line."""

    url: HttpUrl
    distribution: constr(min_length=1)
    component: constr(min_length=1)


class AptSource(BaseModel):
    """Settings for a single APT source."""

    name: constr(min_length=1)
    key_url: HttpUrl
    dearmor: bool = True
    deb: AptDebLine


class Sources(BaseModel):
    """Settings for the additional sources configuration."""

    apt: list[AptSource] = []


class Packages(BaseModel):
    """Settings for the packages configuration."""

    apt: list[constr(min_length=1)] = []
    pip: list[constr(min_length=1)] = []


class Script(BaseModel):
    """Settings for a single script configuration."""

    commands: list[str] = []

    @validator("commands", pre=True)
    def convert_strings(cls: "Script", value: str | list[str]) -> list[str]:
        """Convert a string commands to a list."""
        if isinstance(value, str):
            return [line for line in value.split("\n") if line.strip()]
        else:
            return value


class Scripts(BaseModel):
    """Settings for the scripts configuration."""

    build: list[Script] = []
    startup: list[Script] = []
    shutdown: list[Script] = []


class LauncherEntry(BaseModel):
    """Settings for a single launcher entry."""

    enabled: bool = True
    icon_path: str = ""
    title: str = ""


class WebApp(BaseModel):
    """Settings for a single web application configuration."""

    path: constr(min_length=1)
    cmdline: Optional[list[constr(min_length=1)]] = None
    command: Optional[list[constr(min_length=1)]] = None
    port: int = 0
    default: bool = False
    timeout: int = 60
    absolute_url: bool = False
    environment: dict = {}
    new_browser_tab: bool = False
    request_headers_override: dict = {}
    launcher_entry: LauncherEntry = LauncherEntry()

    @validator("cmdline", pre=True)
    def convert_string_cmdline(cls: 'WebApp', value: str | list[constr(min_length=1)]) -> list[constr(min_length=1)]:
        """Convert a string cmdline to its list representation."""
        if isinstance(value, str):
            return shlex.split(value)
        else:
            return value

    @validator("command", pre=True)
    def convert_string_command(cls: 'WebApp', value: str | list[constr(min_length=1)]) -> list[constr(min_length=1)]:
        """Convert a string command to its list representation."""
        if isinstance(value, str):
            return shlex.split(value)
        else:
            return value


class EnvironmentVariable(BaseModel):
    """Settings for additional environment variables."""

    name: constr(min_length=1)
    value: str = ""


class Flags(BaseModel):
    """Settings for output flags."""

    ou_container_content: bool = False


class Settings(BaseModel):
    """Application Settings."""

    module: Module
    image: Image = Image()
    server: Server = Server()
    content: list[Content] = []
    sources: Sources = Sources()
    packages: Packages = Packages()
    scripts: Scripts = Script()
    web_apps: list[WebApp] = []
    services: list[constr(min_length=1)] = []
    environment: list[EnvironmentVariable] = []
    packs: list[JupyterLabPack | CodeServerPack | MariaDBPack | NBClassicPack | TutorialServerPack] = []
    hacks: list[Literal["missing-man1"]] = []
    flags: Flags = Flags()
    jupyter_server_config: dict = {}
