import click

from patch.auth.auth_forms import AuthForm
from patch.auth.auth_token import global_access_token
from patch.cli.phone_number_param_type import PhoneNumberParamType
from patch.cli.styled import StyledCommand
from patch.cli.commands import pass_obj
from patch.cli import PatchClickContext
from patch.cli.tools.state.auth_state_transfer import AuthStateTransfer

TIMEOUT_MINUTES = 5


def login_sso(patch_ctx: PatchClickContext, sso):
    console = patch_ctx.console
    [domain, app_id] = sso.split(":")

    state_transfer = AuthStateTransfer(patch_ctx, '/v1/auth/login/sso', '/v1/auth/login/sso/poll')
    state_transfer.call_for_state_transfer({'domain': domain, 'app': app_id})
    redirect_url = state_transfer.get_redirect_url()

    result = click.launch(redirect_url)
    if result != 0:
        console.print(f"Now, open [magenta]{redirect_url}[/magenta]")
    else:
        console.print(f"If a tab hasn't opened already, load this URL in your browser: "
                      f"[magenta]{redirect_url}[/magenta]")

    console.print(
        f"\n [magenta]Important![/magenta] Please don't terminate this CLI until the login process is done!\n")
    try:
        returned_state = state_transfer.poll_for_state(TIMEOUT_MINUTES)
        access_token = returned_state.get('access-token')
        refresh_token = returned_state.get('refresh-token')
        if access_token:
            global_access_token.store(access_token, refresh_token)
            console.print(f"\n[green]Login successful![/green]\nYou can now start using your Patch account!")
            console.print("Let's start with [magenta]pat source ls[/magenta]")
        else:
            console.print("Something went wrong! Please try again. If no luck, please reach out to your Patch contact.")
    except TimeoutError:
        console.print(f"The authentication attempt timed out. Please try again.")


@click.command(cls=StyledCommand, help='Login to Patch using your mobile phone or email')
@click.argument('depreciated_phone', required=False, type=PhoneNumberParamType())
@click.option('--email', help='Login to Patch using your email', type=click.STRING)
@click.option('--phone', help='Login to Patch using your mobile phone', type=PhoneNumberParamType())
@click.option('--sso', help='Log in using SSO', )
@pass_obj()
def login(patch_ctx: PatchClickContext, email, phone, depreciated_phone, sso):
    console = patch_ctx.console
    if sso:
        login_sso(patch_ctx, sso)
    elif email:
        auth = AuthForm(patch_ctx, email, "email")
        auth.request_validation()
    elif phone:
        auth = AuthForm(patch_ctx, phone, "sms")
        auth.request_validation()
    elif depreciated_phone:
        auth = AuthForm(patch_ctx, depreciated_phone, "sms")
        auth.request_validation()
        console.print(
            "[yellow]Warning: This method of login is depreciated. Please use --phone to login with " +
            "a phone number or --email to login with email[/yellow]")
    else:
        console.print("[red]Error: Please login with phone number (--phone) or email (--email)[/red]")
