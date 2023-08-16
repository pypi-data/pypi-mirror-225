from enum import Enum
from typing import List, Optional

import typer

from neosctl.services.gateway import entity, schema

app = typer.Typer(name="output")


def _output_url(ctx: typer.Context) -> str:
    return "{}/v2/output".format(ctx.obj.get_gateway_api_url().rstrip("/"))


arg_generator = entity.EntityArgGenerator("Output")


class OutputType(Enum):
    """Output type."""

    application = "application"
    dashboard = "dashboard"


@app.command(name="create")
def create_entity(
    ctx: typer.Context,
    label: str = arg_generator.label,
    name: str = arg_generator.name,
    description: str = arg_generator.description,
    output_type: OutputType = typer.Argument(OutputType.application, help="Output type"),
    owner: Optional[str] = arg_generator.owner_optional,
    contacts: List[str] = arg_generator.contacts,
    links: List[str] = arg_generator.links,
) -> None:
    """Create output."""
    entity_schema = schema.CreateOutput(
        name=name,
        label=label,
        description=description,
        output_type=output_type.value,
    )

    entity.create_entity(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        label=label,
        name=name,
        description=description,
        owner=owner,
        contacts=contacts,
        links=links,
        entity_schema=entity_schema,
    )


@app.command(name="list")
def list_entities(ctx: typer.Context) -> None:
    """List outputs."""
    entity.list_entities(ctx=ctx, url_prefix=_output_url(ctx=ctx))


@app.command(name="get")
def get_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Get output."""
    entity.get_entity(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="delete")
def delete_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Delete output."""
    entity.delete_entity(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="get-info")
def get_entity_info(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Get output info."""
    entity.get_entity_info(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="update")
def update_entity(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    label: str = arg_generator.label,
    name: str = arg_generator.name,
    description: str = arg_generator.description,
    output_type: OutputType = typer.Argument(OutputType.application, help="Output type"),
) -> None:
    """Update output."""
    entity_schema = schema.CreateOutput(
        name=name,
        label=label,
        description=description,
        output_type=output_type.value,
    )

    entity.update_entity(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        identifier=identifier,
        label=label,
        name=name,
        description=description,
        entity_schema=entity_schema,
    )


@app.command(name="update-info")
def update_entity_info(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    owner: str = arg_generator.owner,
    contacts: List[str] = arg_generator.contacts,
    links: List[str] = arg_generator.links,
) -> None:
    """Update output info."""
    entity.update_entity_info(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        identifier=identifier,
        owner=owner,
        contacts=contacts,
        links=links,
    )


@app.command(name="get-journal")
def get_entity_journal(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Get output journal."""
    entity.get_entity_journal(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        identifier=identifier,
    )


@app.command(name="update-journal")
def update_entity_journal(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
    note: str = arg_generator.note,
) -> None:
    """Update output journal."""
    entity.update_entity_journal(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        identifier=identifier,
        note=note,
    )


@app.command(name="get-links")
def get_entity_links(
    ctx: typer.Context,
    identifier: str = arg_generator.identifier,
) -> None:
    """Get output links."""
    entity.get_entity_links(
        ctx=ctx,
        url_prefix=_output_url(ctx=ctx),
        identifier=identifier,
    )
