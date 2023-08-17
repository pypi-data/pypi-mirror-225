from os.path import exists
from typing import Set

import click

from rastless.db.models import LayerStepModel


def validate_filenames_exists(filenames: Set[str]):
    filename_errors = []

    for filename in filenames:
        if not exists(filename):
            filename_errors.append(filename)

    filename_errors_str = "\n".join(filename_errors)

    if filename_errors:
        click.echo(f"Filenames could not be found:\n{filename_errors_str}")
        raise click.Abort()


def validate_layer_step_override(layer_step: LayerStepModel, append: bool, override: bool) -> bool:
    if layer_step and not append and not override:
        click.confirm(
            f"Layer step {layer_step.datetime} with layer id {layer_step.layer_id} already exists."
            f" Do yo want to override the layer step and delete all associated data?",
            abort=True)
        override = True

    if append and override:
        click.echo("You can either append data to a layer step or override the complete layer step. "
                   "Existing filenames will be overridden automatically on append.")
        raise click.Abort()

    if (not layer_step and append) or (not layer_step and override):
        click.echo(f"Layer step {layer_step.datetime} is not existing. Layer step will be created.")

    return override


def validate_input_with_append(sensor, append):
    if not append and not sensor:
        click.echo("Sensor needs to be define if timestep wil be created")
        raise click.Abort()
