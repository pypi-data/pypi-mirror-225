"""
Sarmat.

Описание сущностей.

Базовый класс для описания моделей.
"""
from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, List, Optional

from sarmat.core.constants import PeriodType
from sarmat.core.context.containers.sarmat_containers import SarmatContainer, PeriodItemContainer, PeriodContainer


@dataclass
class BaseModel:

    @property
    def sarmat_fields(self):
        return [fld.name for fld in fields(self)]

    @property
    def as_dict(self):
        return asdict(self)

    @classmethod
    def from_container(cls, container: SarmatContainer) -> 'BaseModel':
        raise NotImplementedError

    def raw(self) -> SarmatContainer:
        raise NotImplementedError


@dataclass
class BaseIdModel:

    id: Optional[int] = 0


@dataclass
class BaseUidModel:

    uid: Optional[str] = ""


@dataclass
class CustomAttributesModel:

    custom_attributes: Optional[Dict[str, Any]] = None

    @property
    def custom_fields(self) -> List[str]:
        return list(self.custom_attributes.keys()) if self.custom_attributes else []


@dataclass
class PersonModel(BaseModel):
    """Данные человека"""

    last_name: str      # фамилия
    first_name: str     # имя
    middle_name: str    # отчество
    male: bool          # пол: М


@dataclass
class BasePeriodItemModel(BaseModel):
    """Элементы сложного периода"""

    period_type: PeriodType     # тип периода
    cypher: str                 # шифр (константа)
    name: str                   # название
    value: List[int]            # список значений
    is_active: bool             # период активности


@dataclass
class PeriodItemModel(BaseIdModel, CustomAttributesModel, BasePeriodItemModel):
    @classmethod
    def from_container(cls, container: PeriodItemContainer) -> 'PeriodItemModel':   # type: ignore[override]
        return cls(
            id=container.id,
            custom_attributes=container.custom_attributes,
            period_type=container.period_type,
            cypher=container.cypher,
            name=container.name,
            value=container.value,
            is_active=container.is_active,
        )

    def raw(self) -> PeriodItemContainer:       # type: ignore[override]
        return PeriodItemContainer(
            id=self.id,
            custom_attributes=self.custom_attributes,
            period_type=self.period_type,
            cypher=self.cypher,
            name=self.name,
            value=self.value,
            is_active=self.is_active,
        )


@dataclass
class BasePeriodModel(BaseModel):
    """Период"""

    cypher: str                                         # системное имя
    name: str                                           # константа
    periods: Optional[List[PeriodItemModel]] = None     # описание сложного периода
    period: Optional[PeriodItemModel] = None            # описание простого периода


@dataclass
class PeriodModel(BaseIdModel, CustomAttributesModel, BasePeriodModel):
    @classmethod
    def from_container(cls, container: PeriodContainer) -> 'PeriodModel':       # type: ignore[override]
        period, periods = None, []
        if container.periods:
            periods = [PeriodItemModel.from_container(item) for item in container.periods]
        if container.period:
            period = PeriodItemModel.from_container(container.period)

        return cls(
            id=container.id,
            custom_attributes=container.custom_attributes,
            cypher=container.cypher,
            name=container.name,
            periods=periods,
            period=period,
        )

    def raw(self) -> PeriodContainer:   # type: ignore[override]
        return PeriodContainer(
            id=self.id,
            custom_attributes=self.custom_attributes,
            cypher=self.cypher,
            name=self.name,
            periods=[item.raw() for item in self.periods] if self.periods else None,
            period=self.period.raw() if self.period else None,
        )
