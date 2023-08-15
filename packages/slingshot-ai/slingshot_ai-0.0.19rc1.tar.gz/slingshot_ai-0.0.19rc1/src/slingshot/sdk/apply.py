from __future__ import annotations

import json
from logging import getLogger
from typing import TYPE_CHECKING, Optional

import sentry_sdk

from slingshot import schemas
from slingshot.cli.shared import create_empty_project_manifest, prompt_confirm, prompt_for_single_choice
from slingshot.schemas import ProjectManifest
from slingshot.sdk import config
from slingshot.sdk.apply_diff import (
    apply_diff_to_local_manifest,
    compute_project_manifest_diff,
    detect_local_remote_diff_conflicts,
    diff_to_str,
)
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException, SlingshotFileNotFoundException
from slingshot.sdk.graphql import fragments
from slingshot.sdk.utils import console, edit_slingshot_yaml
from slingshot.sdk.wrapped_diff import DiffItem
from slingshot.shared.config import load_slingshot_project_config
from slingshot.shared.utils import (
    get_data_or_raise,
    machine_size_to_machine_type_gpu_count,
    machine_type_gpu_count_to_machine_size,
)

if TYPE_CHECKING:
    from slingshot.sdk.slingshot_sdk import SlingshotSDK

    EnvSpecPlan = tuple[
        list[tuple[schemas.EnvironmentSpec, str]],
        list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]],
        list[fragments.ExecutionEnvironmentSpec],
    ]
    AppSpecPlan = tuple[
        list[schemas.SlingshotAbstractAppSpec],
        list[tuple[schemas.SlingshotAbstractAppSpec, str]],
        list[fragments.AppSpec],
    ]
else:
    EnvSpecPlan = tuple
    AppSpecPlan = tuple

logger = getLogger(__name__)


def _convert_using_to_app_subtype(using: str) -> schemas.AppSubType:
    using = using.upper()
    using = using.replace("-", "_")
    return schemas.AppSubType(using)


