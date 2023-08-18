from sarmat.core.constants import (
    CrewType,
    LocationType,
    PeriodType,
    PermitType,
    RoadType,
    RouteType,
    SettlementType,
    StationType,
    JourneyClass,
    JourneyState,
    JourneyType,
    VehicleType,
    PlaceKind,
    PlaceType,
    PlaceState,
)


def test_route_types():
    assert RouteType.as_text(RouteType.TURNOVER) == "Оборотный"
    assert RouteType.as_text(RouteType.CIRCLE) == "Кольцевой"

    assert RouteType.as_cypher(RouteType.TURNOVER) == "turn"
    assert RouteType.as_cypher(RouteType.CIRCLE) == "circle"

    assert len(RouteType) == RouteType.CIRCLE.value


def test_journey_types():
    assert JourneyType.as_text(JourneyType.SUBURBAN) == "Пригородный"
    assert JourneyType.as_text(JourneyType.LONG_DISTANCE) == "Междугородный"
    assert JourneyType.as_text(JourneyType.INTER_REGIONAL) == "Межрегиональный"
    assert JourneyType.as_text(JourneyType.INTERNATIONAL) == "Международный"
    assert JourneyType.as_text("InterCity") == ""

    assert len(JourneyType) == JourneyType.INTERNATIONAL.value


def test_journey_class():
    assert JourneyClass.as_text(JourneyClass.BASE) == "Формирующийся"
    assert JourneyClass.as_text(JourneyClass.TRANSIT) == "Транзитный"
    assert JourneyClass.as_text(JourneyClass.ARRIVING) == "Прибывающий"
    assert JourneyClass.as_text(0) == ""

    assert len(JourneyClass) == JourneyClass.ARRIVING.value


def test_journey_state():
    assert JourneyState.as_text(JourneyState.READY) == "Активен"
    assert JourneyState.as_text(JourneyState.ARRIVED) == "Прибыл"
    assert JourneyState.as_text(JourneyState.ON_REGISTRATION) == "На регистрации"
    assert JourneyState.as_text(JourneyState.DEPARTED) == "Отправлен"
    assert JourneyState.as_text(JourneyState.CANCELLED) == "Отменен"
    assert JourneyState.as_text(JourneyState.CLOSED) == "Закрыт"
    assert JourneyState.as_text(JourneyState.DISRUPTED) == "Сорван"
    assert JourneyState.as_text(0) == ""

    assert len(JourneyState) == JourneyState.DISRUPTED.value + 1


def test_road_type():
    assert RoadType.as_text(RoadType.PAVED) == "Дорога с твердым покрытием"
    assert RoadType.as_text(RoadType.DIRT) == "Грунтовая дорога"
    assert RoadType.as_text(RoadType.HIGHWAY) == "Магистраль"

    assert len(RoadType) == RoadType.HIGHWAY.value


def test_period_type():
    assert PeriodType.as_text(PeriodType.MINUTE) == "По минутам"
    assert PeriodType.as_text(PeriodType.HOUR) == "По часам"
    assert PeriodType.as_text(PeriodType.DAY) == "По дням"
    assert PeriodType.as_text(PeriodType.WEEK) == "По неделям"
    assert PeriodType.as_text(PeriodType.MONTH) == "По месяцам"
    assert PeriodType.as_text(PeriodType.YEAR) == "По годам"
    assert PeriodType.as_text(PeriodType.EVEN) == "По четным дням месяца"
    assert PeriodType.as_text(PeriodType.ODD) == "По нечетным дням месяца"
    assert PeriodType.as_text(PeriodType.DAYS) == "По числам месяца"
    assert PeriodType.as_text(PeriodType.DAYS_OF_WEEK) == "По дням недели"

    assert PeriodType.as_cypher(PeriodType.MINUTE) == "minute"
    assert PeriodType.as_cypher(PeriodType.HOUR) == "hour"
    assert PeriodType.as_cypher(PeriodType.DAY) == "day"
    assert PeriodType.as_cypher(PeriodType.WEEK) == "week"
    assert PeriodType.as_cypher(PeriodType.MONTH) == "month"
    assert PeriodType.as_cypher(PeriodType.YEAR) == "year"
    assert PeriodType.as_cypher(PeriodType.EVEN) == "even"
    assert PeriodType.as_cypher(PeriodType.ODD) == "odd"
    assert PeriodType.as_cypher(PeriodType.DAYS) == "days"
    assert PeriodType.as_cypher(PeriodType.DAYS_OF_WEEK) == "dow"

    assert len(PeriodType) == PeriodType.DAYS_OF_WEEK.value


def test_location_type():
    assert LocationType.as_text(LocationType.COUNTRY) == "Страна"
    assert LocationType.as_text(LocationType.DISTRICT) == "Республика"
    assert LocationType.as_text(LocationType.PROVINCE) == "Область"
    assert LocationType.as_text(LocationType.REGION) == "Край"
    assert LocationType.as_text(LocationType.AREA) == "Район"

    assert LocationType.as_cypher(LocationType.COUNTRY) == ""
    assert LocationType.as_cypher(LocationType.DISTRICT) == "респ."
    assert LocationType.as_cypher(LocationType.PROVINCE) == "обл."
    assert LocationType.as_cypher(LocationType.REGION) == "кр."
    assert LocationType.as_cypher(LocationType.AREA) == "р-н"

    assert len(LocationType) == LocationType.AREA.value


