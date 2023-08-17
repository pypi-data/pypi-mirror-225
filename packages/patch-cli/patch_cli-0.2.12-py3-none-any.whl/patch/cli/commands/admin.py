import click
from rich import box
from rich.emoji import EMOJI
from rich.table import Table

from patch.auth.auth_token import global_is_admin_or_mta
from patch.cli import PatchClickContext
from patch.cli.commands import active_source, pass_obj, with_as_tenant
from patch.cli.styled import StyledGroup, StyledCommand
from patch.cli.tools.tables.renders import render_number
from rich.prompt import Confirm


def render_user(tenant_user):
    segments = [_c('ID', 'yellow', tenant_user.id),
                _c('Name', 'cyan', tenant_user.fullName),
                _c('Login', 'magenta', tenant_user.login)]
    logged_in = EMOJI['green_circle'] + ' ' if tenant_user.loggedIn else ''
    return logged_in + ', '.join([s for s in segments if s is not None])


suffix_pow_map = {
    'K': 1,
    'M': 2,
    'G': 3,
    'T': 4,
}


def parse_quota(value):
    if value:
        value = value.upper()
    if value.endswith('B'):
        value = value[:-1]
    multiplier = 2  # default: in megabytes
    if value:
        multiplier_candidate = suffix_pow_map.get(value[-1], None)
        if multiplier_candidate:
            value = value[:-1]
            multiplier = multiplier_candidate
    else:
        raise Exception('Quota value is too short. Examples of valid quota: 12 MB or 2GB.')
    try:
        return int(value) * 1024 ** multiplier
    except ValueError:
        raise Exception('Quota has invalid value. Examples of valid quota: 12 MB or 2GB.')


@click.group(cls=StyledGroup, help='Admin commands', hidden=not global_is_admin_or_mta)
def admin():
    pass


@admin.group(cls=StyledGroup, help='Manage users')
def user():
    pass


@user.command(cls=StyledCommand, help='Register user by phone/email')
@click.argument('name', type=click.STRING)
@click.option('--phone', type=click.STRING)
@click.option('--email', type=click.STRING)
@click.option('-t', '--tenant-id', help='Tenant ID')
@pass_obj()
def register(patch_ctx: PatchClickContext, phone, email, tenant_id, name):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    input_arg = {'phone': phone, 'email': email, 'isMultiTenant': False, 'fullName': name, 'tenantId': tenant_id}
    mut = client.prepare_mutation('registerUser', input=input_arg)
    result = mut.execute()
    console.print(f"Added user [green]{result.login}[/green], ID: [green]{result.id}[/green], "
                  f"Tenant: [magenta]{result.tenantId}[/magenta]")


@user.command(cls=StyledCommand, help='Unregister user by ID')
@click.argument('user_id', metavar='ID', type=click.STRING)
@pass_obj()
def unregister(patch_ctx: PatchClickContext, user_id):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    query_user = client.prepare_query('user', id=user_id)
    user_to_unregister = query_user.execute()
    confirmation = Confirm.ask(f"You are about to remove user {render_user(user_to_unregister)}. Proceed? ",
                               console=console)
    if confirmation:
        mut = client.prepare_mutation('unregisterUser', input={'userId': user_id})
        result = mut.execute()
        console.print(f"Unregistered user: [green]{result.login}[/green]")
    else:
        console.print(f"Command [red]aborted[/red]")


@user.command(cls=StyledCommand, help='Rename user')
@click.argument('tenant_id', metavar='ID', type=click.STRING)
@click.argument('name', type=click.STRING)
@pass_obj()
def rename(patch_ctx: PatchClickContext, tenant_id, name):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    mut = client.prepare_mutation('updateUser', input={'userId': tenant_id, 'fullName': name})
    result = mut.execute()
    console.print(f"Renamed user: [green]{result.login}[/green] [cyan]{result.fullName}[/cyan]")


@admin.group(cls=StyledGroup, help='Manage tenants')
def tenant():
    pass


def _c(prefix, color, text):
    if text is not None:
        return f"{prefix}: [{color}]{text}[/{color}]"