class ApplyService:
    WAIT_FOR_ENV_POLL_INTERVAL = 2

    def __init__(self, sdk: "SlingshotSDK") -> None:
        if not (project := sdk.project):
            raise SlingshotException(
                "SDK has no project set.", cli="No project set. Please run 'slingshot init' or 'slingshot use'."
            )
        self._project = project
        self._sdk = sdk

    async def plan(self, config_: schemas.ProjectManifest | None = None) -> tuple[EnvSpecPlan, AppSpecPlan]:
        if not config_:
            config_ = load_slingshot_project_config()
        env_plan, _ = await self.plan_environments(config_)
        app_plan = await self.plan_apps(config_)
        return env_plan, app_plan

    async def plan_apps(self, config_: schemas.ProjectManifest) -> AppSpecPlan:
        existing_app_specs = await self._sdk.list_apps()
        components_mapping: dict[schemas.AppType, list[schemas.SlingshotAbstractAppSpec]] = {
            schemas.AppType.RUN: config_.runs,
            schemas.AppType.DEPLOYMENT: config_.deployments,
        }

        app_specs_to_create = []
        app_specs_to_update = []
        app_specs_to_delete = []
        all_change_msgs = []

        # Check App Sub Types
        for app_sub_type in schemas.AppSubType:
            apps_from_sub_type = [
                app
                for app in config_.apps
                if isinstance(app, schemas.SlingshotAbstractAppSpec)
                and _convert_using_to_app_subtype(app.using) == app_sub_type
            ]
            (
                app_sub_type_specs_to_create,
                app_sub_type_app_specs_to_update,
                app_sub_type_app_specs_to_delete,
                app_sub_type_app_change_msgs,
            ) = _diff_existing_app_yaml_specs(
                existing_app_specs, apps_from_sub_type, schemas.AppType.CUSTOM, app_sub_type  # noqa
            )
            app_specs_to_create += app_sub_type_specs_to_create
            app_specs_to_update += app_sub_type_app_specs_to_update
            app_specs_to_delete += app_sub_type_app_specs_to_delete
            all_change_msgs += app_sub_type_app_change_msgs

        # Check Runs, Apps, Deployments
        for component_type, components in components_mapping.items():
            (
                component_specs_to_create,
                component_app_specs_to_update,
                component_app_specs_to_delete,
                component_app_change_msgs,
            ) = _diff_existing_app_yaml_specs(existing_app_specs, components, component_type)
            app_specs_to_create += component_specs_to_create
            app_specs_to_update += component_app_specs_to_update
            app_specs_to_delete += component_app_specs_to_delete
            all_change_msgs += component_app_change_msgs

        if all_change_msgs:
            console.print("\n".join(all_change_msgs))

        return app_specs_to_create, app_specs_to_update, app_specs_to_delete

    async def plan_environments(self, config_: schemas.ProjectManifest) -> tuple[EnvSpecPlan, set[str]]:
        existing_env_specs = await self._sdk.list_environments()
        (
            env_specs_to_create,
            env_specs_to_update,
            env_specs_to_delete,
            updated_spec_names,
            change_msgs,
        ) = _diff_existing_env_yaml_specs(existing_env_specs, config_.environments)
        if change_msgs:
            console.print("\n".join(change_msgs))
        return (env_specs_to_create, env_specs_to_update, env_specs_to_delete), updated_spec_names

    async def apply_env_specs(self, env_spec_plan: EnvSpecPlan) -> dict[str, str]:
        """
        Returns a dict mapping env spec names to env spec ids
        """
        env_specs_to_create, env_specs_to_update, env_specs_to_delete = env_spec_plan
        existing_specs = await self._sdk.list_environments()
        env_spec_name_to_id = {
            spec.execution_environment_spec_name: spec.execution_environment_spec_id for spec in existing_specs
        }

        has_env_updates = (len(env_specs_to_create) + len(env_specs_to_update) + len(env_specs_to_delete)) > 0
        if not has_env_updates:
            console.print("No changes detected to environments ✅ ")
            return env_spec_name_to_id

        for spec, spec_name in env_specs_to_create:
            try:
                new_env_spec = await self.create_env_spec(environment_name=spec_name, environment_spec=spec)
                env_spec_name_to_id[spec_name] = new_env_spec.execution_environment_spec_id
            except Exception as e:
                raise SlingshotException(f"Failed to create environment: {e}") from e

        for spec, existing_spec in env_specs_to_update:
            try:
                updated_env_spec = await self.update_env_spec(
                    environment_spec=spec, existing_execution_environment_spec=existing_spec
                )
                spec_id = updated_env_spec.execution_environment_spec_id
                env_spec_name_to_id[existing_spec.execution_environment_spec_name] = spec_id
            except Exception as e:
                raise SlingshotException(f"Failed to update environment: {e}") from e
        for spec in env_specs_to_delete:
            try:
                await self.delete_env_spec(spec)
            except Exception as e:
                raise SlingshotException(f"Failed to delete environment: {e}") from e
        return env_spec_name_to_id

    async def create_env_spec(
        self, environment_name: str, environment_spec: schemas.EnvironmentSpec
    ) -> fragments.ExecutionEnvironmentSpec:
        console.print(f"Creating environment '{environment_name}'...", end="")
        requested_python_requirements = [
            schemas.RequestedRequirement.from_str(i) for i in environment_spec.python_packages
        ]
        requested_apt_requirements = [schemas.RequestedAptPackage(name=p) for p in environment_spec.apt_packages]
        create_env_spec_resp = await self._sdk.create_environment(
            name=environment_name,
            requested_python_requirements=requested_python_requirements,
            requested_apt_requirements=requested_apt_requirements,
            post_install_command=environment_spec.post_install_command,
        )
        if create_env_spec_resp.error:
            raise SlingshotException(f"Failed to create environment: {create_env_spec_resp.error}")
        console.print("✅ ")

        create_env_spec = get_data_or_raise(create_env_spec_resp)
        if create_env_spec.is_new:
            logger.debug(f"Environment '{environment_name}' has changed or is new - we're building it now...")

        env_spec = await self._sdk.get_environment(create_env_spec.execution_environment_spec_id)
        assert env_spec, "Environment was not created"
        return env_spec

    async def update_env_spec(
        self,
        environment_spec: schemas.EnvironmentSpec,
        existing_execution_environment_spec: fragments.ExecutionEnvironmentSpec,
    ) -> fragments.ExecutionEnvironmentSpec:
        environment_name = existing_execution_environment_spec.execution_environment_spec_name
        execution_environment_spec_id = existing_execution_environment_spec.execution_environment_spec_id
        console.print(f"Updating environment '{environment_name}'...", end="")
        requested_python_requirements = [
            schemas.RequestedRequirement.from_str(i) for i in environment_spec.python_packages
        ]
        requested_apt_requirements = [schemas.RequestedAptPackage(name=p) for p in environment_spec.apt_packages]
        await self._sdk.update_environment(
            name=environment_name,
            requested_python_requirements=requested_python_requirements,
            requested_apt_requirements=requested_apt_requirements,
            post_install_command=environment_spec.post_install_command,
        )
        console.print("✅ ")
        env_spec = await self._sdk.get_environment(execution_environment_spec_id)
        assert env_spec, "Environment was not updated"
        return env_spec

    async def delete_env_spec(self, env_spec: fragments.ExecutionEnvironmentSpec) -> None:
        console.print(f"Deleting environment '{env_spec.execution_environment_spec_name}'...", end="")
        await self._sdk.delete_environment(environment_id=env_spec.execution_environment_spec_id)
        console.print("✅ ")

    async def apply_app_specs(self, app_spec_plan: AppSpecPlan, env_spec_name_to_id: dict[str, str]) -> None:
        app_specs_to_create, app_specs_to_update, app_specs_to_delete = app_spec_plan

        has_app_updates = (len(app_specs_to_create) + len(app_specs_to_update) + len(app_specs_to_delete)) > 0
        if not has_app_updates:
            console.print("No changes detected to apps, runs, or deployments ✅ ")
            return

        # Note: temporary hack to make sure runs are created before everything else. This is needed because
        # Label Studio Apps now have references to run ids (which must exist before the app is created)
        run_specs_to_create = [app_spec for app_spec in app_specs_to_create if isinstance(app_spec, schemas.RunSpec)]
        remaining_apps_to_create = [
            app_spec for app_spec in app_specs_to_create if not isinstance(app_spec, schemas.RunSpec)
        ]

        # Similarly, we need to delete runs last due to the foreign key constraint
        run_specs_to_delete = [app_spec for app_spec in app_specs_to_delete if app_spec.app_type == schemas.AppType.RUN]
        remaining_apps_to_delete = [
            app_spec for app_spec in app_specs_to_delete if app_spec.app_type != schemas.AppType.RUN
        ]

        for spec in run_specs_to_create:
            try:
                await self.create_app_spec(
                    app_spec=spec, exec_env_spec_id=env_spec_name_to_id[spec.environment] if spec.environment else None
                )
            except Exception as e:
                raise SlingshotException(f"Failed to create: {e}") from e

        for spec in remaining_apps_to_create:
            try:
                # Note: if we're creating a Label Studio app, we need to fetch the import and export run ids first
                #  If/when we generalize Apps to own Runs, we should refactor this (or if this starts to get too messy)
                import_run_spec = None
                export_run_spec = None
                if isinstance(spec, schemas.LabelStudioAppSpec):
                    import_run_spec = await self._sdk.get_app(spec.import_run)
                    export_run_spec = await self._sdk.get_app(spec.export_run)
                    assert import_run_spec, f"Import run '{spec.import_run}' does not exist"
                    assert export_run_spec, f"Export run '{spec.export_run}' does not exist"
                env_name = getattr(spec, "environment", None)
                env_spec_id = env_spec_name_to_id[env_name] if env_name else None
                _ = await self.create_app_spec(
                    app_spec=spec,
                    exec_env_spec_id=env_spec_id,
                    import_run_spec=import_run_spec,
                    export_run_spec=export_run_spec,
                )
            except Exception as e:
                raise SlingshotException(f"Failed to create app: {e}") from e

        for spec, spec_id in app_specs_to_update:
            try:
                env_name = getattr(spec, "environment", None)
                env_spec_id = env_spec_name_to_id[env_name] if env_name else None
                await self.update_app_spec(app_spec=spec, existing_app_spec_id=spec_id, exec_env_spec_id=env_spec_id)
            except Exception as e:
                raise SlingshotException(f"Failed to update app: {e}") from e
        for spec in remaining_apps_to_delete:
            try:
                await self.delete_app_spec(spec)
            except Exception as e:
                raise SlingshotException(f"Failed to delete: {e}") from e
        for spec in run_specs_to_delete:
            try:
                await self.delete_app_spec(spec)
            except Exception as e:
                raise SlingshotException(f"Failed to delete: {e}") from e

    async def create_app_spec(
        self,
        app_spec: schemas.SlingshotAbstractAppSpec,
        exec_env_spec_id: str | None = None,
        import_run_spec: schemas.HasAppSpecId | None = None,
        export_run_spec: schemas.HasAppSpecId | None = None,
    ) -> schemas.HasAppSpecId:
        console.print(f"Creating '{app_spec.name}'...", end="")
        app_type = _get_app_type(app_spec)
        app_sub_type = _get_app_sub_type(app_spec)
        machine_size = machine_type_gpu_count_to_machine_size(app_spec.machine_type, app_spec.num_gpu)
        app_spec_id_response = await self._sdk.create_app(
            name=app_spec.name,
            command=app_spec.cmd if hasattr(app_spec, "cmd") else None,
            app_type=app_type,
            app_sub_type=app_sub_type,
            exec_env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            mounts=app_spec.mounts,
            attach_project_credentials=(
                app_spec.attach_project_credentials if hasattr(app_spec, "attach_project_credentials") else False
            ),
            config_variables=app_spec.config_variables,
            app_port=app_spec.port if hasattr(app_spec, "port") else None,
            import_run_spec_id=import_run_spec.app_spec_id if import_run_spec else None,
            export_run_spec_id=export_run_spec.app_spec_id if export_run_spec else None,
        )
        app_spec_id = get_data_or_raise(app_spec_id_response)
        console.print("✅")
        return app_spec_id

    async def update_app_spec(
        self,
        app_spec: schemas.SlingshotAbstractAppSpec,
        existing_app_spec_id: str,
        exec_env_spec_id: str | None = None,
        import_run_spec: schemas.HasAppSpecId | None = None,
        export_run_spec: schemas.HasAppSpecId | None = None,
    ) -> None:
        console.print(f"Updating app '{app_spec.name}'...", end="")
        machine_size = machine_type_gpu_count_to_machine_size(app_spec.machine_type, app_spec.num_gpu)
        await self._sdk.update_app(
            app_spec_id=existing_app_spec_id,
            command=app_spec.cmd if hasattr(app_spec, "cmd") else None,
            env_spec_id=exec_env_spec_id,
            machine_size=machine_size,
            config_variables=app_spec.config_variables,
            mounts=app_spec.mounts,
            attach_project_credentials=(
                app_spec.attach_project_credentials if hasattr(app_spec, "attach_project_credentials") else False
            ),
            app_port=app_spec.port if hasattr(app_spec, "port") else None,
            batch_size=app_spec.batch_size if hasattr(app_spec, "batch_size") else None,
            batch_interval=app_spec.batch_interval if hasattr(app_spec, "batch_interval") else None,
            import_run_spec_id=import_run_spec.app_spec_id if import_run_spec else None,
            export_run_spec_id=export_run_spec.app_spec_id if export_run_spec else None,
        )
        console.print("✅ ")

    async def delete_app_spec(self, app_spec: fragments.AppSpec) -> None:
        console.print(
            f"Deleting {app_spec.friendly_app_type} '{app_spec.app_spec_name}' from the remote project manifest...",
            end="",
        )
        await self._sdk.delete_app(app_spec_id=app_spec.app_spec_id)
        console.print("✅ ")

    async def apply_changes_to_remote(self, env_spec_plan: EnvSpecPlan, app_spec_plan: AppSpecPlan) -> None:
        """
        Applies all environments and app specs in the given plans by updating the remote.
        """
        console.print(f"Applying 'slingshot.yaml' for project '{self._project.project_id}'.")
        env_spec_name_to_id = await self.apply_env_specs(env_spec_plan=env_spec_plan)
        await self.apply_app_specs(app_spec_plan=app_spec_plan, env_spec_name_to_id=env_spec_name_to_id)
        config.project_config.last_pushed_manifest = load_slingshot_project_config()

    async def check_conflicts_pull_remote_changes(self, force: bool = False) -> bool:
        """
        Pulls the remote manifest to the local slingshot.yaml.

        The last pushed manifest is used as the base of the initial diff. If there is no last-pushed manifest,
        the base is an empty manifest so that all remote changes are computed in the diff and can be pulled.
        Then, the local slingshot.yaml applied using the resulting diff. If there are conflicts, the user is
        prompted to override either the local or remote changes.

        Returns True if there were changes pulled, False otherwise.
        """
        # Step 1. Load all manifests (local, last_pushed, remote)
        local_manifest = _load_local_manifest(create_empty=True)
        last_pushed_manifest, is_last_pushed_manifest_empty = _load_last_pushed_manifest()
        remote_manifest = await remote_project_manifest(self._sdk, raise_on_error=not force)

        # Step 2. Compute diff between the last pushed and remote, and the last pushed and local
        remote_diff = compute_project_manifest_diff(last_pushed_manifest, remote_manifest)
        local_diff = compute_project_manifest_diff(last_pushed_manifest, local_manifest)
        if not remote_diff:
            logger.debug("No remote changes detected")
            return False

        # Step 3. Check for conflicts between the remote and local relative to the last pushed manifest
        if not force and detect_local_remote_diff_conflicts(local_diff=local_diff, remote_diff=remote_diff):
            console.print("[red]Conflict detected[/red]")
            return await _handle_conflict(
                local_diff=local_diff, remote_diff=remote_diff, remote_manifest=remote_manifest, force=force
            )

        # Step 4. Pull any changes from the remote into the local manifest
        console.print("Changes found on the remote since your last push:")
        console.print(diff_to_str(remote_diff))
        try:
            apply_diff_to_local_manifest(remote_diff, remote_manifest, force=force)
            config.project_config.last_pushed_manifest = load_slingshot_project_config()
            console.print("[green]Changes pulled to your local 'slingshot.yaml'[/green]")
            return True
        except Exception as e:
            sentry_sdk.capture_exception(e)
            console.print("[red]An error occurred while pulling[/red]")
            console.print("Changes found on the local copy since your last push:")
            console.print(diff_to_str(local_diff))
            return await _prompt_override_local_remote(diff=remote_diff, remote_manifest=remote_manifest, force=force)

    async def apply(self, *, force: bool) -> bool:
        """
        Detects conflicts, pulls, and then applies local changes to the remote.

        Returns if any changes were applied or pulled.
        """
        # 1. Check for conflicts between the remote and local manifests and pull changes from the remote
        any_changes_pulled = await self.check_conflicts_pull_remote_changes(force=force)

        # 2. Plan and apply changes from local to the remote
        local_manifest = load_slingshot_project_config()  # Reload local, in case it was changed
        env_spec_plan, app_spec_plan = await self.plan(config_=local_manifest)
        if any(env_spec_plan) or any(app_spec_plan):
            if force or prompt_confirm("Do you want to apply these changes?", default=True):
                await self.apply_changes_to_remote(env_spec_plan=env_spec_plan, app_spec_plan=app_spec_plan)
                return True
            return any_changes_pulled

        # Make sure the last pushed manifest is at parity with the local manifest if there were no plan changes
        config.project_config.last_pushed_manifest = load_slingshot_project_config()
        return any_changes_pulled


