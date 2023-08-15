from __future__ import annotations

import re
import shutil
import uuid
from pathlib import Path
from typing import Callable, Literal, Optional, Type, cast

import typer
from pydantic import ValidationError

from slingshot.cli.config.slingshot_cli import SlingshotCLIApp
from slingshot.cli.shared import create_empty_project_manifest, prompt_confirm, prompt_for_single_choice
from slingshot.schemas import SlingshotAbstractAppSpec
from slingshot.schemas import slingshot_schema as slingshot_yaml_schemas
from slingshot.sdk import SlingshotSDK
from slingshot.sdk.config import client_settings
from slingshot.sdk.utils import console, edit_slingshot_yaml

from .. import schemas
from ..sdk.errors import SlingshotException
from ..shared.config import load_slingshot_project_config
from ..shared.utils import pydantic_to_dict
from .project import list_and_set_project_id

app = SlingshotCLIApp()

OPTIONS = ["run", "deployment", "app", "environment", "label-studio", "session"]
OPTION_TO_SPEC_CLASS: dict[str, Type[SlingshotAbstractAppSpec] | Type[slingshot_yaml_schemas.EnvironmentSpec]] = {
    "run": slingshot_yaml_schemas.RunSpec,
    "deployment": slingshot_yaml_schemas.DeploymentSpec,
    "app": slingshot_yaml_schemas.SlingshotCustomAppSpec,
    "environment": slingshot_yaml_schemas.EnvironmentSpec,
}


def _display_name_to_id(input_str: str) -> str:
    """Converts a name to a valid project ID by removing special characters and replacing spaces with hyphens."""
    lower = input_str.strip().lower()
    single_space = re.sub(r"\s+", "-", lower)
    single_hyphen = re.sub(r"-+", "-", single_space)
    alphanumeric_hyphen_underscore = re.sub(r"[^a-z0-9-_]", "", single_hyphen)
    return alphanumeric_hyphen_underscore


async def _create_project(sdk: SlingshotSDK) -> str:
    new_id = None
    display_name = typer.prompt("Enter a name for your project")

    # Use the display name to generate a project ID and append UUID if it's not available
    project_id_default = _display_name_to_id(display_name)
    if not await sdk._api.project_id_available(project_id_default):
        project_id_default = f"{project_id_default}-{uuid.uuid4().hex[:4]}"

    while True:
        # Replace multiple spaces with a single space and spaces with hyphens
        new_id = new_id or typer.prompt(
            "Enter a slug for your project (unique ID used for URLs)", default=project_id_default
        )
        try:
            project_response = await sdk.create_project(new_id, display_name=display_name)
            if project_response.error:
                console.print(f"[red]Error creating project[/red]: {project_response.error.message}")
                display_name = None
                new_id = None
                continue

            assert project_response.data is not None
            console.print(f"Created project: {new_id}")
            await sdk.use_project(project_response.data.project_id)
            return project_response.data.project_id
        except ValidationError as e:
            for error in e.errors():
                loc = error['loc']
                if loc[0] == 'project_id':
                    console.print(f"[red]Project slug is invalid[/red]: {error['msg']}")
                    new_id = None
                if loc[0] == 'project_display_name':
                    console.print(f"[red]Project name is invalid[/red]: {error['msg']}")
                    display_name = None


@app.command(requires_auth=False, requires_project=False, top_level=True, name="init")
async def init(*, sdk: SlingshotSDK) -> None:
    """Initialize a new project in the current directory"""
    has_project = bool(sdk.project_id)
    has_slingshot_yaml = (
        client_settings.slingshot_config_path.exists() and client_settings.slingshot_config_path.stat().st_size > 0
    )
    options = ["Create new project", "Select existing project"]

    if not has_project and not has_slingshot_yaml:
        create_or_choose_project = prompt_for_single_choice(
            "Create a new project or select an existing project?", options
        )
        if create_or_choose_project == 0:  # Create new project
            await _create_project(sdk)
            create_empty_project_manifest(client_settings.slingshot_config_path)
            await prompt_add_component(sdk)
            await sdk.apply_project()
        else:  # Select existing project
            await list_and_set_project_id(sdk)
            await sdk.pull_remote_changes()  # No YAML so we can just pull anything that exists on the remote
    if not has_project and has_slingshot_yaml:
        console.print(
            f"[yellow]slingshot.yaml[/yellow] detected, but no project is currently being tracked ({client_settings.slingshot_config_path})."
        )
        create_or_choose_project = prompt_for_single_choice(
            f"Create a new project (at {client_settings.slingshot_config_path}) or select an existing project?", options
        )
        if create_or_choose_project == 0:  # Create new project
            await _create_project(sdk)
        else:  # Select existing project
            await list_and_set_project_id(sdk)
        await sdk.apply_project()
    if has_project and not has_slingshot_yaml:
        console.print(f"Project '{sdk.project_id}' is already tracked.")
        if prompt_confirm("Do you want to pull any remote changes?", default=True):
            # TODO: Shouldn't the SDK already be setup at this point?
            await sdk.use_project(sdk.project_id)
            await sdk.pull_remote_changes()  # No YAML so we can just pull anything that exists on the remote
    if has_project and has_slingshot_yaml:
        console.print(
            f"Project '{sdk.project_id}' already initialized. You may modify it by editing the 'slingshot.yaml' or track another project with 'slingshot use'."
        )


