import inspect
import json
from typing import Optional, TextIO

import click

from .base import RootSchemaBaseModel
from .utils import SCHEMA_MODULES, current_schema_module, guess_schema_version

SCHEMA_VERSIONS = sorted(schema_module.VERSION for schema_module in SCHEMA_MODULES)
SCHEMA_VERSION_MODULES = {
    schema_module.VERSION: schema_module for schema_module in SCHEMA_MODULES
}


@click.group()
@click.version_option()
def cli() -> None:
    pass


@cli.command(name="versions", help="List all supported schema versions.")
def versions() -> None:
    for schema_version in SCHEMA_VERSIONS:
        click.echo(schema_version)


@cli.command(name="models", help="List all supported models.")
@click.option(
    "--version",
    "schema_version",
    type=click.Choice(SCHEMA_VERSIONS),
    default=current_schema_module.VERSION,
    show_default=True,
    help="Schema version.",
)
def models(schema_version: str) -> None:
    schema_module = SCHEMA_VERSION_MODULES[schema_version]
    for model_type_name, model_type in inspect.getmembers(
        schema_module, inspect.isclass
    ):
        if issubclass(model_type, RootSchemaBaseModel):
            click.echo(model_type_name)


@cli.command(name="generate", help="Generate a JSON Schema for the specified model.")
@click.option(
    "--version",
    "schema_version",
    type=click.Choice(SCHEMA_VERSIONS),
    default=current_schema_module.VERSION,
    show_default=True,
    help="Schema version.",
)
@click.option(
    "--indent",
    "indent",
    type=click.IntRange(min=0),
    default=2,
    show_default=True,
    help="JSON indentation level.",
    metavar="INTEGER",
)
@click.option(
    "-o",
    "json_schema_file",
    type=click.File("w"),
    help="Output JSON Schema file.",
)
@click.argument("model_type_name", metavar="MODEL", type=click.STRING)
def generate(
    schema_version: str,
    indent: int,
    json_schema_file: Optional[TextIO],
    model_type_name: str,
) -> None:
    schema_module = SCHEMA_VERSION_MODULES[schema_version]
    model_type = getattr(schema_module, model_type_name, None)
    if model_type is None or not issubclass(model_type, RootSchemaBaseModel):
        root_model_type_names = [
            model_type_name
            for model_type_name, model_type in inspect.getmembers(
                schema_module, inspect.isclass
            )
            if issubclass(model_type, RootSchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{model_type_name}' not in {root_model_type_names}", param_hint="MODEL"
        )
    json_schema_data = model_type.model_json_schema(by_alias=True)
    _remove_titles_inplace(json_schema_data)
    json_schema_str = json.dumps(json_schema_data, indent=indent)
    click.echo(message=json_schema_str, file=json_schema_file)


@cli.command(name="upgrade", help="Upgrade the specified model instance.")
@click.option(
    "--from-version",
    "from_schema_version",
    type=click.Choice(SCHEMA_VERSIONS),
    help="Schema version to upgrade from.",
)
@click.option(
    "--to-version",
    "to_schema_version",
    type=click.Choice(SCHEMA_VERSIONS),
    default=current_schema_module.VERSION,
    show_default=True,
    help="Schema version to upgrade to.",
)
@click.option(
    "--strict/--no-strict",
    "strict",
    default=None,
    show_default=True,
    help="Whether to raise an error on invalid fields.",
)
@click.option(
    "--indent",
    "indent",
    type=click.IntRange(min=0),
    default=2,
    show_default=True,
    help="JSON indentation level.",
    metavar="INTEGER",
)
@click.option(
    "-o",
    "output_model_instance_file",
    type=click.File("w"),
    help="Output data file.",
)
@click.argument("model_type_name", metavar="MODEL", type=click.STRING)
@click.argument("model_instance_file", metavar="FILE", type=click.File())
def upgrade(
    from_schema_version: Optional[str],
    to_schema_version: str,
    strict: Optional[bool],
    indent: int,
    output_model_instance_file: Optional[TextIO],
    model_type_name: str,
    model_instance_file: TextIO,
) -> None:
    model_data = json.load(model_instance_file)
    if from_schema_version is None:
        from_schema_version = guess_schema_version(model_data)
    from_schema_module = SCHEMA_VERSION_MODULES[from_schema_version]
    from_model_type = getattr(from_schema_module, model_type_name, None)
    if from_model_type is None or not isinstance(from_model_type, RootSchemaBaseModel):
        root_from_model_type_names = [
            model_type_name
            for model_type_name, model_type in inspect.getmembers(
                from_schema_module, inspect.isclass
            )
            if issubclass(model_type, RootSchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{model_type_name}' not in {root_from_model_type_names}",
            param_hint="MODEL",
        )
    to_schema_module = SCHEMA_VERSION_MODULES[to_schema_version]
    to_model_type = getattr(to_schema_module, model_type_name, None)
    if to_model_type is None or not isinstance(to_model_type, RootSchemaBaseModel):
        root_to_model_type_names = [
            model_type_name
            for model_type_name, model_type in inspect.getmembers(
                to_schema_module, inspect.isclass
            )
            if issubclass(model_type, RootSchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{model_type_name}' not in {root_to_model_type_names}", param_hint="MODEL"
        )
    model_instance = from_model_type.parse(model_data, strict=strict)
    upgraded_model_instance = to_model_type.upgrade(model_instance)
    upgraded_model_json = upgraded_model_instance.model_dump_json(
        indent=indent, by_alias=True
    )
    click.echo(message=upgraded_model_json, file=output_model_instance_file)


@cli.command(name="validate", help="Validate the specified model instance.")
@click.option(
    "--expect-version",
    "schema_version",
    type=click.Choice(SCHEMA_VERSIONS),
    default=current_schema_module.VERSION,
    show_default=True,
    help="Schema version to expect.",
)
@click.option(
    "--strict/--no-strict",
    "strict",
    default=None,
    show_default=True,
    help="Whether to raise an error on invalid fields.",
)
@click.argument("model_type_name", metavar="MODEL", type=click.STRING)
@click.argument("model_instance_file", metavar="FILE", type=click.File())
def validate(
    schema_version: Optional[str],
    strict: Optional[bool],
    model_type_name: str,
    model_instance_file: TextIO,
) -> None:
    model_data = json.load(model_instance_file)
    if schema_version is None:
        schema_version = guess_schema_version(model_data)
    schema_module = SCHEMA_VERSION_MODULES[schema_version]
    model_type = getattr(schema_module, model_type_name, None)
    if model_type is None or not issubclass(model_type, RootSchemaBaseModel):
        root_model_type_names = [
            model_type_name
            for model_type_name, model_type in inspect.getmembers(
                schema_module, inspect.isclass
            )
            if issubclass(model_type, RootSchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{model_type_name}' not in {root_model_type_names}", param_hint="MODEL"
        )
    model_type.parse(model_data, strict=strict)


def _remove_titles_inplace(*args) -> None:
    for arg in args:
        if isinstance(arg, dict):
            arg.pop("title", None)
            _remove_titles_inplace(*arg.values())
        elif isinstance(arg, list):
            _remove_titles_inplace(*arg)