async def _prompt_override_local_remote(
    diff: list[DiffItem], remote_manifest: schemas.ProjectManifest, *, force: bool
) -> bool:
    """Overwrites the local manifest with the applied diff. Returns if changes were applied."""
    console.print("[yellow]Unable to sync remote changes with your local 'slingshot.yaml'[/yellow]")
    if not force:
        prompt_result = prompt_for_single_choice(
            "Do you want to use the local or remote version?", ["local", "remote", "resolve manually"], default=0
        )
        if prompt_result == 0:
            config.project_config.last_pushed_manifest = load_slingshot_project_config()
            console.print(
                "[bold]Ignored[/bold] the remote changes. To override the remote manifest with your local "
                "'slingshot.yaml', run 'slingshot apply -f'."
            )
            return False
        elif prompt_result == 2:
            with edit_slingshot_yaml(raise_if_absent=False, filename=".slingshot.remote.yaml") as slingshot_yaml:
                slingshot_yaml.clear()
                slingshot_yaml.update(remote_manifest.model_dump())

            console.print(
                "[bold]Manual resolution:[/bold] A copy of the remote slingshot manifest has been saved to "
                "'.slingshot.remote.yaml'. Please resolve the conflicts manually in 'slingshot.yaml' and then "
                "force-apply your local resolution with 'slingshot apply -f'."
            )
            return False

    # If force pull or the user chose to use the remote for conflict resolution, apply remote diff to local manifest
    apply_diff_to_local_manifest(diff, reference_manifest=remote_manifest, force=True)
    config.project_config.last_pushed_manifest = load_slingshot_project_config()
    return True


