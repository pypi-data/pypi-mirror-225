import click
import simplejson

from rastless.commands import layers
from rastless.config import Cfg
from rastless.core.s3 import delete_layer_step_files
from rastless.core.schemas import CompressionTypes
from rastless.core.validate import validate_filenames_exists, validate_input_with_append
from rastless.db.base import str_uuid
from rastless.db.models import LayerModel, PermissionModel


@click.command()
@click.pass_obj
@click.option("-cl", "--client", required=True, type=str, help="Define frontend client, which consumes the layers")
@click.option("-pr", "--product", required=True, type=str, help="Product abbreviation e.g tur, sdb")
@click.option("-t", "--title", required=True, type=str, help="Title which is displayed in the frontend")
@click.option("-id", "--layer-id", default=str_uuid, type=str, help="Predefined uuid otherwise self generated")
@click.option("-cm", "--colormap", type=str, help="SLD colormap name")
@click.option("-u", "--unit", type=str, help="Unit abbreviation e.g. m or FTU")
@click.option("-b", "--background-id", type=str, help="Layer uuid of the background layer")
@click.option("-d", "--description", type=str, help="Description to better identify the layer")
@click.option("-r", "--region-id", default=1, type=int, help="Region ID of api-layer service")
@click.option("-p", "--permissions", type=str, multiple=True,
              help="Keycloak role permissions in the following form: User -> user#<unique username>"
                   " e.g. user#siegmann@eomap.de, Role -> role#<keycloak client>:<client role>"
                   " e.g. role#hypos:full-access")
def create_layer(cfg: Cfg, permissions, **kwargs):
    """Create layer. This has to be done before adding timesteps"""
    layer = LayerModel.parse_obj(kwargs)
    cfg.db.add_layer(layer)

    permission_models = [PermissionModel(permission=permission, layer_id=layer.layer_id) for permission in permissions]
    cfg.db.add_permissions(permission_models)

    click.echo(f"Created layer with id: {layer.layer_id}")
    return layer.layer_id


@click.command()
@click.pass_obj
@click.option("-f", "--filenames", type=str, help="Filename paths ", multiple=True, required=True)
@click.option("-d", "--datetime", required=True, type=str, help="Admission date")
@click.option("-s", "--sensor", type=str, help="Sensor e.g. SENT2")
@click.option("-l", "--layer-id", required=True, type=str, help="Created layer uuid")
@click.option("-t", "--temporal-resolution", default="daily", type=str, help="Temporal resolution e.g. daily, monthly")
@click.option("-p", "--profile", type=click.Choice([CompressionTypes.DEFLATE.value, CompressionTypes.WEBP.value]),
              default=CompressionTypes.DEFLATE.value,
              help="Compression of the GeoTiff")
@click.option("-a", "--append", is_flag=True)
@click.option("-o", "--override", is_flag=True)
def create_timestep(cfg: Cfg, filenames, append, datetime, sensor, layer_id, temporal_resolution, profile,
                    override):
    """Create timestep entry and upload layer to S3 bucket"""
    filenames = set(filenames)
    validate_filenames_exists(filenames)
    validate_input_with_append(sensor, append)

    layers.create_timestep(cfg, filenames, append, datetime, sensor, layer_id, temporal_resolution, profile,
                           override)


@click.command()
@click.option("-cl", "--client", type=str, help="Filter by client")
@click.pass_obj
def list_layers(cfg: Cfg, client):
    """List all layers"""
    layers = cfg.db.list_layers()
    if client:
        filtered_layers = [x for x in layers if x["client"] == client]
    else:
        filtered_layers = layers

    click.echo(simplejson.dumps(filtered_layers, indent=4, sort_keys=True))


@click.command()
@click.pass_obj
@click.option("-l", "--layer-id", required=True, type=str, help="Layer uuid")
@click.option('--yes', is_flag=True)
def delete_layer(cfg: Cfg, layer_id, yes):
    """Delete a layer with all timestep entries and permissions"""
    if not yes:
        click.confirm(f'Do you really want to delete layer {layer_id}? All associated data will be deleted', abort=True)

    layer_steps = cfg.db.get_layer_steps(layer_id)

    for layer_step in layer_steps:
        delete_layer_step_files(layer_step, cfg)

    cfg.db.delete_layer(layer_id=layer_id)


@click.command()
@click.pass_obj
@click.option("-l", "--layer-id", required=True, type=str, help="Layer uuid")
@click.option("-t", "--timestep", required=True, type=str, help="ISO timestep e.g 2022-01-01T15:00:00", multiple=True)
@click.option('--yes', is_flag=True)
def delete_layer_timestep(cfg: Cfg, layer_id, timestep, yes):
    """Delete one or multiple layer timesteps"""
    if not yes:
        click.confirm(
            f'Do you really want to delete layer the layer step {timestep} for layer {layer_id}? '
            f'All associated data will be deleted',
            abort=True)
    layer_steps = [cfg.db.get_layer_step(step, layer_id) for step in timestep]

    for layer_step in layer_steps:
        delete_layer_step_files(layer_step, cfg)
        cfg.db.delete_layer_step(layer_step.datetime, layer_id)


@click.command()
@click.pass_obj
@click.option("-l", "--layer-id", required=True, type=str, help="Layer uuid")
def layer_exists(cfg: Cfg, layer_id):
    """Ask database if layer_id exists: returns a boolean"""
    response = cfg.db.get_layer("layer", f"layer#{layer_id}")
    click.echo(bool(response))
