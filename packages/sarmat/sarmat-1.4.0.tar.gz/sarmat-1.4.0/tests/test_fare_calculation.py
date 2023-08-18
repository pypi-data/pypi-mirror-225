import os
import pytest
from datetime import date
from decimal import Decimal

from sarmat.tools.fare_calculation import AreaStrategy, FareCalculator, PKStrategy
# from tests.test_containers.test_fare_strategy import get_fake_route

base_path = os.path.abspath('.')
prm_pas_fare = base_path + "/tests/data/permanent_passenger_fare.py"
prm_bag_fare = base_path + "/tests/data/permanent_baggage_fare.py"
vol_fare = base_path + "/tests/data/volatile_fare.py"


@pytest.mark.skip('Not ready yet')
def test_fare_calculation(station_factory, destination_point_factory):
    # fake_route = get_fake_route(station_factory, destination_point_factory)
    price = Decimal(1.5)
    area_dimension = [80, 150]
    area_prices = [Decimal(32.4), Decimal(44.8)]

    pas_strategy = PKStrategy(price)
    bag_strategy = AreaStrategy(area_dimension, area_prices)

    with open(prm_pas_fare) as hndl:
        prm_pas_fare_code = hndl.read()

    with open(prm_bag_fare) as hndl:
        prm_bag_fare_code = hndl.read()

    with open(vol_fare) as hndl:
        vol_pas_fare_code = hndl.read()

    calculator = FareCalculator(pas_strategy,
                                bag_strategy,
                                permanent_passenger_calc_script=prm_pas_fare_code,
                                permanent_baggage_calc_script=prm_bag_fare_code,
                                volatile_passenger_calc_script=vol_pas_fare_code)

    # result = calculator.calculate_price(fake_route, 0, 1)
    today = date.today()
    # if today.weekday() == 6:
    #     assert result.base_passenger_price == Decimal(0)
    #     assert result.base_baggage_price == Decimal(0)
    #     assert result.permanent_passenger_price == Decimal(0)
    #     assert result.permanent_baggage_price == Decimal(0)
    # else:
    #     assert result.base_baggage_price == Decimal(20)
    #     assert result.base_passenger_price < 200
    assert today
    assert calculator