def _get_app_type(spec: schemas.SlingshotAbstractAppSpec) -> schemas.AppType:
    if isinstance(spec, schemas.RunSpec):
        return schemas.AppType.RUN
    elif isinstance(spec, schemas.DeploymentSpec):
        return schemas.AppType.DEPLOYMENT
    else:
        return schemas.AppType.CUSTOM


def _get_app_sub_type(spec: schemas.SlingshotAbstractAppSpec) -> schemas.AppSubType | None:
    if isinstance(spec, schemas.SlingshotCustomAppSpec):
        return schemas.AppSubType.WEBAPP
    if isinstance(spec, schemas.SessionAppSpec):
        return schemas.AppSubType.SESSION
    if isinstance(spec, schemas.RedisAppSpec):
        return schemas.AppSubType.REDIS
    if isinstance(spec, schemas.LabelStudioAppSpec):
        return schemas.AppSubType.LABEL_STUDIO
    return None


def _diff_existing_env_yaml_specs(
    existing_env_specs: list[fragments.ExecutionEnvironmentSpec], yaml_env_specs: dict[str, schemas.EnvironmentSpec]
) -> tuple[
    list[tuple[schemas.EnvironmentSpec, str]],  # tuple of spec, name
    list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]],  # tuple of spec, existing spec to update
    list[fragments.ExecutionEnvironmentSpec],  # existing specs to delete
    set[str],  # updated spec names
    list[str],  # change messages
]:
    env_specs_to_create: list[tuple[schemas.EnvironmentSpec, str]] = []
    env_specs_to_update: list[tuple[schemas.EnvironmentSpec, fragments.ExecutionEnvironmentSpec]] = []
    env_specs_to_delete: list[fragments.ExecutionEnvironmentSpec] = []

    existing_env_names = {spec.execution_environment_spec_name for spec in existing_env_specs}
    existing_env_name_to_spec = {spec.execution_environment_spec_name: spec for spec in existing_env_specs}
    yaml_env_names = {spec_name for spec_name in yaml_env_specs.keys()}

    updated_spec_names: set[str] = set()
    change_msgs: list[str] = []
    for spec_name, env_spec in yaml_env_specs.items():
        if spec_name not in existing_env_names:
            change_msgs.append(f"[green](+)[/green] environment '{spec_name}'")
            env_specs_to_create.append((env_spec, spec_name))
            continue

        _change_msgs: list[str] = []
        existing_env_spec = existing_env_name_to_spec[spec_name]
        if diff := env_spec.diff(existing_env_spec):
            _change_msgs.extend(f"\t- {i}" for i in diff)
        if _change_msgs:
            change_msgs.append(f"Detected [yellow]changes[/yellow] to environment '{spec_name}'")
            change_msgs.extend(_change_msgs)
            updated_spec_names.add(spec_name)
            env_specs_to_update.append((env_spec, existing_env_spec))

    for existing_spec in existing_env_specs:
        if existing_spec.execution_environment_spec_name not in yaml_env_names:
            logger.debug(
                f"Detected environment '{existing_spec.execution_environment_spec_name}' has been [red]deleted[/red]"
            )
            logger.debug(f"\t- Environment will be [red]deleted[/red]")
            env_specs_to_delete.append(existing_spec)

    return env_specs_to_create, env_specs_to_update, env_specs_to_delete, updated_spec_names, change_msgs


