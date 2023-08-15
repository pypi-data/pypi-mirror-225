from __future__ import annotations

from typing import Optional

import typer
from rich.table import Table

from .. import schemas
from ..sdk.errors import SlingshotException
from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .add import _create_session
from .config.slingshot_cli import SlingshotCLIApp
from .shared import (
    app_spec_id_by_name_or_prompt,
    filter_for_apps,
    filter_for_running_apps,
    filter_for_sessions,
    follow_app_logs_until_ready,
    prompt_for_app_spec,
    prompt_push_code,
)

app = SlingshotCLIApp()


@app.command("start", requires_project=True)
async def start_app(
    *,
    sdk: SlingshotSDK,
    name: Optional[str] = typer.Argument(None, help="App name"),
    sessions: bool = typer.Option(False, "--sessions", "-s", help="Only show sessions"),
) -> str:
    """Start a Slingshot app"""
    applied = await sdk.apply_project()
    source_code_id = await prompt_push_code(sdk)

    if not name:
        filter_fn = filter_for_sessions if sessions else filter_for_apps
        id_and_name_or_none = await prompt_for_app_spec(
            sdk, filter_fn, app_display_name='session' if sessions else 'app', raise_if_missing=False
        )
        if id_and_name_or_none:
            _, name = id_and_name_or_none
        elif sessions:
            console.print("Creating a new session")
            name = _create_session()
            await sdk.apply_project(force=applied)  # If applied, the user was already prompted. Just quietly apply.

            # If the user doesn't apply the prompt with the session, exit because there will not be a session to start.
            all_app_specs = await sdk.list_apps()
            session_specs = [
                app_spec for app_spec in all_app_specs if app_spec.app_sub_type == schemas.AppSubType.SESSION
            ]
            if not session_specs:
                raise SlingshotException("Session not created, exiting")
        else:
            raise typer.Exit(1)

    assert sdk.project
    app_spec = await sdk.api.get_app_spec_by_name(name, sdk.project.project_id)
    if not app_spec:
        raise SlingshotException(f"No run found with the name '{name}'")

    app_instance = await sdk.start_app(app_name=name, source_code_id=source_code_id)
    url = await sdk.web_path_util.app(app_spec=app_instance.app_spec_id)
    console.print(f"Starting app '{name}'. See details here: {url}")

    console.print(f"Following logs. Ctrl-C to stop, and run 'slingshot logs {name} --follow' to follow again")
    status = await follow_app_logs_until_ready(sdk, app_instance.app_spec_id)
    if status == schemas.AppInstanceStatus.ERROR:
        raise SlingshotException(f"App failed to start. Try again or contact support for help.")

    if status == schemas.AppInstanceStatus.READY:
        refreshed_app_spec = await sdk.get_app(name)
        assert refreshed_app_spec is not None, "App does not exist anymore"

        console.print(f"[green]App '{name}' started successfully[/green].")
        if refreshed_app_spec.app_instance_url:
            console.print(f"App will be available at {refreshed_app_spec.app_instance_url}")
            console.print(f"Open the URL with [blue]slingshot app open {name}[/blue]")
        return name

    console.print(f"App stopped with status {status}")
    return name


@app.command("stop", requires_project=True)
async def stop_app(*, sdk: SlingshotSDK, name: Optional[str] = typer.Argument(None, help="App name")) -> None:
    """Stop a Slingshot app"""
    if not name:
        _, name = await prompt_for_app_spec(sdk, filter_for_apps, filter_for_running_apps, app_display_name="app")
    await sdk.stop_app(app_name=name)
    console.print(f"[green]App '{name}' stopped successfully[/green].")


@app.command(name="logs", requires_project=True)
async def app_logs(
    name: Optional[str] = typer.Argument(None, help="App name"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow logs"),
    refresh_rate: float = typer.Option(3.0, "--refresh-rate", "-r", help="Refresh rate in seconds"),
    *,
    sdk: SlingshotSDK,
) -> None:
    """Get logs for a Slingshot app."""
    app_spec_id = await app_spec_id_by_name_or_prompt(sdk, name)
    await sdk.print_logs(app_spec_id=app_spec_id, follow=follow, refresh_rate_s=refresh_rate)


@app.command("open", requires_project=True)
async def open_app(*, sdk: SlingshotSDK, name: Optional[str] = typer.Argument(None, help="App name")) -> None:
    """Open a Slingshot app in your browser"""
    app_spec_id = await app_spec_id_by_name_or_prompt(sdk, name)
    app_instance = await sdk.api.get_latest_app_instance_for_app_spec(app_spec_id=app_spec_id)
    if app_instance is None or not app_instance.app_instance_url:
        console.print(f"[red]No URL found for app[/red]")
        return

    console.print(f"[green]Opening {app_instance.app_instance_url}[/green]")
    typer.launch(app_instance.app_instance_url)


@app.command("list", requires_project=True)
async def list_apps(*, sdk: SlingshotSDK) -> None:
    """List all Slingshot apps as a table"""
    app_specs = await sdk.list_apps()
    app_specs = [spec for spec in app_specs if spec.app_type == schemas.AppType.CUSTOM]
    if not app_specs:
        console.print(
            "No apps found! Edit [yellow]slingshot.yaml[/yellow] or use [yellow]slingshot add[/yellow] to add one."
        )
        return

    table = Table(title="Apps")
    table.add_column("App Name", style="cyan")
    table.add_column("Status", style="cyan")
    table.add_column("Environment", style="cyan")
    table.add_column("URL", style="cyan")
    for app_spec in app_specs:
        env_spec = app_spec.execution_environment_spec
        env_name = env_spec.execution_environment_spec_name if env_spec else '-'
        row = [app_spec.app_spec_name, app_spec.app_instance_status, env_name, app_spec.app_instance_url]
        table.add_row(*row)
    console.print(table)
