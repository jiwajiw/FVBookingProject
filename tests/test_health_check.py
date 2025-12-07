import allure
import pytest
import requests

@allure.feature("Test Ping")
@allure.story("Test connection")
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Not expected status code: {status_code}"

@allure.feature("Test Ping")
@allure.story("Test server unavailability")
def test_ping_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client, 'ping', side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.ping()

@allure.feature("Test Ping")
@allure.story("Test wrong HTTP method")
def test_ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client, 'ping', return_value=mock_response)
    with pytest.raises(AssertionError, match=f"Expected status code: {mock_response.status_code}"):
        api_client.ping()

@allure.feature("Test Ping")
@allure.story("Test server error")
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client, 'ping', return_value=mock_response)
    with pytest.raises(AssertionError, match=f"Expected status code: {mock_response.status_code}"):
        api_client.ping()

@allure.feature("Test Ping")
@allure.story("Test wrong URL")
def test_ping_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client, 'ping', return_value=mock_response)
    with pytest.raises(AssertionError, match=f"Expected status code: {mock_response.status_code}"):
        api_client.ping()

@allure.feature("Test Ping")
@allure.story("Test timeout")
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client, 'ping', side_effect=requests.Timeout())
    with pytest.raises(requests.Timeout):
        api_client.ping()

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