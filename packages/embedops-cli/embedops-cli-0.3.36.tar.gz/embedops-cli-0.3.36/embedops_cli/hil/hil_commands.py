"""
Contains functions for the HIL sub-group commands.
"""

import json
import click
from embedops_cli.eo_types import (
    NoRepoIdException,
    NetworkException,
    LoginFailureException,
)
from embedops_cli.hil.hil_types import HILRepoId404Exception
from embedops_cli.sse.sse_api import SSEApi
from embedops_cli.sse import eo_sse
from embedops_cli.utilities import echo_error_and_fix
from embedops_cli import config
from embedops_cli.hil.hil_common import hil_run


@click.command()
@click.pass_context
def blink(ctx: click.Context):

    """Get a streaming response for the given event feed using urllib3."""

    try:

        repo_id = config.get_repo_id()

        if not repo_id:
            raise NoRepoIdException()

        sse_api = SSEApi()
        for event in sse_api.sse_blink_gateway(repo_id):
            if event.event == eo_sse.SSE_TEXT_EVENT:
                eo_sse.sse_print_command_text(event)
            elif event.event == eo_sse.SSE_RESULT_EVENT:
                result_event_obj = json.loads(event.data)
                ctx.exit(result_event_obj["exitCode"])
            else:
                pass  # Just ignore

        # If the command hasn't returned anything yet, exit here
        ctx.exit(2)

    except NoRepoIdException as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)
    except NetworkException as exc:
        if exc.status_code == 401:
            echo_error_and_fix(LoginFailureException())
        elif exc.status_code == 404:
            echo_error_and_fix(HILRepoId404Exception())
        else:
            echo_error_and_fix(exc)

        ctx.exit(2)


@click.command()
@click.pass_context
def run(ctx: click.Context):

    """Run hil in local mode, using the current repository as a source."""

    ctx.exit(hil_run(local=True))