def _diff_existing_app_yaml_specs(
    all_existing_app_specs: list[fragments.AppSpec],
    yaml_app_specs: list[schemas.SlingshotAbstractAppSpec],
    app_type: schemas.AppType,
    app_sub_type: schemas.AppSubType | None = None,
) -> tuple[
    list[schemas.SlingshotAbstractAppSpec],
    list[tuple[schemas.SlingshotAbstractAppSpec, str]],
    list[fragments.AppSpec],
    list[str],
]:
    spec_display_type = "app"
    if app_type == schemas.AppType.DEPLOYMENT:
        spec_display_type = "deployment"
    elif app_type == schemas.AppType.RUN:
        spec_display_type = "run"
    elif app_sub_type == schemas.AppSubType.WEBAPP:
        spec_display_type = "webapp"
    elif app_sub_type == schemas.AppSubType.SESSION:
        spec_display_type = "session"
    elif app_sub_type == schemas.AppSubType.REDIS:
        spec_display_type = "redis"
    elif app_sub_type == schemas.AppSubType.LABEL_STUDIO:
        spec_display_type = "label-studio"

    app_specs_to_create: list[schemas.SlingshotAbstractAppSpec] = []
    app_specs_to_update: list[tuple[schemas.SlingshotAbstractAppSpec, str]] = []
    app_specs_to_delete: list[fragments.AppSpec] = []

    existing_app_specs = [spec for spec in all_existing_app_specs if spec.app_type == app_type]
    existing_spec_name_to_spec: dict[str, fragments.AppSpec] = {
        app_spec.app_spec_name: app_spec for app_spec in existing_app_specs
    }
    yaml_app_spec_names = {app_spec.name for app_spec in yaml_app_specs}

    change_msgs: list[str] = []
    for app_spec in yaml_app_specs:
        if app_spec.name not in existing_spec_name_to_spec:
            change_msgs.append(f"[green](+)[/green] {spec_display_type} '{app_spec.name}'")
            app_specs_to_create.append(app_spec)
            continue

        existing_app_spec = existing_spec_name_to_spec[app_spec.name]
        _change_msgs: list[str] = []
        if app_spec_diff := app_spec.diff(existing_app_spec):
            _change_msgs.extend(f"\t- {i}" for i in app_spec_diff)
        if _change_msgs:
            change_msgs.append(f"[yellow]Changes[/yellow] to {spec_display_type} '{app_spec.name}'")
            change_msgs.extend(_change_msgs)
            if app_type in (schemas.AppType.CUSTOM, schemas.AppType.DEPLOYMENT):
                change_msgs.append(f"\t(Your {spec_display_type} will not be restarted)")

        # Only update if there are changes to the app spec itself, not just the environment
        if len(app_spec_diff) > 0:
            app_specs_to_update.append((app_spec, existing_app_spec.app_spec_id))

    for existing_app_spec in existing_app_specs:
        if existing_app_spec.app_spec_name not in yaml_app_spec_names and (
            _normalize_app_sub_type(existing_app_spec) == app_sub_type
        ):
            console.print(f"[red](-)[/red] {spec_display_type} '{existing_app_spec.app_spec_name}'")
            app_specs_to_delete.append(existing_app_spec)

    return app_specs_to_create, app_specs_to_update, app_specs_to_delete, change_msgs


