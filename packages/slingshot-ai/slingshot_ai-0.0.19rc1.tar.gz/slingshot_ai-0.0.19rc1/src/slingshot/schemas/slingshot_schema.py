from __future__ import annotations

import json
from abc import ABC
from pathlib import Path
from typing import Annotated, Any, Literal, Optional, Union

import deepdiff
from pydantic import BaseModel, ConfigDict, Field, RootModel, TypeAdapter, field_validator, model_validator
from pydantic_core.core_schema import FieldValidationInfo

from slingshot import schemas
from slingshot.schemas.utils import has_path_ending_in_filename
from slingshot.schemas.validation_warnings import SlingshotDeprecationWarning, record_validation_warning
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.graphql import fragments
from slingshot.shared.utils import (
    get_default_num_gpu,
    machine_size_to_machine_type_gpu_count,
    machine_type_gpu_count_to_machine_size,
)

REPO = "https://github.com/slingshot-ai/slingshot"
PATH_TO_FILE = "slingshot_client/src/slingshot/schemas"
FILENAME = "slingshot-schema.config.json"
FILE_LOCATION = "/".join([REPO, "blob/main", PATH_TO_FILE, FILENAME])
ALPHANUMERIC_UNDERSCORE_HYPHEN_RE = "^[A-Za-z][A-Za-z0-9_-]*$"  # This should match the regex on the backend


class SlingshotBaseModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


# NOTE: We prefer to forbid extra fields, but this is not compatible with how Pydantic parse unions where fields
# are required in some places and not permitted in others. This would be clean if we had a single field that
# explicitly discriminated the type of subclass, but this does not work here as we support either a name or a tag,
# but without any other field that controls which.
class BaseMountSpec(SlingshotBaseModel):
    mode: str = Field(..., title="Mode", description="The mode to use for the mount.")
    path: str = Field(..., title="Path", description="The path to mount into the environment.", pattern=r'/mnt/[\w-]+')

    @field_validator('path', mode='after')
    @classmethod
    def fail_on_mount_paths_that_look_like_filenames(cls, path: str) -> str:
        if has_path_ending_in_filename(path):
            raise ValueError(
                f"The specified mount path '{path}' appears to be a filename. "
                + "Mounts paths must refer to directories, rather than individual files"
            )
        return path

    def diff(self, other: BaseMountSpec) -> list[str]:
        what_changed = []
        if self.mode != other.mode:
            what_changed.append(f"mode: {other.mode} → {self.mode}")
        if self.path != other.path:
            what_changed.append(f"path: {other.path} → {self.path}")
        return what_changed


class MountSelectionFields(BaseModel):
    name: str = Field(..., title="Name", description="The name of the artifact to download/upload.")
    tag: Optional[str] = Field(None, title="Tag", description="The tag of the artifact.")

    def diff(self, other: MountSelectionFields) -> list[str]:
        what_changed = []
        if self.name != other.name:
            what_changed.append(f"name: {other.name} → {self.name}")
        if self.tag != other.tag:
            what_changed.append(f"tag: {other.tag} → {self.tag}")
        return what_changed


class DownloadMountSpec(BaseMountSpec):
    mode: Literal["DOWNLOAD"] = Field("DOWNLOAD", title="Mode", description="The mode to use for the mount.")
    selector: MountSelectionFields = Field(..., title="Selector", description="The artifact selector.")

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, DownloadMountSpec):
            d.extend(self.selector.diff(other.selector))
        return d


class UploadMountSpec(BaseMountSpec):
    mode: Literal["UPLOAD"] = Field("UPLOAD", title="Mode", description="The mode to use for the mount.")
    target: MountSelectionFields = Field(..., title="Target", description="The artifact target for selection.")

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, UploadMountSpec):
            d.extend(self.target.diff(other.target))
        return d