async def prompt_add_component(sdk: SlingshotSDK) -> None:
    first = True
    while True:
        prompt = "Do you want to add another component?" if not first else "Do you want to add a component?"
        if not prompt_confirm(prompt, default=False):
            break
        await add_component.function(sdk=sdk, component=None)
        first = False


@app.command(requires_auth=False, requires_project=False, top_level=True, name="add")
async def add_component(
    *,
    sdk: SlingshotSDK,
    component: Optional[str] = typer.Argument(
        None, help="The component to add. One of " + ", ".join(OPTIONS), show_default=False
    ),
) -> None:
    """Add a component (run, deployment, app, environment) to the project"""
    if component is None:
        component_i = prompt_for_single_choice("What component do you want to add?", OPTIONS)
        component = OPTIONS[component_i]
    if component not in OPTIONS:
        raise typer.BadParameter(f"Invalid component: {component}. Must be one of " + ", ".join(OPTIONS))
    if component == "env":
        _create_new_environment()
    elif component == "label-studio":
        _create_label_studio()
    elif component == "session":
        _create_session()
    else:
        component = cast(Literal["run", "deployment", "app"], component)
        _create_app_spec(component, OPTION_TO_SPEC_CLASS[component])

    if not await sdk.is_signed_in():
        console.print(
            "Skipping apply because you are not logged in. You can run 'slingshot login' and then "
            "'slingshot apply' later."
        )
        return

    if not sdk.project_id:
        console.print(
            "Skipping apply because your project is not set. You can run 'slingshot use' and then "
            "'slingshot apply' later."
        )
        return

    await sdk.use_project(sdk.project_id)
    await sdk.apply_project()


def _create_new_environment(name: str | None = None) -> str:
    current = load_slingshot_project_config()  # For raising if absent
    if not current:
        raise SlingshotException("No Slingshot manifest found. Run 'slingshot init' first.")

    name = name or typer.prompt("Name of the environment")
    if name in current.environments:
        raise SlingshotException(f"Environment '{name}' already exists")

    # Allowed to be empty
    _options = ["pytorch", "tensorflow", "jax", "pytorch-serving", "session", "custom"]
    base_training_python_packages = ["numpy", "matplotlib", "pandas", "scikit-learn", "tqdm", "wandb"]
    base_env_idx = prompt_for_single_choice("What base environment do you want to use?", _options, default=0)
    base_env = _options[base_env_idx]
    if base_env == "custom":
        python_packages = typer.prompt(
            "List of Python packages to install (e.g. 'numpy, pandas, scikit-learn')", default="", show_default=False
        )
        python_packages = [p.strip() for p in python_packages.split(",")] if python_packages else []
    elif base_env == "pytorch":
        python_packages = ["torch", "torchvision"] + base_training_python_packages
    elif base_env == "tensorflow":
        python_packages = ["tensorflow"] + base_training_python_packages
    elif base_env == "jax":
        python_packages = ["jax", "jaxlib"] + base_training_python_packages
    elif base_env == "pytorch-serving":
        python_packages = ["torch", "torchvision", "fastapi", "uvicorn"]
    elif base_env == "session":
        python_packages = ["jupyterlab>=3.5.0"]
    else:
        raise NotImplementedError(f"Base environment {base_env} not implemented yet")

    environment = slingshot_yaml_schemas.EnvironmentSpec(python_packages=python_packages)
    current.environments[name] = environment
    with edit_slingshot_yaml() as doc:
        if "environments" not in doc:
            doc["environments"] = {}
        doc["environments"][name] = pydantic_to_dict(environment)
    console.print(f"Environment '{name}' added", style="green")
    return name