def _normalize_app_sub_type(app: fragments.AppSpec) -> Optional[schemas.AppSubType]:
    """
    Ensures that a custom app always has a sub app type. Prior to Aug 2023, apps without a
    'using' configured (wihtout a sub type) were treated by default as web apps.
    """
    if app.app_type == schemas.AppType.CUSTOM and app.app_sub_type is None:
        return schemas.AppSubType.WEBAPP
    return app.app_sub_type


async def remote_project_manifest(sdk: "SlingshotSDK", raise_on_error: bool = True) -> schemas.ProjectManifest:
    existing_env_specs = await sdk.list_environments()
    env_specs_by_name = {}
    for env_spec in existing_env_specs:
        assert env_spec.environment_instances, "Environment spec has no instances"
        env_instance = env_spec.environment_instances[0]
        parsed_env_spec = schemas.EnvironmentSpec(
            python_packages=[
                str(schemas.RequestedRequirement.model_validate(i)) for i in env_instance.requested_python_requirements
            ],
            apt_packages=[
                schemas.RequestedAptPackage.model_validate(i).name for i in env_instance.requested_apt_packages
            ],
            post_install_command=env_instance.post_install_command,
        )
        env_specs_by_name[env_spec.execution_environment_spec_name] = parsed_env_spec

    app_specs: list[schemas.SlingshotAbstractAppSpec] = []
    existing_app_specs = await sdk.list_apps()
    for spec in existing_app_specs:
        name = spec.app_spec_name
        existing_env_spec = spec.execution_environment_spec
        environment = existing_env_spec.execution_environment_spec_name if existing_env_spec else None
        config_variables = json.loads(spec.config_variables) if spec.config_variables else {}
        port = spec.app_port
        attach_project_credentials = spec.service_account
        cmd = spec.app_spec_command
        machine_type, num_gpu = machine_size_to_machine_type_gpu_count(spec.machine_size)
        mounts = [schemas.remote_mount_spec_to_local(ms) for ms in spec.mount_specs]
        if spec.app_type == schemas.AppType.CUSTOM and (
            spec.app_sub_type is None or spec.app_sub_type == schemas.AppSubType.WEBAPP
        ):
            app_specs.append(
                schemas.SlingshotCustomAppSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    port=port,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    using="webapp",
                    mounts=mounts,
                )
            )
        elif spec.app_type == schemas.AppType.CUSTOM and spec.app_sub_type == schemas.AppSubType.SESSION:
            app_specs.append(
                schemas.SessionAppSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    using="session",
                    mounts=mounts,
                )
            )
        elif spec.app_type == schemas.AppType.CUSTOM and spec.app_sub_type == schemas.AppSubType.REDIS:
            app_specs.append(
                schemas.RedisAppSpec(
                    name=name, environment=environment, machine_type=machine_type, num_gpu=num_gpu, using="redis"
                )
            )
        elif spec.app_type == schemas.AppType.CUSTOM and spec.app_sub_type == schemas.AppSubType.LABEL_STUDIO:
            app_specs.append(
                schemas.LabelStudioAppSpec(
                    name=name, environment=environment, machine_type=machine_type, num_gpu=num_gpu, using="label-studio"
                )
            )
        elif spec.app_type == schemas.AppType.RUN:
            app_specs.append(
                schemas.RunSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    mounts=mounts,
                )
            )
        elif spec.app_type == schemas.AppType.DEPLOYMENT:
            app_specs.append(
                schemas.DeploymentSpec(
                    name=name,
                    environment=environment,
                    machine_type=machine_type,
                    num_gpu=num_gpu,
                    config_variables=config_variables,
                    attach_project_credentials=attach_project_credentials,
                    cmd=cmd,
                    mounts=mounts,
                )
            )
        else:
            raise ValueError(f"Unknown app type {spec.app_type}")

    try:
        return schemas.ProjectManifest(
            environments=env_specs_by_name,
            apps=[
                app
                for app in app_specs
                if isinstance(
                    app,
                    (
                        schemas.SlingshotCustomAppSpec,
                        schemas.SessionAppSpec,
                        schemas.RedisAppSpec,
                        schemas.LabelStudioAppSpec,
                    ),
                )
            ],
            runs=[app for app in app_specs if isinstance(app, schemas.RunSpec)],
            deployments=[app for app in app_specs if isinstance(app, schemas.DeploymentSpec)],
        )
    except SlingshotException as e:
        if raise_on_error:
            raise SlingshotException(
                f"Error reading the remote slingshot manifest: {e.cli} -- Contact slingshot support for help."
            )
        console.print(f"[yellow]Warning[/yellow]: {e}")
        return ProjectManifest()  # Return an empty manifest if we failed to load and don't want to raise


