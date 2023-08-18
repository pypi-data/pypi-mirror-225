"""
Sarmat.

Описание сущностей.

Базовый класс для контейнеров.
"""
import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import pydantic

from sarmat.core.constants import PeriodType, DATE_FORMAT, FULL_DATETIME_FORMAT
from sarmat.tools.json_encoder import json_dumps


class SarmatContainer(pydantic.BaseModel):

    custom_attributes: Optional[Dict[str, Any]] = None

    def sarmat_fields(self):
        return list(self.model_fields.keys())

    @classmethod
    def _parse_date(cls, value) -> date:
        return datetime.strptime(value, DATE_FORMAT).date()

    @classmethod
    def _parse_datetime(cls, value) -> datetime:
        return datetime.strptime(value, FULL_DATETIME_FORMAT)

    class ConfigDict:
        json_loads = json.loads
        json_dumps = json_dumps


class BaseIdSarmatContainer(SarmatContainer):
    """Базовая модель с числовым идентификатором."""

    id: Optional[int] = 0


class BaseUidSarmatContainer(SarmatContainer):
    """Базовая модель с UUID идентификатором."""

    uid: Optional[str] = ''


class PeriodItemContainer(BaseIdSarmatContainer):
    """Элементы сложного периода"""

    period_type: PeriodType     # тип периода
    cypher: str                 # шифр (константа)
    name: str                   # название
    value: List[int]            # список значений
    is_active: bool             # период активности


class PeriodContainer(BaseIdSarmatContainer):
    """Период"""

    cypher: str                                           # системное имя
    name: str                                             # константа
    periods: Optional[List[PeriodItemContainer]] = None   # описание сложного периода
    period: Optional[PeriodItemContainer] = None          # описание простого периода


class BasePersonSarmatContainer(SarmatContainer):
    """Базовая модель для описания человека."""

    last_name: str                  # фамилия
    first_name: str                 # имя
    middle_name: Optional[str] = None      # отчество
    male: bool                      # пол
