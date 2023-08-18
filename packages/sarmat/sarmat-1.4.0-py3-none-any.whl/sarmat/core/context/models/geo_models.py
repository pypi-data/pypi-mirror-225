"""
Sarmat.

Описание сущностей.

Модели для описания географических объектов.
"""
from dataclasses import dataclass
from typing import Optional

from sarmat.core.constants import LocationType, SettlementType
from sarmat.core.verification import DestinationPointVerifier, GeoVerifier

from .sarmat_models import BaseIdModel, BaseModel, CustomAttributesModel
from ..containers import (
    DestinationPointContainer,
    DirectionContainer,
    GeoContainer,
    RoadNameContainer,
)


@dataclass
class BaseGeoModel(BaseModel):
    """Модель географического справочника"""

    name: str                               # наименование
    location_type: LocationType             # тип образования
    latin_name: str = ""                    # латинское название
    mapping_data: Optional[dict] = None     # данные геолокации
    tags: Optional[str] = ''                # теги
    parent: Optional['GeoModel'] = None     # родительский объект


@dataclass
class GeoModel(BaseIdModel, CustomAttributesModel, BaseGeoModel):
    @classmethod
    def from_container(cls, geo_container: GeoContainer) -> 'GeoModel':     # type: ignore[override]
        GeoVerifier().verify(geo_container)

        return cls(
            id=geo_container.id or 0,
            custom_attributes=geo_container.custom_attributes,
            name=geo_container.name,
            latin_name=geo_container.latin_name,
            location_type=geo_container.location_type,
            mapping_data=geo_container.mapping_data,
            tags=geo_container.tags,
            parent=GeoModel.from_container(geo_container.parent) if geo_container.parent else None,
        )

    def raw(self) -> GeoContainer:      # type: ignore[override]
        return GeoContainer(
            id=self.id,
            custom_attributes=self.custom_attributes,
            name=self.name,
            latin_name=self.latin_name,
            location_type=self.location_type,
            mapping_data=self.mapping_data,
            tags=self.tags,
            parent=self.parent.raw() if self.parent else None,
        )


@dataclass
class BaseDestinationPointModel(BaseModel):
    """Модель для описания пунктов назначения"""

    name: str                       # наименование
    state: GeoModel                 # территориальное образование
    point_type: SettlementType      # тип поселения


@dataclass
class DestinationPointModel(BaseIdModel, CustomAttributesModel, BaseDestinationPointModel):
    @classmethod
    def from_container(cls, container: DestinationPointContainer) -> 'DestinationPointModel':   # type: ignore[override]
        DestinationPointVerifier().verify(container)

        return cls(
            id=container.id or 0,
            custom_attributes=container.custom_attributes,
            name=container.name,
            state=GeoModel.from_container(container.state),
            point_type=container.point_type,
        )

    def raw(self) -> DestinationPointContainer:     # type: ignore[override]
        return DestinationPointContainer(
            id=self.id,
            custom_attributes=self.custom_attributes,
            name=self.name,
            state=self.state.raw(),
            point_type=self.point_type,
        )


@dataclass
class BaseDirectionModel(BaseModel):
    """Модель для описания направления"""

    name: str           # наименование
    cypher: str = ""    # шифр (системное имя)


@dataclass
class DirectionModel(BaseIdModel, CustomAttributesModel, BaseDirectionModel):
    @classmethod
    def from_container(cls, container: DirectionContainer) -> 'DirectionModel':     # type: ignore[override]
        return cls(
            id=container.id or 0,
            custom_attributes=container.custom_attributes,
            name=container.name,
            cypher=container.cypher,
        )

    def raw(self) -> DirectionContainer:    # type: ignore[override]
        return DirectionContainer(
            id=self.id,
            custom_attributes=self.custom_attributes,
            name=self.name,
            cypher=self.cypher,
        )


@dataclass
class BaseRoadNameModel(BaseModel):
    """Модель для описания дороги"""

    cypher: str
    name: str = ''


@dataclass
class RoadNameModel(BaseIdModel, CustomAttributesModel, BaseRoadNameModel):
    @classmethod
    def from_container(cls, container: RoadNameContainer) -> 'RoadNameModel':       # type: ignore[override]
        return cls(
            id=container.id or 0,
            custom_attributes=container.custom_attributes,
            name=container.name,
            cypher=container.cypher,
        )

    def raw(self) -> RoadNameContainer:    # type: ignore[override]
        return RoadNameContainer(
            id=self.id,
            custom_attributes=self.custom_attributes,
            name=self.name,
            cypher=self.cypher,
        )