class VolumeMountSpec(BaseMountSpec):
    mode: Literal["VOLUME"] = Field("VOLUME", title="Mode", description="The mode to use for the mount.")
    name: str = Field(..., title="Name", description="The name of the volume to mount.")

    def diff(self, other: BaseMountSpec) -> list[str]:
        d = super().diff(other)
        if isinstance(other, VolumeMountSpec) and self.name != other.name:
            d.append(f"name: {other.name} → {self.name}")
        return d


MountSpecDiscriminatedUnion = Annotated[
    Union[DownloadMountSpec, UploadMountSpec, VolumeMountSpec], Field(discrimnator="mode")
]


class MountSpecUnion(RootModel[MountSpecDiscriminatedUnion]):
    """
    Reads an mount spec and performs validation based on mode. Using a root model appears to be the only way to add
    validation so that Pydantic doesn't try to validate against all the fields of all the subclasses.
    """

    @model_validator(mode='before')
    @classmethod
    def validate_mount_mode(cls, data: Any) -> Any:
        if isinstance(data, BaseModel):
            data = data.model_dump()

        if 'mode' not in data or not data['mode']:
            raise ValueError("Mount mode not specified.")

        if 'path' not in data or not data['path']:
            raise ValueError("Mount path not specified.")

        mode = data['mode']
        if mode not in ['DOWNLOAD', 'UPLOAD', 'VOLUME']:
            raise ValueError(f"Invalid mount mode: {mode}")

        if mode == 'DOWNLOAD' and ('selector' not in data or not data['selector']):
            raise ValueError("Download mount selector not specified.")
        if mode == 'UPLOAD' and ('target' not in data or not data['target']):
            raise ValueError("Upload mount target not specified.")
        if mode == 'VOLUME' and ('name' not in data or not data['name']):
            raise ValueError("Volume mount name not specified.")
        return data


def remote_mount_spec_to_local(mount_spec: fragments.MountSpec) -> MountSpecDiscriminatedUnion:
    if mount_spec.mode == "DOWNLOAD":
        return DownloadMountSpec(
            path=mount_spec.path, selector=MountSelectionFields(name=mount_spec.name, tag=mount_spec.tag)
        )
    elif mount_spec.mode == "UPLOAD":
        return UploadMountSpec(
            path=mount_spec.path, target=MountSelectionFields(name=mount_spec.name, tag=mount_spec.tag)
        )
    elif mount_spec.mode == "VOLUME":
        return VolumeMountSpec(path=mount_spec.path, name=mount_spec.name)
    raise SlingshotException(f"Unknown mount mode: {mount_spec.mode}")


def diff_mount_spec(new: MountSpecUnion, existing: fragments.MountSpec) -> list[str]:
    """Returns a list of differences between a local and a remote mount spec."""
    return new.diff(remote_mount_spec_to_local(existing))


