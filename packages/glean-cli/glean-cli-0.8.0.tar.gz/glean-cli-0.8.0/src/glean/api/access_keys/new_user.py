import click
from dataclasses import fields

from glean.api.access_keys.browser_auth import login_and_handle_query_params
from glean.api.access_keys.utils import (
    AccessKeyInfo,
    confirm_credentials_filepath,
    echo_horizontal_rule,
    save_access_key,
)
from glean.constants import GLEAN_BASE_URI


def create_account_and_access_key(credentials_filepath: str):
    """Creates a new account and project and saves a new access key.
    For authentication, opens a browser page that pushes them through
    our sign up flow.

    Args:
        credentials_filepath (str): Filepath to save access key to.
    """
    confirm_credentials_filepath(credentials_filepath)
    access_key_info = _get_new_account_access_key_info()
    save_access_key(credentials_filepath, access_key_info)
    echo_horizontal_rule()
    click.echo()
    click.echo(
        f"👋 Welcome {access_key_info.user_full_name}! We created a new Glean project for you."
    )
    click.echo()
    click.echo(
        f"{click.style('Go to the following link to set up a database connection:', bold=True)} {GLEAN_BASE_URI}/app/mb"
    )
    click.echo()


def _get_new_account_access_key_info() -> AccessKeyInfo:
    # Whether our request errored while finishing authentication.
    request_error = False

    # Access key info received from Glean's app server.
    access_key_info = None

    def qp_handler(query_params: dict) -> str:
        nonlocal request_error
        nonlocal access_key_info

        if any(
            map(
                lambda field: query_params.get(field.name, None) is None,
                fields(AccessKeyInfo),
            )
        ):
            request_error = True
            return f"{GLEAN_BASE_URI}/cliAuthConfirmation/error"

        access_key_info = AccessKeyInfo(**query_params)
        return f"{GLEAN_BASE_URI}/cliAuthConfirmation/success/newUser?userFullName={access_key_info.user_full_name}"

    login_and_handle_query_params(qp_handler, True)

    # If encountered error while handling request, raise an exception.
    if request_error:
        raise click.ClickException(
            "Unknown error while finishing authentication. Please try again."
        )

    return access_key_info