@tenant.command(cls=StyledCommand, help='List tenants')
@pass_obj()
def ls(patch_ctx: PatchClickContext):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    q = client.prepare_query('getTenants')
    tenants = q.execute()
    table = Table(title="Tenants", box=box.ROUNDED, border_style="grey37")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("ID", justify="left", style="yellow", no_wrap=True)
    table.add_column("Quota", justify="left", style="white", no_wrap=True)
    table.add_column("Users", justify="left", style="white", no_wrap=True)
    for tenant_elem in tenants:
        users = []
        for tenant_user in tenant_elem.users:
            users.append(render_user(tenant_user))
        quota_desc = ''
        if tenant_elem.quota:
            used = tenant_elem.quotaUsed or 0
            usage = used / tenant_elem.quota
            quota_str = render_number(tenant_elem.quota, 1024, ['', 'KB', 'MB', 'GB', 'TB'])
            quota_desc = f"{quota_str}, {usage:.0%}"
        table.add_row(tenant_elem.name, tenant_elem.id, quota_desc, "\n".join(users))
    console.print(table)


@tenant.command(cls=StyledCommand, help='Rename Tenant')
@click.argument('tenant_id', metavar='ID', type=click.STRING)
@click.argument('name', type=click.STRING)
@pass_obj()
def rename(patch_ctx: PatchClickContext, tenant_id, name):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    mut = client.prepare_mutation('updateTenant', input={'tenantId': tenant_id, 'name': name})
    result = mut.execute()
    console.print(f"Renamed tenant: [green]{result.id}[/green] [cyan]{result.name}[/cyan]")


@tenant.command(cls=StyledCommand, help='Create Tenant')
@click.argument('name', type=click.STRING)
@click.option('-q', '--quota', help='Tenant quota')
@pass_obj()
def create(patch_ctx: PatchClickContext, name, quota):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    mutation_input = {'name': name}
    if quota:
        mutation_input['quota'] = parse_quota(quota)
    mut = client.prepare_mutation('createTenant', input=mutation_input)
    result = mut.execute()
    console.print(f"Created tenant: [green]{result.id}[/green] [cyan]{result.name}[/cyan]")


@tenant.command(cls=StyledCommand, help='Delete Tenant')
@click.argument('tenant_id', metavar='ID', type=click.STRING)
@pass_obj()
def delete(patch_ctx: PatchClickContext, tenant_id):
    console = patch_ctx.console
    confirmation = Confirm.ask(f"You are about to delete tenant [cyan]{tenant_id}[/cyan]. Proceed? ", console=console)
    if confirmation:
        client = patch_ctx.gql_client
        mut = client.prepare_mutation('deleteTenant', input={'tenantId': tenant_id})
        mut.execute()
        console.print(f"Deleted tenant: [green]{tenant_id}[/green]")
    else:
        console.print(f"Command [red]aborted[/red]")


@tenant.command(cls=StyledCommand, name='update-quota', help='Update tenant quota')
@click.argument('tenant_id', metavar='ID', type=click.STRING)
@click.argument('quota', type=click.STRING)
@pass_obj()
def update_quota(patch_ctx: PatchClickContext, tenant_id, quota):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    quota_bytes = parse_quota(quota)
    mut = client.prepare_mutation('updateTenant', input={'tenantId': tenant_id, 'quota': quota_bytes})
    result = mut.execute()
    quota_str = render_number(quota_bytes, 1024, ['', 'KB', 'MB', 'GB', 'TB'])
    console.print(f"Change tenant quota: [green]{result.id}[/green] [cyan]{quota_str}[/cyan]")


@admin.group(cls=StyledGroup, help='Manage datasets')
def dataset():
    pass


@dataset.command(cls=StyledCommand, help='Schedule immediate run for dataset on current source.')
@click.option('-n', '--dataset_name')
@click.option('-i', '--dataset_id')
@click.option('-t', '--table_name')
@with_as_tenant()
@pass_obj()
def sync(patch_ctx: PatchClickContext, dataset_name, dataset_id, table_name):
    console = patch_ctx.console
    if dataset_name and dataset_id:
        console.print(f"[red]Provide only one of dataset_name or dataset_id[/red]")
        return
    with active_source(patch_ctx) as local_state:
        source_id = local_state.active_source_id
        client = patch_ctx.gql_client
        mutation_input = {
            'sourceId': source_id,
        }
        if dataset_id:
            mutation_input['datasetId'] = dataset_id
        elif dataset_name:
            mutation_input['datasetName'] = dataset_name
        if table_name:
            mutation_input['tableName'] = table_name

        gql_mutation = client.prepare_mutation('syncDataset', input=mutation_input)
        gql_mutation.execute()
        console.print(f"[green]Dataset queued for sync[/green]")