class EnvironmentSpec(SlingshotBaseModel):
    python_version: Literal["3.10"] = Field("3.10", title="Python version")
    python_packages: list[str] = Field(
        default_factory=list,
        title="Python packages",
        description=f"List of Python packages to install in the environment.",
    )
    post_install_command: str = Field(
        "",
        title="Post-install command",
        description="Custom command to run after all packages have been installed. Skipped if not specified.",
    )
    apt_packages: list[str] = Field(
        default_factory=list, title="APT packages", description=f"List of APT packages to install"
    )
    model_config = ConfigDict(
        title="Environment",
        json_schema_extra={
            "example": {"python_version": "3.10", "python_packages": ["numpy", "pandas", "torch==2.0.1"]}
        },
    )

    # All python packages can be converted to RequestedRequirement
    @field_validator("python_packages")
    @classmethod
    def convert_python_packages(cls, v: list[str]) -> list[str]:
        for i in v:
            try:
                schemas.RequestedRequirement.from_str(i)
            except ValueError as e:
                raise ValueError(f"Error occurred while trying to parse python packages") from e
        return v

    def diff(self, existing: fragments.ExecutionEnvironmentSpec) -> list[str]:
        """Returns a list of differences between this and another environment."""
        diff = []
        current_python_packages = [schemas.RequestedRequirement.from_str(pkg) for pkg in self.python_packages]
        current_apt_packages = [schemas.RequestedAptPackage(name=pkg) for pkg in self.apt_packages]
        assert existing.environment_instances, "Environment spec has no instances"
        existing_env_instance = existing.environment_instances[0]
        existing_python_packages = TypeAdapter(list[schemas.RequestedRequirement]).validate_python(
            existing_env_instance.requested_python_requirements
        )
        existing_apt_packages = TypeAdapter(list[schemas.RequestedAptPackage]).validate_python(
            existing_env_instance.requested_apt_packages
        )
        existing_post_install_command = existing_env_instance.post_install_command

        if existing_post_install_command != self.post_install_command:
            existing_post_install_command_repr = existing_post_install_command.replace("\n", "\\n")
            new_post_install_command_repr = self.post_install_command.replace("\n", "\\n")
            diff.append(f"Post-install command: {existing_post_install_command_repr} → {new_post_install_command_repr}")

        python_package_diffs = self._diff_python_requirements(current_python_packages, existing_python_packages)
        if python_package_diffs:
            diff.append(f"Python packages changed")
            diff.extend(python_package_diffs)

        apt_package_diffs = self._diff_apt_packages(current_apt_packages, existing_apt_packages)
        if apt_package_diffs:
            diff.append(f"APT packages changed")
            diff.extend(apt_package_diffs)

        return diff

    @staticmethod
    def _diff_python_requirements(
        current: list[schemas.RequestedRequirement], existing: list[schemas.RequestedRequirement]
    ) -> list[str]:
        diff = []
        for req in current:
            if req not in existing:
                diff.append(f"  [green]+[/green] {str(req)}")
        for req in existing:
            if req not in current:
                diff.append(f"  [red]-[/red] {str(req)}")
        return diff

    @staticmethod
    def _diff_apt_packages(
        current: list[schemas.RequestedAptPackage], existing: list[schemas.RequestedAptPackage]
    ) -> list[str]:
        diff = []
        for req in current:
            if req not in existing:
                diff.append(f"  [green]+[/green] {req.name}")
        for req in existing:
            if req not in current:
                diff.append(f"  [red]-[/red] {req.name}")
        return diff


