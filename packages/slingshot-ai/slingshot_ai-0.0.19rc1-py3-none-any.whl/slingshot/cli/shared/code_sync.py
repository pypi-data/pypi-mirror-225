from __future__ import annotations

import asyncio
import contextlib
import platform
import shutil
import sys
from logging import getLogger
from pathlib import Path
from time import sleep
from typing import Any, Iterator
from urllib.parse import urlparse

import sh  # type: ignore
import typer

from slingshot import schemas
from slingshot.cli.auth import set_ssh_public_key_if_not_set
from slingshot.cli.config.slingshot_cli import SlingshotCLIApp
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.graphql import fragments
from slingshot.sdk.slingshot_sdk import SlingshotSDK
from slingshot.sdk.utils import console

app = SlingshotCLIApp()
logger = getLogger(__name__)

ERROR_SSH_KEY_MISSING = (
    "[red]You must add an SSH key to your account before using code sync[/red]"
    "Run [bold green]slingshot auth set-ssh[/bold green] to add an SSH key"
)


async def start_code_sync_ssh(sync_path: Path, app_spec: fragments.AppSpec, *, sdk: SlingshotSDK) -> None:
    console.print(f"Starting code sync for session '{app_spec.app_spec_name}'")

    if app_spec.app_instance_status != schemas.AppInstanceStatus.READY:
        raise SlingshotException(
            f"Can't code sync while session is not ready. Current status: {app_spec.app_instance_status}"
        )

    if not (app_instance_url := app_spec.app_instance_url):
        raise SlingshotException("App instance URL not found")

    assert app_spec.app_instances, "App instances should be available"
    app_instance = app_spec.app_instances[0]
    ssh_port = app_instance.ssh_port
    if not ssh_port:
        console.log("Allocating port for code sync...")
        resp = await sdk.start_app_code_sync(app_spec.app_spec_id)
        if resp.error:
            raise SlingshotException(resp.error.message)
        ssh_port = resp.data and resp.data.ssh_port

    if not ssh_port:
        raise SlingshotException("Failed to allocate port for code sync")
    await _start_unison(app_instance_url, ssh_port, sync_path, verbose=sdk.verbose)


async def check_ssh_key_exists(sdk: SlingshotSDK) -> None:
    """Check that the user has an SSH key set. If not, prompt to set one."""
    await set_ssh_public_key_if_not_set(sdk)
    me = await sdk.me()
    if not (me and me.user):
        raise SlingshotException("Only users can sync code")
    if not me.user.ssh_public_key:
        raise SlingshotException(ERROR_SSH_KEY_MISSING)


async def _start_unison(session_url: str, ssh_port: int, sync_path: Path | None, verbose: bool = False) -> None:
    if sync_path is None:
        sync_path = Path.cwd()
    if not _is_unison_installed():
        _print_unison_install_instructions()
        raise typer.Exit(1)

    hostname = urlparse(session_url).hostname
    # TODO: poll until sshd is available. For now, we can assume it takes <1s.
    sleep(1)
    logger.debug(f"ssh://slingshot@{hostname}:{ssh_port}//slingshot/session")

    p = "working directory" if sync_path.cwd().absolute() == sync_path.absolute() else sync_path
    for _ in range(3):  # retry 3 times
        console.print(f"[blue]Syncing {p} to your session...[/blue]")
        try:
            # run unison command in a subprocess
            # assumes ssh key is already added to the server authorized_keys
            with _open_log_file(verbose) as (stdout, stderr):
                # TODO: support explicit selection of the SSH key
                #  unison /local/path ssh://remote/path -sshcmd 'ssh -i /path/to/your_specific_key'
                sh.unison(
                    str(sync_path),
                    f"ssh://slingshot@{hostname}:{ssh_port}//slingshot/session",  # sync to /slingshot/session
                    batch=True,  # batch mode: ask no questions at all
                    repeat="watch",  # synchronize repeatedly (using unison-fsmonitor process to detect changes)
                    prefer="newer",  # choose newer version for conflicting changes
                    copyonconflict=True,  # keep copies of conflicting files
                    sshargs="-o StrictHostKeyChecking=no",  # skip known_hosts check
                    _long_prefix="-",
                    _err=stderr,
                    _out=stdout,
                )
        except sh.ErrorReturnCode:
            # TODO consider parsing the unison.log to e.g. automatically identify if it's a `Permission denied
            #  (publickey)` error
            console.print("[yellow]An error occurred while syncing your code. Retrying...[/yellow]")
            console.print(
                "[yellow]Please make sure the SSH key used for code sync has been added to the SSH agent[/yellow]"
            )
            await asyncio.sleep(1)  # wait for a second before retrying
    raise SlingshotException(f"Error running unison, please check {Path.home()}/.slingshot/unison.log for more details")


def _is_unison_installed() -> bool:
    _unison = shutil.which("unison") is not None
    if not _unison:
        console.print("[red]Unison is not installed[/red]")
    _fsmonitor = shutil.which("unison-fsmonitor") is not None
    if not _fsmonitor:
        console.print("[red]Unison-fsmonitor is not installed[/red]")
    return _unison and _fsmonitor


def _print_unison_install_instructions() -> None:
    uname = platform.uname()

    console.print("[yellow] We use unison and unison-fsmonitor for code sync, please install [/yellow]")
    if uname.system == "Darwin":
        console.print("[yellow] Using homebrew:[/yellow]")
        console.print("[yellow]  brew install unison[/yellow]")
        console.print("[yellow]  brew install eugenmayer/dockersync/unox[/yellow]")
    elif uname.system == "Linux":
        console.print("[yellow] Manually from official releases:[/yellow]")
        console.print(
            "[yellow]  sudo wget -qO- "
            "https://github.com/bcpierce00/unison/releases/download/v2.53.0/"
            "unison-v2.53.0+ocaml-4.13.1+x86_64.linux.tar.gz"
            " | tar -zxvf - -C /usr bin/[/yellow]"
        )
    console.print("[yellow] For more information see:[/yellow]")
    console.print("[yellow]  https://github.com/bcpierce00/unison/wiki/Downloading-Unison [/yellow]")


@contextlib.contextmanager
def _open_log_file(verbose: bool) -> Iterator[tuple[Any, Any]]:  # stdout, stderr
    log_file = client_settings.global_config_folder / "unison.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    # If verbose, print to stdout/stderr, otherwise write to log file
    if verbose:
        yield sys.stdout, sys.stderr
    else:
        with open(log_file, "w") as f:
            yield f, f
