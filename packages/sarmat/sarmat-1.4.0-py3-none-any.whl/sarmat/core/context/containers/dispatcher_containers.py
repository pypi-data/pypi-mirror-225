"""
Sarmat.

Описание сущностей.

Диспетчерские объекты.
"""
from datetime import date, datetime
from typing import List, Optional

from pydantic import field_serializer, field_validator

from sarmat.core.constants import DATE_FORMAT, FULL_DATETIME_FORMAT, JourneyClass, JourneyState

from .traffic_management_containers import DestinationPointContainer, JourneyContainer, StationContainer
from .sarmat_containers import BaseIdSarmatContainer, BaseUidSarmatContainer, PeriodContainer
from .vehicle_containers import PermitContainer


class IntervalContainer(BaseIdSarmatContainer):
    """График выполнения рейсов"""

    journey: JourneyContainer   # рейс
    start_date: date            # дата начала
    interval: PeriodContainer   # интервал движения

    @field_validator('start_date', mode="before")
    @classmethod
    def parse_start_date(cls, val):
        if val and isinstance(val, str):
            return cls._parse_date(val)
        return val

    @field_serializer('start_date')
    def serialize_start_date(self, start_date: date, _info):
        return start_date.strftime(DATE_FORMAT)


class JourneyProgressContainer(BaseUidSarmatContainer):
    """Атрибуты рейсовой ведомости"""

    depart_date: date               # дата отправления в рейс
    journey: JourneyContainer       # рейс
    permit: PermitContainer         # номер путевого листа

    @field_validator('depart_date', mode="before")
    @classmethod
    def parse_depart_date(cls, val):
        if val and isinstance(val, str):
            return cls._parse_date(val)
        return val

    @field_serializer('depart_date')
    def serialize_depart_date(self, depart_date: date, _info):
        return depart_date.strftime(DATE_FORMAT)


class JourneyScheduleContainer(BaseUidSarmatContainer):
    """Процесс прохождения рейса по автоматизированным точкам"""

    journey_progress: JourneyProgressContainer                      # рейсовая ведомость
    journey_class: JourneyClass                                     # классификация рейса в данном пункте
    station: Optional[StationContainer] = None                             # станция
    point: Optional[DestinationPointContainer] = None                      # точка прохождения маршрута
    state: JourneyState                                             # состояние рейса
    plan_arrive: Optional[datetime] = None                          # плановое время прибытия
    fact_arrive: Optional[datetime] = None                          # фактическое время прибытия
    plan_depart: Optional[datetime] = None                          # плановое время отправления
    fact_depart: Optional[datetime] = None                          # фактическое время отправления
    platform: str = ''                                              # платформа
    comment: str = ''                                               # комментарий к текущему пункту
    last_items: Optional[List['JourneyScheduleContainer']] = None   # оставшиеся активные пункты прохождения рейса

    @field_validator('plan_arrive', mode="before")
    @classmethod
    def parse_plan_arrive(cls, val):
        if val and isinstance(val, str):
            return cls._parse_datetime(val)
        return val

    @field_serializer('plan_arrive')
    def serialize_plan_arrive(self, plan_arrive: Optional[datetime], _info):
        if plan_arrive:
            return plan_arrive.strftime(FULL_DATETIME_FORMAT)

        return None

    @field_validator('fact_arrive', mode="before")
    @classmethod
    def parse_fact_arrive(cls, val):
        if val and isinstance(val, str):
            return cls._parse_datetime(val)
        return val

    @field_serializer('fact_arrive')
    def serialize_fact_arrive(self, fact_arrive: Optional[datetime], _info):
        if fact_arrive:
            return fact_arrive.strftime(FULL_DATETIME_FORMAT)

        return None

    @field_validator('plan_depart', mode="before")
    @classmethod
    def parse_plan_depart(cls, val):
        if val and isinstance(val, str):
            return cls._parse_datetime(val)
        return val

    @field_serializer('plan_depart')
    def serialize_plan_depart(self, plan_depart: Optional[datetime], _info):
        if plan_depart:
            return plan_depart.strftime(FULL_DATETIME_FORMAT)

        return None

    @field_validator('fact_depart', mode="before")
    @classmethod
    def parse_fact_depart(cls, val):
        if val and isinstance(val, str):
            return cls._parse_datetime(val)
        return val

    @field_serializer('fact_depart')
    def serialize_fact_depart(self, fact_depart: Optional[datetime], _info):
        if fact_depart:
            return fact_depart.strftime(FULL_DATETIME_FORMAT)

        return None