class SlingshotAbstractAppSpec(SlingshotBaseModel, ABC):
    name: str = Field(..., title="Name", description="The name of the app.", pattern=ALPHANUMERIC_UNDERSCORE_HYPHEN_RE)
    machine_type: schemas.MachineType = Field(None, title="Machine type", description="The machine type to be used.")
    num_gpu: int = Field(0, title="Number of GPUs", description="The number of GPUs to use.")
    config_variables: dict[str, Any] = Field(
        default_factory=dict, title="Arguments", description="Optional user defined arguments to pass to the app."
    )
    mounts: list[MountSpecUnion] = Field(default_factory=list, title="Mounts", description="The mounts to be attached.")
    attach_project_credentials: bool = Field(
        True,
        title="Attach project credentials",
        description=(
            "If true, will make an API key available to instances under the `SLINGSHOT_API_KEY` environment"
            "variable so that they can make requests using the Slingshot SDK for this project"
        ),
    )

    model_config = ConfigDict(title="App")

    @model_validator(mode='before')
    @classmethod
    def warn_on_missing_explicit_machine_type(cls, data: Any) -> Any:
        if 'machine_type' not in data or not data['machine_type']:
            default_machine_type = schemas.MachineType.CPU_SMALL
            record_validation_warning(
                SlingshotDeprecationWarning(
                    f"'machine_type' not set for '{data['name']}', defaulting to '{default_machine_type}'. "
                    + "Specifying machine_type will be required in upcoming versions of the CLI."
                )
            )
            return {**data, 'machine_type': default_machine_type}

        return data

    @field_validator("config_variables", mode='before')
    @classmethod
    def show_nicer_error_for_nested_config_variables(cls, v: dict[str, Any]) -> dict[str, Any]:
        """
        Pydantic will enforce this already but the errors aren't pretty, do a manual check here.
        """
        if not isinstance(v, dict):
            raise ValueError("config_variables must be a mapping")

        return v

    @field_validator("mounts")
    @classmethod
    def validate_mount_paths_unique(cls, v: list[MountSpecUnion]) -> list[MountSpecUnion]:
        """
        Verify that all download mount paths are unique, and all upload mount paths are unique.
        However, it should be possible for download and upload mounts to share the same mount path.
        """
        spec_roots = [spec.root for spec in v]
        download_paths = [str(spec.path) for spec in spec_roots if spec.mode == "DOWNLOAD"]
        if len(download_paths) != len(set(download_paths)):
            raise ValueError("All download mount paths must be unique.")

        upload_paths = [str(spec.path) for spec in spec_roots if spec.mode == "UPLOAD"]
        if len(upload_paths) != len(set(upload_paths)):
            raise ValueError("All upload mount paths must be unique.")
        return v

    @field_validator("num_gpu", mode="after")
    @classmethod
    def validate_num_gpu(cls, v: int | None, info: FieldValidationInfo) -> int:
        """Validate that the number of GPUs is valid based on machine_type."""
        machine_type: schemas.MachineType = info.data["machine_type"]
        v = v or get_default_num_gpu(machine_type)
        try:
            machine_type_gpu_count_to_machine_size(gpu_count=v, machine_type=machine_type)
        except ValueError as e:
            raise ValueError(f"Invalid number of GPUs ({v}) for machine type {machine_type}") from e
        return v

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        diff = []
        name = existing.app_spec_name
        config_variables = json.loads(existing.config_variables) if existing.config_variables else {}

        existing_machine_type, existing_num_gpu = machine_size_to_machine_type_gpu_count(existing.machine_size)
        self_machine_type = self.machine_type
        self_num_gpu = self.num_gpu

        if self.name != name:
            diff.append(f"Name changed from '{name}' → '{self.name}'")
        if deepdiff.DeepDiff(config_variables, self.config_variables, ignore_order=True):
            diff.append(f'Config variables changed from {config_variables} → {self.config_variables}')
        if self_machine_type != existing_machine_type:
            diff.append(f"Machine type changed from '{existing_machine_type}' → '{self_machine_type}'")
        if self_num_gpu != existing_num_gpu:
            diff.append(f"Number of GPUs changed from '{existing_num_gpu}' → '{self_num_gpu}'")
        if self.attach_project_credentials and not existing.service_account:
            diff.append(f"Project credentials added")
        elif not self.attach_project_credentials and existing.service_account:
            diff.append(f"Project credentials removed")

        mount_roots = [mount.root for mount in self.mounts]
        my_mount_path = {f"{i.mode}: {i.path}": i for i in mount_roots}
        existing_mounts = {f"{i.mode}: {i.path}": i for i in existing.mount_specs}
        added_keys = set(my_mount_path.keys()) - set(existing_mounts.keys())
        for i in added_keys:
            diff.append(f"Added mount '{i}'")
        removed_keys = set(existing_mounts.keys()) - set(my_mount_path.keys())
        for i in removed_keys:
            diff.append(f"Removed mount '{i}'")
        same_path = set(existing_mounts.keys()) & set(my_mount_path.keys())
        for i in same_path:
            existing = existing_mounts[i]
            new = my_mount_path[i]
            d = diff_mount_spec(new, existing)
            if d:
                diff.append(f"Changed mount '{i}': {d}")

        return diff