def _create_session(name: str | None = None) -> str:
    current = load_slingshot_project_config()

    current_session_environments = [
        key
        for key, value in current.environments.items()
        if any("jupyterlab" in package for package in value.python_packages)
    ]

    # Select an environment or create one if none exist
    env_name = _choose_or_create_environment(
        current_session_environments, new_env_name="session-env", new_env_auto_packages=["jupyterlab>=3.5.0"]
    )

    # Add a new session app if it doesn't already exist
    app_name = name or typer.prompt("Name of the session", default="session")
    if any(existing_app.name == app_name for existing_app in current.apps):
        console.print(f"App '{app_name}' already exists, skipping creation", style="yellow")
    else:
        session_app = schemas.SessionAppSpec(
            name=app_name, environment=env_name, using="session", machine_type=schemas.MachineType.CPU_SMALL
        )
        current.apps.append(session_app)
        with edit_slingshot_yaml() as doc:
            if not doc.get("apps"):
                doc["apps"] = []
            doc["apps"].append(pydantic_to_dict(session_app))
        console.print(f"App '{app_name}' added", style="green")
    return app_name


def _create_label_studio() -> None:
    current = load_slingshot_project_config()

    # Add a new label studio app if it doesn't already exist
    app_name = "label-studio"  # TODO: prompt for name
    ls_app = schemas.LabelStudioAppSpec(
        name=app_name,
        using="label-studio",
        machine_type=schemas.MachineType.CPU_SMALL,
        # TODO: include a volume so we automatically can persist data across app restarts
    )

    ls_runs_env = schemas.LabelStudioAppSpec.get_default_run_environment()
    _insert_env_if_not_exists(
        env_name="label-studio-run-env", python_packages=ls_runs_env.python_packages, current_manifest=current
    )
    import_run = schemas.LabelStudioAppSpec.get_default_import_run()
    export_run = schemas.LabelStudioAppSpec.get_default_export_run()

    _create_component_if_not_exists(ls_app, "app", current_manifest=current)
    _create_component_if_not_exists(import_run, "run", current_manifest=current)
    _create_component_if_not_exists(export_run, "run", current_manifest=current)

    if prompt_confirm(
        "Label Studio requires auxiliary runs to import and export data. Do you want to use template code for these runs?",
        default=True,
    ):
        _copy_template_to_user_dir(
            "label_studio/label_studio_data_export_template.py", "label_studio/label_studio_export.py"
        )
        _copy_template_to_user_dir(
            "label_studio/label_studio_data_import_template.py", "label_studio/label_studio_import.py"
        )
        _copy_template_to_user_dir("label_studio/label_studio_data_type.py", "label_studio/label_studio_data_type.py")
        console.print(
            "You should modify 'label_studio_data_type.py' to specify your data schema for annotation", style="yellow"
        )


def _create_component_if_not_exists(
    component: schemas.SlingshotAbstractAppSpec,
    component_type: Literal["run", "deployment", "app"],
    current_manifest: schemas.ProjectManifest,
) -> None:
    """Add a new app, run or deployment if it doesn't already exist"""
    components_of_type = getattr(current_manifest, component_type + "s")
    if any(existing_component.name == component.name for existing_component in components_of_type):
        console.print(f"{component_type.title()} '{component.name}' already exists, skipping creation", style="yellow")
    else:
        yaml_field_name = component_type + "s"
        with edit_slingshot_yaml() as doc:
            if not doc.get(yaml_field_name):
                doc[yaml_field_name] = []
            doc[yaml_field_name].append(pydantic_to_dict(component))
        console.print(f"{component_type.title()} '{component.name}' added", style="green")


def _insert_env_if_not_exists(
    env_name: str, python_packages: list[str], current_manifest: schemas.ProjectManifest
) -> None:
    if env_name in current_manifest.environments:
        console.print(f"Environment '{env_name}' already exists, skipping creation", style="yellow")
    else:
        environment = slingshot_yaml_schemas.EnvironmentSpec(python_packages=python_packages)
        current_manifest.environments[env_name] = environment
        with edit_slingshot_yaml() as doc:
            doc["environments"][env_name] = pydantic_to_dict(environment)
        console.print(f"Environment '{env_name}' added", style="green")


