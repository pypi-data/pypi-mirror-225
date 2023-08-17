import json

import click

from patch.auth.auth_client import AuthClient
from patch.auth.auth_token import global_access_token
from patch.cli.commands import pass_obj, with_as_tenant

from patch.cli.styled import StyledGroup, StyledCommand

from rich import box
from rich.table import Table

from patch.cli.tools.filters_reader import filters_to_claims
from patch.cli.tools.json_reader import read_json


@click.group(cls=StyledGroup, help='Commands related to accessing data',
             hidden=not global_access_token.has_token())
@click.pass_context
def access(_ctx, ):
    pass


@access.command(cls=StyledCommand, help='Get a Patch API access token',
                hidden=not global_access_token.has_token())
@pass_obj()
def token(patch_ctx):
    console = patch_ctx.console
    auth_client = AuthClient(patch_ctx)
    access_token = auth_client.get_access_token()
    if not access_token:
        console.print("[red]Error[/red] You need to log-in!")
        patch_ctx.exit(1)
    else:
        click.echo(access_token)


@access.group(cls=StyledGroup, name='signing-template', help='Commands related to custom signing templates')
def signing_spec():
    pass


def validate_jwk(jwk_file):
    jwk = read_json(jwk_file, Exception)
    if not jwk.get('kid', None):
        raise Exception('JWK file has no key ID (kid)')
    return json.dumps(jwk)


@signing_spec.command(cls=StyledCommand, help='Create a new custom signing template')
@click.argument('name', type=click.STRING)
@click.argument('jwk', type=click.File(mode='r'))
@click.option('-s', '--source', type=click.STRING, help='Source ID')
@click.option('-d', '--dataset', type=click.STRING, help='Dataset name')
@click.option('-f', '--filter', 'auth_filter', type=str, help='Filter of the authorization scope for JWTs',
              multiple=True)
@with_as_tenant()
@pass_obj()
def create(patch_ctx, name, jwk, source, dataset, auth_filter):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    jwk_json = validate_jwk(jwk)
    gql_mutation = client.prepare_mutation('createCustomSigningTemplate', input={
        'name': name,
        'jwk': jwk_json,
        'sourceId': source,
        'datasetName': dataset,
        'filters': filters_to_claims(auth_filter)
    })
    gql_mutation.execute()
    console.print(f"[green]Signing template created[/green]")


@signing_spec.command(cls=StyledCommand, help='Delete custom signing template')
@click.argument('signing_id', type=click.STRING)
@with_as_tenant()
@pass_obj()
def delete(patch_ctx, signing_id):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    gql_mutation = client.prepare_mutation('deleteCustomSigningTemplate', input={
        'customSigningTemplateId': signing_id
    })
    gql_mutation.execute()
    console.print(f"[green]Signing template has been deleted[/green]")


def render_specs(specs):
    table = Table(title="Signing Templates", box=box.ROUNDED, border_style="grey37")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("ID", justify="left", style="yellow", no_wrap=True)
    table.add_column("Key ID", justify="left", style="yellow", no_wrap=True)
    table.add_column("Scope", justify="left", style="white", no_wrap=True)
    for spec in specs:
        scope = []
        kids = []
        for jwk in spec.jwks:
            kids.append(jwk.kid)
        if spec.sourceId:
            scope.append(f"Source ID: [yellow]{spec.sourceId}[/yellow]")
        if spec.datasetName:
            scope.append(f"Dataset name: [yellow]{spec.datasetName}[/yellow]")
        for f in spec.filters:
            scope.append(
                f"Table: [yellow]{f.tableName}[/yellow], "
                f"column: [yellow]{f.columnName}[/yellow], "
                f"value: [yellow]{f.value}[/yellow]")
        if not scope:
            rendered_scope = "[dim](No constraints)[/dim]"
        else:
            rendered_scope = "\n".join(scope)
        table.add_row(spec.name, spec.id, "\n".join(kids), rendered_scope)
    return table


@signing_spec.command(cls=StyledCommand, help='List of custom signing templates')
@with_as_tenant()
@pass_obj()
def ls(patch_ctx):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    gql_query = client.prepare_query('listCustomSigningTemplates')
    result = gql_query.execute()
    if not result:
        console.print(f"No signing templates")
    else:
        table = render_specs(result)
        console.print(table)
