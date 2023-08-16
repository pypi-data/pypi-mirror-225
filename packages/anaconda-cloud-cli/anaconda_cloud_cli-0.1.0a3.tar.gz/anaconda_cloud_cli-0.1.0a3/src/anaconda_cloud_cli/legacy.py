"""Wrappers and functions to handle loading of legacy anaconda-client subcommands into the new CLI.

A one-stop-shop for maintaining compatibility and helping to gracefully migrate & deprecate.

"""
import logging
import sys
from argparse import ArgumentParser
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Set

import typer as typer
from binstar_client import commands as command_module
from binstar_client.scripts.cli import main as binstar_main
from clyent import add_subparser_modules
from typer import Typer

log = logging.getLogger(__name__)

# All subcommands in anaconda-client
LEGACY_SUBCOMMANDS = {
    "auth",
    "label",
    "channel",
    "config",
    "copy",
    "download",
    "groups",
    "login",
    "logout",
    "move",
    "notebook",
    "package",
    "remove",
    "search",
    "show",
    "update",
    "upload",
    "whoami",
}
# These subcommands will be shown in the top-level help
NON_HIDDEN_SUBCOMMANDS = {"upload"}
# Any subcommands that should emit deprecation warnings, and show as deprecated in the help
DEPRECATED_SUBCOMMANDS: Set[str] = set()


def _get_help_text(parser: ArgumentParser, name: str) -> str:
    """Extract the help text from the anaconda-client CLI Argument Parser."""
    if parser._subparsers is None:
        return ""
    if parser._subparsers._actions is None:
        return ""
    if parser._subparsers._actions[1].choices is None:
        return ""
    subcommand_parser = dict(parser._subparsers._actions[1].choices).get(name)
    if subcommand_parser is None:
        return ""
    description = subcommand_parser.description
    if description is None:
        return ""
    return description.strip()


def load_legacy_subcommands(app: Typer) -> None:
    """Load each of the legacy subcommands into its own typer subcommand.

    This allows them to be called from the new CLI, without having to manually migrate.
    """

    parser = ArgumentParser()
    add_subparser_modules(parser, command_module)

    dot_org_app = Typer(
        name="org", help="Interact with the anaconda.org API", no_args_is_help=True
    )
    app.add_typer(dot_org_app)
    for name in LEGACY_SUBCOMMANDS:

        def subcommand_function(ctx: typer.Context) -> None:
            # Here, we are using the ctx instead of sys.argv because the test invoker doesn't
            # use sys.argv
            args = []
            if ctx.info_name is not None:
                args.append(ctx.info_name)
            args.extend(ctx.args)
            legacy_main(args=args)

        # TODO: Can we load the arguments, or at least the docstring to make the help nicer?
        help_text = _get_help_text(parser, name)
        dot_org_app.command(
            name=name,
            help=help_text,
            context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
        )(subcommand_function)

        # Mount the legacy CLI subcommands at the top-level, but emit a deprecation warning
        if name not in {"login", "logout"}:
            help_text = f"anaconda.org: {help_text + ' ' if help_text else ''}(alias for 'anaconda org {name}')"
            if name in DEPRECATED_SUBCOMMANDS:
                help_text = f"(deprecated) {help_text}"
            app.command(
                name=name,
                help=help_text,
                hidden=name not in NON_HIDDEN_SUBCOMMANDS,
                context_settings={
                    "allow_extra_args": True,
                    "ignore_unknown_options": True,
                },
            )(_deprecate(name, subcommand_function))


def _deprecate(name: str, f: Callable) -> Callable:
    def new_f(ctx: typer.Context) -> Any:
        if name in DEPRECATED_SUBCOMMANDS:
            log.warning(
                "The existing anaconda-client commands will be deprecated. To maintain compatibility, "
                "please either pin `anaconda-client<2` or update your system call with the `org` prefix, "
                f'e.g. "anaconda org {name} ..."'
            )
        return f(ctx)

    return new_f


def legacy_main(args: Optional[List[str]] = None) -> None:
    binstar_main(args if args is not None else sys.argv[1:], allow_plugin_main=False)