def _choose_or_create_environment(
    env_names: list[str], *, new_env_name: str, new_env_auto_packages: list[str] | None = None
) -> str:
    if len(env_names) == 1:
        env_name = list(env_names)[0]
        console.print(f"Defaulting to '{env_name}' as the environment", style="yellow")
        return env_name
    elif len(env_names) == 0 and new_env_name and new_env_auto_packages:
        env_name = new_env_name
        console.print(f"No suitable environments found -- creating a default one called '{env_name}'.", style="yellow")
        env_spec = slingshot_yaml_schemas.EnvironmentSpec(python_packages=new_env_auto_packages)
        with edit_slingshot_yaml() as doc:
            doc["environments"][env_name] = pydantic_to_dict(env_spec)
        console.print(f"Environment '{env_name}' added", style="green")
        return env_name

    environment: str | None = None

    if not env_names:
        # No environments yet. Create one.
        environment = _create_new_environment(new_env_name)
    else:
        options = env_names + ["Create a new environment"]
        choice = prompt_for_single_choice(
            prompt_text="Choose an environment to run this on:", values=options, default=0
        )
        if choice < len(env_names):
            environment = env_names[choice]

    if environment is None:
        # Create a new environment
        environment = _create_new_environment(new_env_name)

    return environment


def _create_app_spec(
    # class_ should be Type[SlingshotAppSpec] but Python doesn't like that
    type_: Literal["run", "deployment", "app", "environment"],
    class_: Callable[..., SlingshotAbstractAppSpec],
) -> slingshot_yaml_schemas.SlingshotAbstractAppSpec | None:
    current = load_slingshot_project_config()
    env_names = list(current.environments.keys())
    default_name = {"run": "train", "deployment": "deploy", "app": "my-app", "environment": "environment"}
    name = typer.prompt(f"Name of the {type_}", default=default_name[type_])

    if type_ == "environment" and any(env_name == name for env_name in env_names):
        raise SlingshotException(f"Environment '{name}' already exists")
    else:
        console.print(f"No existing {type_.title()} named '{name}' found", style="green")

    if type_ == "environment":
        _create_new_environment(name)
        return None

    environment = _choose_or_create_environment(env_names, new_env_name=f"{type_}-env")

    command: str | None = None
    mounts: list[schemas.MountSpecUnion] = []
    if type_ == "deployment" and prompt_confirm("Do you want to use a template?", default=True):
        command = "python inference.py"
        mounts = [
            schemas.DownloadMountSpec(
                path="/mnt/model", mode="DOWNLOAD", selector=schemas.MountSelectionFields(name="model")
            )
        ]
        _copy_template_to_user_dir("inference_template.py", "inference.py")
    elif type_ == "run":
        mounts = [
            schemas.UploadMountSpec(
                path="/mnt/output", mode="UPLOAD", target=schemas.MountSelectionFields(name="model")
            )
        ]

    default_ = {
        "run": "python train.py",
        "deployment": "python inference.py",
        "app": "uvicorn app:app --port 8080 --host 0.0.0.0",  # TODO: add uvicorn and fastapi to default app env
    }
    if not command:
        command = typer.prompt(f"Command to run the {type_}", default=default_[type_])

    params = {
        "name": name,
        "environment": environment,
        "machine_type": schemas.MachineType.CPU_SMALL,
        "cmd": command,
        "mounts": mounts,
    }
    if type_ == "app":
        params["port"] = 8080

    component = class_(**params)
    _create_component_if_not_exists(component, type_, current)
    return component


def _copy_template_to_user_dir(template_filename: str, target_filename: str) -> None:
    console.print(f"Copying a template to '{target_filename}'...")
    target_path = client_settings.slingshot_config_path.parent / target_filename
    if target_path.exists():
        if not prompt_confirm(f"File '{target_filename}' already exists. Overwrite?", default=False):
            console.print("Aborting", style="red")
            return  # No need to raise an exception, the user can just try again
    template_path = Path(__file__).parent.parent / "templates" / template_filename
    if not template_path.exists():
        raise SlingshotException(f"Template file {template_path} not found")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template_path, target_path)
    console.print(f"Template copied to '{target_filename}'")