class SlingshotCustomAppSpec(SlingshotAbstractAppSpec):
    using: Literal['webapp'] = Field(
        'webapp', title="Using", description="Which package to use. Set to webapp for a custom web application."
    )
    port: Optional[int] = Field(None, title="Port", description="The port to expose.")
    cmd: str = Field(..., title="Command", description="The command to run.")
    environment: str = Field(..., title="Environment", description="The name of the environment.")

    model_config = ConfigDict(title="Web app")

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_type != schemas.AppType.CUSTOM:
            raise ValueError(f"Cannot diff an app against a non-app.")
        diff = super().diff(existing)
        env_spec = existing.execution_environment_spec
        environment = env_spec.execution_environment_spec_name if env_spec else None
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if self.cmd != existing.app_spec_command:
            diff.append(f"Command changed from '{existing.app_spec_command}' → '{self.cmd}'")
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class SessionAppSpec(SlingshotAbstractAppSpec):
    using: Literal['session'] = Field(
        'session',
        title="Using",
        description="Which package to use. When specified, this feature automatically adjusts the behavior of the app.",
    )
    # TODO: Allow users to not specify envs for Sessions
    environment: str = Field(..., title="Environment", description="The name of the execution environment.")

    model_config = ConfigDict(title="Session")

    @property
    def port(self) -> int:
        return 8080

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_sub_type != schemas.AppSubType.SESSION:
            raise ValueError(f"Cannot diff session app against a non-session.")
        diff = super().diff(existing)
        env_spec = existing.execution_environment_spec
        environment = env_spec.execution_environment_spec_name if env_spec else None
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class RedisAppSpec(SlingshotAbstractAppSpec):
    using: Literal['redis'] = Field(
        'redis',
        title="Using",
        description="Which package to use. When specified, this feature automatically adjusts the behavior of the app.",
    )

    model_config = ConfigDict(title="Redis")

    @property
    def port(self) -> int:
        return 6379

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_sub_type != schemas.AppSubType.REDIS:
            raise ValueError(f"Cannot diff Redis app against other app type.")
        diff = super().diff(existing)
        if self.port != existing.app_port:
            diff.append(f"Port changed from '{existing.app_port}' → '{self.port}'")
        return diff


class LabelStudioAppSpec(SlingshotAbstractAppSpec):
    using: Literal['label-studio'] = Field(
        'label-studio',
        title="Using",
        description="Which package to use. When specified, this feature automatically adjusts the behavior of the app.",
    )

    import_run: str = Field(
        "label-studio-import",
        title="Import Run",
        description="The name of the run used to import data to Label Studio.",
    )

    export_run: str = Field(
        "label-studio-export",
        title="Export Run",
        description="The name of the run used to export data from Label Studio.",
    )

    model_config = ConfigDict(title="Label Studio")

    @staticmethod
    def get_default_import_run() -> RunSpec:
        return RunSpec(
            name="label-studio-import",
            environment="label-studio-run-env",
            machine_type=schemas.MachineType.CPU_SMALL,
            cmd="python label_studio/label_studio_import.py",
            # Note, we have to explicitly set the mount mode in order for it to be written to the final YAML
            mounts=[
                DownloadMountSpec(mode="DOWNLOAD", path="/mnt/data", selector=MountSelectionFields(name="dataset"))
            ],
        )

    @staticmethod
    def get_default_export_run() -> RunSpec:
        return RunSpec(
            name="label-studio-export",
            environment="label-studio-run-env",
            machine_type=schemas.MachineType.CPU_SMALL,
            cmd="python label_studio/label_studio_export.py",
            attach_project_credentials=True,
        )

    @staticmethod
    def get_default_run_environment() -> EnvironmentSpec:
        return EnvironmentSpec(python_packages=["label-studio-sdk>=0.0.30", "slingshot-ai"])

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_sub_type != schemas.AppSubType.LABEL_STUDIO:
            raise ValueError(f"Cannot diff Label Studio app against other app type.")
        diff = super().diff(existing)
        # TODO: Add diff for import/export runs
        return diff