def test_settlement_type():
    assert SettlementType.as_text(SettlementType.CITY) == "Город"
    assert SettlementType.as_text(SettlementType.SETTLEMENT) == "Поселок"
    assert SettlementType.as_text(SettlementType.TOWNSHIP) == "Село"
    assert SettlementType.as_text(SettlementType.HAMLET) == "Деревня"
    assert SettlementType.as_text(SettlementType.STANITSA) == "Станица"
    assert SettlementType.as_text(SettlementType.FARM) == "Хутор"
    assert SettlementType.as_text(SettlementType.VILLAGE) == "Слобода"
    assert SettlementType.as_text(SettlementType.TURN) == "Поворот"
    assert SettlementType.as_text(SettlementType.POINT) == "Место"

    assert SettlementType.as_cypher(SettlementType.CITY) == "г."
    assert SettlementType.as_cypher(SettlementType.SETTLEMENT) == "пос."
    assert SettlementType.as_cypher(SettlementType.TOWNSHIP) == "с."
    assert SettlementType.as_cypher(SettlementType.HAMLET) == "дер."
    assert SettlementType.as_cypher(SettlementType.STANITSA) == "ст."
    assert SettlementType.as_cypher(SettlementType.FARM) == "х."
    assert SettlementType.as_cypher(SettlementType.VILLAGE) == "сл."
    assert SettlementType.as_cypher(SettlementType.TURN) == "пов."
    assert SettlementType.as_cypher(SettlementType.POINT) == "м."

    assert len(SettlementType) == SettlementType.POINT.value


def test_station_type():
    assert StationType.as_text(StationType.STATION) == "Автовокзал"
    assert StationType.as_text(StationType.TERMINAL) == "Автостанция"
    assert StationType.as_text(StationType.TICKET_OFFICE) == "Автокасса"
    assert StationType.as_text(StationType.PLATFORM) == "Остановочная платформа"

    assert StationType.as_cypher(StationType.STATION) == "АВ"
    assert StationType.as_cypher(StationType.TERMINAL) == "АС"
    assert StationType.as_cypher(StationType.TICKET_OFFICE) == "АК"
    assert StationType.as_cypher(StationType.PLATFORM) == "ОП"

    assert len(StationType) == StationType.PLATFORM.value


def test_vehicle_type():
    assert VehicleType.as_text(VehicleType.BUS) == "Автобус"
    assert VehicleType.as_text(VehicleType.SMALL_BUS) == "Автобус малой вместимости"
    assert VehicleType.as_text(VehicleType.CAR) == "Легковой автомобиль"
    assert VehicleType.as_text(VehicleType.TRUCK) == "Грузовой автомобиль"
    assert VehicleType.as_text(VehicleType.TRAILER) == "Прицеп"
    assert VehicleType.as_text(VehicleType.SPECIAL) == "Спецтехника"

    assert len(VehicleType) == VehicleType.SPECIAL.value


def test_crew_type():
    assert CrewType.as_text(CrewType.DRIVER) == "Водитель"
    assert CrewType.as_text(CrewType.TRAINEE) == "Стажер"

    assert len(CrewType) == CrewType.TRAINEE.value


def test_permit_type():
    assert PermitType.as_text(PermitType.BUS_PERMIT) == "Путевой лист автобуса"
    assert PermitType.as_text(PermitType.CAR_PERMIT) == "Путевой лист легкового автомобиля"
    assert PermitType.as_text(PermitType.TRUCK_PERMIT) == "Путевой лист грузового автомобиля"
    assert PermitType.as_text(PermitType.CUSTOM_PERMIT) == "Заказной путевой лист"

    assert len(PermitType) == PermitType.CUSTOM_PERMIT.value


def test_place_kind():
    assert PlaceKind.as_text(PlaceKind.PASSANGERS_SEAT) == "Пассажирское место"
    assert PlaceKind.as_text(PlaceKind.BAGGAGE) == "Багажное место"

    assert PlaceKind.as_cypher(PlaceKind.PASSANGERS_SEAT) == "P"
    assert PlaceKind.as_cypher(PlaceKind.BAGGAGE) == "B"

    assert len(PlaceKind) == PlaceKind.BAGGAGE.value


def test_place_type():
    assert PlaceType.as_text(PlaceType.STANDING) == "Место для стоящих пассажиров"
    assert PlaceType.as_text(PlaceType.SITTING) == "Место для сидящих пассажиров"

    assert len(PlaceType) == PlaceType.SITTING.value


def test_place_state():
    assert PlaceState.as_text(PlaceState.FREE) == "Свободно"
    assert PlaceState.as_text(PlaceState.BOOKED) == "Забронировано"
    assert PlaceState.as_text(PlaceState.CLOSED) == "Закрыто"
    assert PlaceState.as_text(PlaceState.SOLD) == "Продано"
    assert PlaceState.as_text(PlaceState.LOCKED) == "Заблокировано"
    assert PlaceState.as_text(PlaceState.TRANSFERRED) == "Произведена пересадка"

    assert len(PlaceState) == PlaceState.TRANSFERRED.value
