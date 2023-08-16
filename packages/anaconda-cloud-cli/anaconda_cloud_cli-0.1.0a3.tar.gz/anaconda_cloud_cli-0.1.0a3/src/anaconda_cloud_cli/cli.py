import logging
from typing import Optional

import typer
from rich.prompt import Confirm
from rich.prompt import Prompt

from anaconda_cli_base import console
from anaconda_cli_base.console import select_from_list
from anaconda_cloud_auth import login
from anaconda_cloud_auth import logout
from anaconda_cloud_auth.config import AuthConfig
from anaconda_cloud_auth.exceptions import TokenNotFoundError
from anaconda_cloud_auth.token import TokenInfo

from anaconda_cloud_cli.legacy import legacy_main
from anaconda_cloud_cli.legacy import load_legacy_subcommands

log = logging.getLogger(__name__)

# We need to keep this as a placeholder to register as a subcommand plugin for
# the `anaconda-cli-base` package. However, we want to attach the login and
# logout commands to the main CLI app.
app = typer.Typer(add_completion=False, name="cloud", hidden=True)

# We need to place this down here to prevent circular import
from anaconda_cli_base.cli import app as main_app  # noqa: E402

load_legacy_subcommands(main_app)


@main_app.command(
    name="login",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def auth_login(
    ctx: typer.Context,
    domain: Optional[str] = typer.Option(None),
    basic: bool = typer.Option(False, help="Deprecated"),
    force: bool = typer.Option(False),
) -> None:
    """Login to your Anaconda account."""
    if domain is None:
        if any(opt in ctx.args for opt in {"--username", "--hostname", "--password"}):
            domain = "anaconda.org"
        else:
            domain = select_from_list(
                prompt="Please select login domain:",
                choices=["anaconda.cloud", "anaconda.org"],
            )

    if domain == "anaconda.org":
        # We would like to strip off all arguments & options that are part of the typer
        # specification, but allow passing the rest into the legacy_main entrypoint.
        # This is done using the ctx.args, in combination with the context_settings
        # in the decorator above.
        # See: https://typer.tiangolo.com/tutorial/commands/context/#configuring-the-context
        name = ctx.command.name
        assert name is not None
        legacy_main(args=[name, *ctx.args])
        raise typer.Exit()

    try:
        auth_domain = AuthConfig().domain
        expired = TokenInfo.load(domain=auth_domain).expired
        if expired:
            console.print("Your API key has expired, logging into Anaconda.cloud")
            login(basic=basic, force=True)
            raise typer.Exit()
    except TokenNotFoundError:
        pass  # Proceed to login
    else:
        force_login = force or Confirm.ask(
            "You are already logged into Anaconda Cloud. Would you like to force a new login?",
            default=False,
        )
        if not force_login:
            raise typer.Exit()
    login(basic=basic, force=True)
    console.print("Successfully logged into Anaconda Cloud", style="green")


@main_app.command(name="logout")
def auth_logout() -> None:
    """Logout of your Anaconda account."""
    domain = Prompt.ask(
        "Please choose which domain to logout from:",
        choices=["anaconda.cloud", "anaconda.org", "all"],
        default="all",
    )

    if domain == "anaconda.org" or domain == "all":
        legacy_main()

    if domain == "anaconda.cloud" or domain == "all":
        logout()
        console.print("Successfully logged out of Anaconda Cloud", style="green")
