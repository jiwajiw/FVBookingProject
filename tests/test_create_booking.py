import allure
import pytest
import requests
from pydantic import ValidationError
from core.models.booking import BookingResponse

@allure.feature("Booking")
@allure.story("Positive: create booking with random data")
def test_create_booking(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    with allure.step("Create booking"):
        response_json = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response_json)
        except ValidationError as error:
            raise ValidationError(f"Response error: {error}")

    with allure.step("Assert booking data"):
        booking = response_json["booking"]
        assert booking["firstname"] == booking_data["firstname"]
        assert booking["lastname"] == booking_data["lastname"]
        assert booking["totalprice"] == booking_data["totalprice"]
        assert booking["depositpaid"] == booking_data["depositpaid"]
        assert booking["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
        assert booking["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
        assert booking["additionalneeds"] == booking_data["additionalneeds"]

@allure.feature("Booking")
@allure.story("Negative: missing required field")
def test_create_booking_missing_firstname(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    booking_data.pop("firstname")

    with allure.step("Expect error due to missing firstname"):
        with pytest.raises(requests.HTTPError):
            api_client.create_booking(booking_data)

@allure.feature("Booking")
@allure.story("Negative: invalid data type")
def test_create_booking_invalid_totalprice(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    booking_data["totalprice"] = "not a number"

    with allure.step("Create booking with invalid totalprice"):
        response_json = api_client.create_booking(booking_data)

    with allure.step("Validation should fail because totalprice must be int"):
        with pytest.raises(ValidationError):
            BookingResponse(**response_json)

@allure.feature("Booking")
@allure.story("Negative: empty payload")
def test_create_booking_empty_payload(api_client):
    with allure.step("Expect error with empty request body"):
        with pytest.raises(requests.HTTPError):
            api_client.create_booking({})

def test_create_booking_invalid_response_structure(api_client, mocker, generate_random_booking_data):
    mock_response = {"wrong": "structure"}
    mocker.patch.object(api_client, "create_booking", return_value=mock_response)

    with pytest.raises(ValidationError):
        BookingResponse(**mock_response)