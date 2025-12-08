import allure
import pytest
import requests

@allure.feature("Booking")
@allure.story("Create booking")
def test_create_booking(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    with allure.step("Create booking"):
        response_json = api_client.create_booking(booking_data)
    with allure.step("Assert structure"):
        assert "bookingid" in response_json, "'bookingid' field is absent"
        assert "booking" in response_json, "'booking' field is absent"
    with allure.step("Assert booking data"):
        booking = response_json["booking"]
        assert booking["firstname"] == booking_data["firstname"]
        assert booking["lastname"] == booking_data["lastname"]
        assert booking["totalprice"] == booking_data["totalprice"]
        assert booking["depositpaid"] == booking_data["depositpaid"]
        assert booking["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
        assert booking["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]