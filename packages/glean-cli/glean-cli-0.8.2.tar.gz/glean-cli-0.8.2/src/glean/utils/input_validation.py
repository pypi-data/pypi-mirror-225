import click
from typing import Optional


def prompt_and_validate_value_length(
    prompt: str, value_name: str, value_length_limit: Optional[int] = 100
):
    value = ""
    while True:
        value = click.prompt(prompt, type=str).strip()
        if len(value) <= value_length_limit:
            return value

        error_message = (
            f"{value_name} must be {value_length_limit} characters or fewer."
        )
        click.secho(error_message, fg="red", bold=True)
