import click
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, Optional
from urllib.parse import urlparse, parse_qs, urlencode
import webbrowser

from glean.constants import GLEAN_BASE_URI, GLEAN_DEBUG

# A handler for query params consumed a dict of processed query params
# and returns a redirect URL.
QueryParamsHandler = Callable[[dict], str]


def login_and_handle_query_params(
    handle_get_query_params: QueryParamsHandler,
    is_new_user: bool,
    intended_project_id: Optional[str] = None,
):
    """Opens a browser page where the user can sign up or login depending
    on the value of `is_new_user`. When sign up or login finishes, Hashboard's
    app server creates a new access key for the user (as well as an account and
    project if the user is signing up).

    To receive information back from this browser page about the newly created
    access key (and potentially account and project), this function spins up a
    local HTTP server that listens for GET requests. Hashboard's app server makes
    a GET request to this local server using query params to pass information
    about the created access key back to the CLI client. `handle_get_query_params`
    is a callback that consumes the query params as a dictionary and returns a
    final redirect URL to send the user's browser page to.

    Args:
        handle_get_query_params (QueryParamsHandler): Callback that consumes query params dict and returns a redirect URL.
        is_new_user (bool): Whether this flow is for a new user. If so, restricts to sign up. Otherwise, restricts to login.
        intended_project_id (Optional[str]): Project ID to create a new access key for. Only applies to existing users
          (`is_new_user = False`). Defaults to None.
    """
    # `0` instructs Python to find any available port.
    server_address = ("localhost", 0)
    # HTTPServer requires a class, so we create a class object with
    # the passed `handle_get_query_params` injected.
    CustomCallbackHandler = type(
        "CustomCallbackHandler",
        (CallbackHandler,),
        # Python calls this function as if it's a class member, so we
        # wrap `handle_get_query_params` in a function that consumes `self`.
        {"handle_get_query_params": lambda self, qp: handle_get_query_params(qp)},
    )
    httpd = HTTPServer(server_address, CustomCallbackHandler)

    redirect_url = f"http://localhost:{httpd.server_port}"
    query_params_dict = {"cli-auth-server-host": redirect_url}
    if is_new_user:
        login_url = f"{GLEAN_BASE_URI}/cliAuthConfirmation/entry/newUser?{urlencode(query_params_dict)}"
    else:
        if intended_project_id:
            query_params_dict["cli-auth-project-id"] = intended_project_id
        login_url = f"{GLEAN_BASE_URI}/auth/login?{urlencode(query_params_dict)}"

    click.echo("🚀 Launching login page in your browser...")
    click.echo(
        "If this isn't showing up, copy and paste the following URL into your browser:"
    )
    click.echo()
    click.echo(login_url)
    click.echo()

    # Open login URL in browser.
    webbrowser.open_new(login_url)

    # Wait for our server to handle redirect.
    httpd.handle_request()


class CallbackHandler(BaseHTTPRequestHandler):
    """Class that handles requests to the local HTTP server that
    `login_and_handle_query_params` spins up.
    """

    def __init__(
        self, *args, handle_get_query_params: QueryParamsHandler = None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.handle_get_query_params = handle_get_query_params

    def do_GET(self):
        """Parses query params, hands them off to `handle_get_query_params`,
        and redirects to the returned URL.
        """
        query = urlparse(self.path).query
        query_params_dict = {key: value[0] for key, value in parse_qs(query).items()}
        redirect_url = self.handle_get_query_params(query_params_dict)
        self.send_response(302)
        self.send_header("Location", redirect_url)
        self.end_headers()
        return

    def log_message(self, *args):
        """Disables logging in the CLI, which we don't want to expose to the user
        unless in debug mode.
        """
        if GLEAN_DEBUG:
            super().log_message(*args)
