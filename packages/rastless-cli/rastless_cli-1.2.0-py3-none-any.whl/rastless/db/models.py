from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, validator

from rastless.db.base import DynamoBaseModel, camel_case, str_uuid


class LayerModel(DynamoBaseModel):
    layer_id: str = Field(default_factory=str_uuid)
    client: str
    product: str
    title: str
    region_id: int = 1
    unit: str = None
    background_id: str = None
    colormap: str = None
    description: str = None

    _pk_tag = "layer"
    _sk_tag = "layer"
    _sk_value = "layer_id"


class PermissionModel(DynamoBaseModel):
    permission: str
    layer_id: str

    _pk_tag = "permission"
    _pk_value = "permission"
    _sk_tag = "layer"
    _sk_value = "layer_id"


class CogFile(BaseModel):
    s3_filepath: str
    bbox: tuple[Decimal, Decimal, Decimal, Decimal]

    @classmethod
    @validator('bbox', each_item=True)
    def to_decimal(cls, value):
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        return value

    class Config:
        allow_population_by_field_name = True
        alias_generator = camel_case


class LayerStepModel(DynamoBaseModel):
    layer_id: str
    cog_filepath: str = None
    cog_layers: dict[str, CogFile] = None
    datetime: str
    sensor: str
    resolution: Decimal
    temporal_resolution: str
    maxzoom: int
    minzoom: int
    bbox: tuple[Decimal, Decimal, Decimal, Decimal]

    _pk_tag = "step"
    _pk_value = "datetime"
    _sk_tag = "layer"
    _sk_value = "layer_id"

    @classmethod
    @validator('bbox', each_item=True)
    def to_decimal(cls, value):
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        return value


class ColorMap(DynamoBaseModel):
    name: str
    description: str = None
    values: List[Decimal]
    colors: List[List[Decimal]]
    nodata: List[Decimal]
    legend_image: str = None

    _pk_tag = "cm"
    _sk_tag = "cm"
    _sk_value = "name"