async def _handle_conflict(
    local_diff: list[DiffItem], remote_diff: list[DiffItem], remote_manifest: schemas.ProjectManifest, force: bool
) -> bool:
    console.print("Changes found on the remote since your last push:")
    console.print(diff_to_str(remote_diff))
    console.print("Changes found on the local copy since your last push:")
    console.print(diff_to_str(local_diff))
    return await _prompt_override_local_remote(diff=remote_diff, remote_manifest=remote_manifest, force=force)


def _load_local_manifest(create_empty: bool) -> schemas.ProjectManifest:
    """Load the current local manifest, or create an empty one if it doesn't exist."""
    if create_empty:
        try:
            current_manifest = load_slingshot_project_config()  # Reload local, in case it was changed
        except SlingshotFileNotFoundException:
            create_empty_project_manifest(client_settings.slingshot_config_path)
            current_manifest = load_slingshot_project_config()  # Reload local, which is now an empty manifest.
    else:
        current_manifest = load_slingshot_project_config()
    return current_manifest


def _load_last_pushed_manifest() -> tuple[schemas.ProjectManifest, bool]:
    """Load the last pushed manifest, and return if the last pushed manifest is empty."""
    last_pushed_manifest_dict = config.project_config.last_pushed_manifest
    is_last_pushed_manifest_empty = last_pushed_manifest_dict is None

    # First make sure this is a valid project manifest
    if last_pushed_manifest_dict:
        last_pushed_manifest = ProjectManifest.model_validate(last_pushed_manifest_dict)
    else:
        # If there is no last pushed manifest, we use an empty manifest as the base of the diff to ensure that
        #  all remote changes are computed in the plan and can be applied correctly.
        last_pushed_manifest = ProjectManifest()
    return last_pushed_manifest, is_last_pushed_manifest_empty