class RunSpec(SlingshotAbstractAppSpec):
    name: str = Field("run", title="Name", description="The name of the run.")
    cmd: str = Field(..., title="Command", description="The command to run.")
    environment: str = Field(..., title="Environment", description="The name of the environment.")

    model_config = ConfigDict(title="Run")

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_type != schemas.AppType.RUN:
            raise ValueError(f"Cannot diff a run against a non-run.")
        diff = super().diff(existing)
        env_spec = existing.execution_environment_spec
        environment = env_spec.execution_environment_spec_name if env_spec else None
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if self.cmd != existing.app_spec_command:
            diff.append(f"Command changed from '{existing.app_spec_command}' → '{self.cmd}'")
        return diff


class DeploymentSpec(SlingshotAbstractAppSpec):
    name: str = Field("deployment", title="Name", description="The name of the deployment.")
    cmd: str = Field(..., title="Command", description="The command to run.")
    environment: str = Field(..., title="Environment", description="The name of the environment.")

    model_config = ConfigDict(title="Deployment")

    def diff(self, existing: fragments.AppSpec) -> list[str]:
        """Returns a list of differences between this and another app spec."""
        if existing.app_type != schemas.AppType.DEPLOYMENT:
            raise ValueError(f"Cannot diff a run against a non-deployment.")
        diff = super().diff(existing)
        env_spec = existing.execution_environment_spec
        environment = env_spec.execution_environment_spec_name if env_spec else None
        if self.environment != environment:
            diff.append(f"Environment changed from '{environment}' → '{self.environment}'")
        if self.cmd != existing.app_spec_command:
            diff.append(f"Command changed from '{existing.app_spec_command}' → '{self.cmd}'")
        return diff


AppSpecUnion = Annotated[
    Union[SessionAppSpec, RedisAppSpec, LabelStudioAppSpec, SlingshotCustomAppSpec], Field(discriminator='using'),
]


class SafeAppSpec(RootModel[AppSpecUnion]):
    """
    Reads an app spec with extra validation for missing 'using'. Using a root model appears to be the only way to add
    validation before Pydantic picks the specific class to validate - this significantly improves the error message
    when no 'using' is specified.
    """

    @model_validator(mode='before')
    @classmethod
    def require_sub_type_to_be_specified(cls, data: Any) -> Any:
        if isinstance(data, BaseModel):
            data = data.model_dump()

        if 'using' not in data or not data['using']:
            record_validation_warning(
                SlingshotDeprecationWarning("Specifying 'using' for an app is required since version 0.0.19")
            )

            raise ValueError("Apps require a 'using' field to be specified, use 'webapp' for a custom web application")
        return data


