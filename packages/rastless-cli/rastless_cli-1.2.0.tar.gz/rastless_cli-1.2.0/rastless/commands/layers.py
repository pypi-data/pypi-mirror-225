from typing import TYPE_CHECKING, Set

from rastless.core.cog import append_to_timestep, create_new_timestep
from rastless.core.s3 import delete_layer_step_files
from rastless.core.validate import validate_layer_step_override

if TYPE_CHECKING:
    from rastless.config import Cfg


def create_timestep(cfg: 'Cfg', filenames: Set[str], append: bool, datetime: str, sensor: str, layer_id: str,
                    temporal_resolution: str, profile: str, override: bool):

    layer_step = cfg.db.get_layer_step(datetime, layer_id)
    override = validate_layer_step_override(layer_step, append, override)

    if layer_step and override:
        delete_layer_step_files(layer_step, cfg)
        create_new_timestep(cfg, filenames, layer_id, datetime, profile, temporal_resolution, sensor)
    elif layer_step and append:
        append_to_timestep(cfg, layer_step, filenames, profile)
    else:
        create_new_timestep(cfg, filenames, layer_id, datetime, profile, temporal_resolution, sensor)
