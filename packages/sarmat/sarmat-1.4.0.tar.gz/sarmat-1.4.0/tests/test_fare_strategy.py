from decimal import Decimal

import pytest

# from sarmat.core.context import RouteStructure, RouteItemStructure
from sarmat.core.exceptions import WrongValueError
from sarmat.tools.fare_calculation import (
    AreaStrategy,
    FixPriceStrategy,
    PercentBaggageStrategy,
    PKStrategy,
)
# from sarmat.tools.fare_containers import FareArguments
#
# from tests.data.behavior_classes import DummyRoute
# from tests.data.fare_test_data import route_items


def get_fake_route(station_factory, destination_point_factory):
    first_station = station_factory()
    first_station.name = "Test1"

    # route_structure = RouteStructure(
    #     id=4,
    #     name="Test1-Test4",
    #     first_station=first_station,
    #     structure=[
    #         RouteItemStructure(
    #             id=idx,
    #             length_from_last_km=item.length,
    #             travel_time_min=item.travel_time,
    #             order=idx,
    #             station=station_factory(),
    #             point=destination_point_factory(),
    #             stop_time_min=item.stop_time,
    #         )
    #         for idx, item in enumerate(route_items)
    #     ],
    #     number=4,
    #     literal="T"
    # )
    #
    # return DummyRoute(**route_structure.as_dict())


@pytest.mark.skip('Not ready yet')
def test_fix_price_strategy(station_factory, destination_point_factory):
    # fake_route = get_fake_route(station_factory, destination_point_factory)
    price_map = [
        [None, Decimal(52), Decimal(96.8), Decimal(160)],
        [None, None, Decimal(34), Decimal(79.5)],
        [None, None, None, Decimal(50)],
        [None, None, None, None],
    ]
    strategy = FixPriceStrategy(price_map)

    # for point_from, point_to, point_ctrl in [
    #     (0, 1, Decimal(52)),
    #     (0, 2, Decimal(96.80)),
    #     (0, 3, Decimal(160)),
    #     (1, 2, Decimal(34)),
    #     (1, 3, Decimal(79.5)),
    #     (2, 3, Decimal(50)),
    # ]:
    #     args = FareArguments(route=fake_route, point_from=point_from, point_to=point_to, other_arguments=dict())
    #     assert strategy.make_base_calculation(args) == point_ctrl.quantize(strategy.accuracy)
    #
    # args = FareArguments(route=fake_route, point_from=3, point_to=2, other_arguments=dict())
    # assert pytest.raises(ImpossibleOperationError, strategy.make_base_calculation, args)
    assert strategy


def test_fail_area_strategy():
    assert pytest.raises(WrongValueError, AreaStrategy, [1, 2, 3], [Decimal(10.0), Decimal(13.2)])


@pytest.mark.skip('Not ready yet')
def test_area_strategy(station_factory, destination_point_factory):
    # fake_route = get_fake_route(station_factory, destination_point_factory)
    area_dimension = [80, 150]
    price = [Decimal(63.5), Decimal(130)]
    strategy = AreaStrategy(area_dimension, price)

    # args = FareArguments(route=fake_route, point_from=0, point_to=1, other_arguments=dict())
    # assert strategy.make_base_calculation(args) == price[0]
    #
    # args = FareArguments(route=fake_route, point_from=0, point_to=2, other_arguments=dict())
    # assert strategy.make_base_calculation(args) == price[0]
    #
    # args = FareArguments(route=fake_route, point_from=0, point_to=3, other_arguments=dict())
    # assert strategy.make_base_calculation(args) == price[1]
    assert strategy


@pytest.mark.skip('Not ready yet')
def test_pk_strategy(station_factory, destination_point_factory):
    # fake_route = get_fake_route(station_factory, destination_point_factory)
    price = Decimal(1.5)
    strategy = PKStrategy(price)
    # args = FareArguments(route=fake_route, point_from=0, point_to=1, other_arguments=dict())

    total_len = 0
    # for idx, item in enumerate(route_items):
    #     args.point_to = idx+1
    #     total_len += item.length
    #
    #     assert strategy.make_base_calculation(args) == total_len * price
    assert total_len == 0
    assert strategy


@pytest.mark.skip('Not ready yet')
def test_percent_baggage_strategy(station_factory, destination_point_factory):
    # fake_route = get_fake_route(station_factory, destination_point_factory)
    price = Decimal(1.5)
    strategy = PKStrategy(price)
    # args = FareArguments(route=fake_route, point_from=0, point_to=1, other_arguments=dict())

    # passenger_price = strategy.make_base_calculation(args)
    # args.base_pas_price = passenger_price

    baggage_strategy = PercentBaggageStrategy(Decimal(10))
    assert baggage_strategy
    assert strategy

    # assert baggage_strategy.make_base_calculation(args) == passenger_price * Decimal(10) / Decimal(100)
