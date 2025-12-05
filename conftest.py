from datetime import datetime, timedelta
from core.clients.api_client import APIClient
from faker import Faker
import pytest

@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.auth()
    return client

@pytest.fixture
def booking_date():
    today = datetime.today()
    checkin_date = today + timedelta(days=10)
    checkout_date = checkin_date + timedelta(days=5)

    return {
        "checkin_date": checkin_date.strftime("%Y-%m-%d"),
        "checkout_date": checkout_date.strftime("%Y-%m-%d")
    }

@pytest.fixture
def generate_random_booking_data(booking_date):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": booking_date["checkin_date"],
            "checkout": booking_date["checkout_date"],
        },
        "additionalneeds": additionalneeds,

    }

    return data