class ProjectManifest(SlingshotBaseModel):
    environments: dict[str, EnvironmentSpec] = Field(
        default_factory=dict, title="Environments", description="The environments to use for the job."
    )
    apps: list[AppSpecUnion] = Field(default_factory=list, title=SlingshotAbstractAppSpec.model_config["title"])
    runs: list[RunSpec] = Field(default_factory=list, title=RunSpec.model_config["title"])
    deployments: list[DeploymentSpec] = Field(default_factory=list, title=DeploymentSpec.model_config["title"])
    model_config = ConfigDict(
        title="Slingshot Config Spec",
        from_attributes=True,
        json_schema_extra={"$schema": "http://json-schema.org/draft/2020-12/schema", "$id": FILE_LOCATION},
    )

    @field_validator('apps', mode='before')
    @classmethod
    def complain_if_missing_using_in_app(cls, value: Any) -> list[Any]:
        return [SafeAppSpec(app).root for app in value]

    @model_validator(mode="after")
    def slingshot_yaml_global_validator(cls, manifest: ProjectManifest) -> ProjectManifest:
        manifest = cls.validate_label_studio_runs(
            manifest
        )  # Must be before env validation, since it might add new envs
        manifest = cls.validate_environments_are_defined(manifest)
        manifest = cls.validate_session_environments(manifest)
        return manifest

    @model_validator(mode='before')
    @classmethod
    def check_machine_deprecations(cls, manifest: ProjectManifest) -> ProjectManifest:
        all_apps_runs_deployments = []
        all_apps_runs_deployments.extend(manifest['apps'] if 'apps' in manifest else [])
        all_apps_runs_deployments.extend(manifest['runs'] if 'runs' in manifest else [])
        all_apps_runs_deployments.extend(manifest['deployments'] if 'deployments' in manifest else [])

        # Check old GPUs
        for app_run_deployment in all_apps_runs_deployments:
            machine_type = app_run_deployment['machine_type'] if 'machine_type' in app_run_deployment else None
            if machine_type in {"GPU", "GPU_A100"}:
                record_validation_warning(
                    SlingshotDeprecationWarning(
                        f"Machine type '{machine_type}' is not supported in slingshot.yaml (since version '0.0.10'). "
                        + "Hint: Use 'slingshot machines' for machine options."
                    )
                )

        return manifest

    @staticmethod
    def validate_environments_are_defined(manifest: ProjectManifest) -> ProjectManifest:
        """Validate that all referenced environments are in the environments list"""
        envs: dict[str, EnvironmentSpec] = manifest.environments
        for app_or_run_or_deployment in [*manifest.apps, *manifest.runs, *manifest.deployments]:
            env = getattr(app_or_run_or_deployment, "environment", None)
            if env and env not in envs:
                name = getattr(app_or_run_or_deployment, "name", None)
                raise SlingshotException(
                    f"Environment '{env}' used in '{name}' not found in 'environments' {list(envs.keys())}"
                )
        return manifest

    @staticmethod
    def validate_session_environments(manifest: ProjectManifest) -> ProjectManifest:
        sessions = [app for app in manifest.apps if isinstance(app, SessionAppSpec)]
        envs: dict[str, EnvironmentSpec] = manifest.environments
        session_envs = {session.environment: envs[session.environment] for session in sessions if session.environment}

        for session_env_name, session_env in session_envs.items():
            requested_python_requirements = session_env.python_packages
            if not any("jupyterlab" in requirement for requirement in requested_python_requirements):
                raise SlingshotException(
                    f"'jupyterlab' was not found in the '{session_env_name}' environment. Please add it and try again."
                )
        return manifest

    @staticmethod
    def validate_label_studio_runs(manifest: ProjectManifest) -> ProjectManifest:
        """Make sure Label Studio is set up correctly"""
        label_studio_apps = [app for app in manifest.apps if isinstance(app, LabelStudioAppSpec)]
        if not label_studio_apps:
            return manifest
        if len(label_studio_apps) > 1:
            app_names = [app.name for app in label_studio_apps]
            # TODO: Implement logic for multiple label studio apps
            raise SlingshotException(f"Only one label studio app is supported per Slingshot Project. Found {app_names}")

        runs: list[RunSpec] = manifest.runs
        import_run_name = label_studio_apps[0].import_run
        export_run_name = label_studio_apps[0].export_run
        label_studio_app_name = label_studio_apps[0].name

        if import_run_name not in [run.name for run in runs]:
            raise SlingshotException(
                f"Run '{import_run_name}' (used as the 'import_run' for {label_studio_app_name}) was not found in "
                "'runs'. Please add it and try again."
            )

        if export_run_name not in [run.name for run in runs]:
            raise SlingshotException(
                f"Run '{export_run_name}' (used as the 'export_run' for {label_studio_app_name}) was not found in "
                "'runs'. Please add it and try again."
            )
        return manifest


if __name__ == "__main__":
    with open(Path(PATH_TO_FILE) / FILENAME, "w") as f:
        json.dump(ProjectManifest.model_json_schema(), f, indent=2)
