from __future__ import annotations

import pytest

from anaconda_cloud_cli.legacy import LEGACY_SUBCOMMANDS

from .conftest import CLIInvoker


def test_auth_subcommand_help(invoke_cli: CLIInvoker) -> None:
    """Auth is available as a subcommand of the core CLI app since it is a dependency and provides a plugin."""
    result = invoke_cli("auth", "--help")
    assert result.exit_code == 0


@pytest.mark.parametrize("name", set(LEGACY_SUBCOMMANDS) - {"login", "logout"})
def test_anaconda_client_subcommand_top_level(
    invoke_cli: CLIInvoker, name: str
) -> None:
    """We mount anaconda-client subcommands at the top-level, except login & logout."""
    result = invoke_cli(name, "-h")
    assert result.exit_code == 0


@pytest.mark.parametrize("name", set(LEGACY_SUBCOMMANDS) - {"login", "logout"})
def test_anaconda_client_subcommand_nested(invoke_cli: CLIInvoker, name: str) -> None:
    """We mount all anaconda-client subcommands under the "org" namespace."""
    result = invoke_cli("org", name, "-h")
    assert result.exit_code == 0
