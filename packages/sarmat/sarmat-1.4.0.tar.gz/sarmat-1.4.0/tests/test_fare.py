import pytest

from decimal import Decimal

from sarmat.tools.fare_containers import FareArguments, FareContainer


@pytest.mark.skip('Not implemented yet')
def test_fare_container():
    container = FareContainer(
        base_passenger_price=Decimal(120),
        base_baggage_price=Decimal(12),
    )

    assert container.permanent_passenger_price == Decimal(0)
    assert container.volatile_passenger_price == Decimal(0)
    assert container.permanent_baggage_price == Decimal(0)
    assert container.volatile_baggage_price == Decimal(0)
    assert container.custom_passenger_price is None
    assert container.custom_baggage_price is None


@pytest.mark.skip('Not implemented yet')
def test_fare_arguments(route_factory):
    container = FareArguments(
        route=route_factory(),
        point_from=0,
        point_to=1,
        other_arguments={}
    )

    assert container.base_pas_price == Decimal(0)
    assert container.base_bag_price == Decimal(0)
    assert container.prm_pas_price == Decimal(0)
    assert container.prm_bag_price == Decimal(0)
    assert container.vlt_pas_price == Decimal(0)
    assert container.vlt_bag_price == Decimal(0)
    assert container.customer_pas_price is None
    assert container.customer_bag_price is None
