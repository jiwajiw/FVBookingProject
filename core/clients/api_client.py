import requests
import os
from dotenv import load_dotenv
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
from requests.auth import HTTPBasicAuth
import allure

load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")
        try:
            environment = Environment(environment_str)
        except KeyError:
            raise KeyError(f"Unsupported environment: {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json',
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PRODUCTION:
            return os.getenv("PRODUCTION_BASE_URL")
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = self.session.get(url, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = self.session.post(url, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT.value}"
            response = self.session.get(url, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 201, f"Status code: {response.status_code}"
        return response.status_code

    def auth(self):
        with allure.step("Getting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT.value}"
            payload = {"username": Users.USERNAME.value, "password": Users.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Status code: {response.status_code}"
        token = response.json().get("token")
        with allure.step("Updating header with authorization"):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_bookings(self, params=None):
        with allure.step("Get booking status"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.get(url, params=params, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Status code: {response.status_code}"
        return response.json()

    def get_booking_by_id(self, booking_id, params=None):
        with allure.step(f"Get booking by id: {booking_id}"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.get(url, params=params, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Status code: {response.status_code}"
        return response.json()

    def delete_booking(self, booking_id):
        with allure.step("Delete booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 201, f"Status code: {response.status_code}"
        return response.status_code == 201

    def create_booking(self, booking_data):
        with allure.step("Create booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.post(url, json=booking_data)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Status code: {response.status_code}"
        return response.json()

    def update_booking(self, booking_id, booking_data):
        with allure.step("Update booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.put(url, json=booking_data, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Status code: {response.status_code}"
        return response.json()

    def partial_update_booking(self, booking_id, booking_data):
        with allure.step("Partial update booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.patch(url, json=booking_data, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Status code: {response.status_code}"
        return response.json()