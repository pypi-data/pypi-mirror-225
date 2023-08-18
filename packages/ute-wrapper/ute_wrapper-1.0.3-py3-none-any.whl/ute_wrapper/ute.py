"""
    UTE (Administración Nacional de Usinas y Trasmisiones Eléctricas) API Wrapper
    Copyright (C) 2023 Roger Gonzalez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from datetime import datetime, timedelta
from time import sleep
from typing import List, Optional

import requests

BASE_URL = "https://rocme.ute.com.uy/api/v1"


class UTEClient:
    def __init__(self, email: str, phone_number: str, device_id: str = None, average_cost_per_kwh: float = None):
        self.email = email
        self.phone_number = phone_number
        self.device_id = device_id
        self.average_cost_per_kwh = average_cost_per_kwh
        self.authorization = self._login()

        if not self.device_id:
            devices = self.get_devices_list()

            if len(devices) > 1:
                devices_dict = {}
                for device in devices:
                    devices_dict[device["name"]] = device["accountServicePointId"]

                raise Exception(
                    f"""
                You have multiple device IDs. You need to choose one from the list
                Valid options are: {devices_dict}
                """
                )

            self.device_id = devices[0]["accountServicePointId"]

        if not self.average_cost_per_kwh:
            try:
                tariff_type = self.get_account()["meterInfo"]["tariffType"].lower()
                self.average_cost_per_kwh = self.get_average_price(tariff_type)
            except Exception:
                raise Exception("Your tariff type is not standard. Try making it explicit on the client initialization")

    def _make_request(self, method: str, url: str, data: Optional[dict] = None) -> requests.Response:
        """
        Make a HTTP request

        Args:
            method (str): The HTTP method to use. Accepted methods are ``GET``, ``POST``.
            url (str): The URL to use for the request.
            authorization (str): Authorization token
            data (dict): The data to send in the body of the request.

        Returns:
            requests.Response: The response object.

        Raises:
            Exception: If the method is not supported.
        """

        headers = {
            "X-Client-Type": "Android",
            "User-Agent": "okhttp/3.8.1",
            "Content-Type": "application/json; charset=utf-8",
            "Connection": "Keep-Alive",
            "User-Agent": "okhttp/3.8.1",
        }

        try:
            if self.authorization:
                headers["Authorization"] = f"Bearer {self.authorization}"
        except AttributeError:
            pass

        if method == "GET":
            return requests.get(url, headers=headers)

        if method == "POST":
            return requests.post(url, headers=headers, json=data)

        raise Exception("Method not supported")

    def _login(self) -> str:
        """
        Login to UTE

        Args:
            email (str): User email for authentication
            phone_number (str): User phone number for authentication

        Returns:
            str: Authorization token
        """

        url = f"{BASE_URL}/token"
        data = {
            "Email": self.email,
            "PhoneNumber": self.phone_number,
        }

        return self._make_request("POST", url, data=data).text

    def get_devices_list(self) -> List[dict]:
        """
        Get UTE devices list

        Returns:
            List[dict]: List of devices
        """

        accounts_url = f"{BASE_URL}/accounts"
        return self._make_request("GET", accounts_url).json()["data"]

    def get_account(self) -> dict:
        """
        Get UTE account info from device id

        Returns:
            dict: UTE account information
        """

        accounts_by_id_url = f"{BASE_URL}/accounts/{self.device_id}"
        return self._make_request("GET", accounts_by_id_url).json()["data"]

    def get_peak(self) -> dict:
        """
        Get UTE peak info from device id

        Returns:
            dict: UTE peak info
        """

        peak_by_id_url = f"{BASE_URL}/accounts/{self.device_id}/peak"
        return self._make_request("GET", peak_by_id_url).json()["data"]

    def get_network_status(self) -> List[dict]:
        """
        Get UTE network status from device id

        Returns:
            dict: UTE network status
        """

        network_status_url = f"{BASE_URL}/info/network/status"
        return self._make_request("GET", network_status_url).json()["data"]["summary"]

    def get_renewable_sources(self) -> str:
        """
        Get UTE renewable sources

        Returns:
            str: UTE renewable sources percentage
        """

        global_demand_url = f"{BASE_URL}/info/demand/global"
        return self._make_request("GET", global_demand_url).json()["data"]["renewableSources"]

    def get_historic_consumption(
        self,
        date_start: Optional[str] = None,
        date_end: Optional[str] = None,
    ) -> dict:
        """
        Generate UTE historic consumption from device id and date range

        Args:
            date_start (str): Start date to check in format YYYY-MM-DD
            date_end (str): End date to check in format YYYY-MM-DD

        Returns:
            dict: UTE info
        """

        if date_start is None:
            yesterday = datetime.now() - timedelta(days=1)
            date_start = yesterday.strftime("%Y-%m-%d")

        if date_end is None:
            yesterday = datetime.now() - timedelta(days=1)
            date_end = yesterday.strftime("%Y-%m-%d")

        historic_url = (
            f"https://rocme.ute.com.uy/api/v2/device/{self.device_id}/curvefromtodate/D/{date_start}/{date_end}"
        )

        response = self._make_request("GET", historic_url).json()

        active_energy = {"total": {"sum_in_kwh": 0}}

        for item in response["data"]:
            if item["magnitudeVO"] == "IMPORT_ACTIVE_ENERGY":
                date = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S%z")
                day_in_week = date.strftime("%A")
                value = round(float(item["value"]), 3)

                active_energy[date.strftime("%d/%m/%Y")] = {
                    "kwh": value,
                    "aproximated_cost_in_uyu": round(value * self.average_cost_per_kwh, 3),
                    "day_in_week": day_in_week,
                }
                active_energy["total"]["sum_in_kwh"] += value

        active_energy["total"]["aproximated_cost_in_uyu"] = round(
            active_energy["total"]["sum_in_kwh"] * self.average_cost_per_kwh, 3
        )
        active_energy["total"]["daily_average_cost"] = round(
            active_energy["total"]["aproximated_cost_in_uyu"] / (len(active_energy) - 1), 3
        )
        return active_energy

    def _convert_triphasic_powers_to_power_in_watts(self, readings: List[dict]) -> float:
        """
        Convert triphasic powers to power in watts

        Args:
            readings (List[dict]): List of readings

        Returns:
            float: Power in watts
        """

        for reading in readings:
            reading_type = reading["tipoLecturaMGMI"]
            if reading_type == "I1":
                i1 = float(reading["valor"])
            elif reading_type == "I2":
                i2 = float(reading["valor"])
            elif reading_type == "I3":
                i3 = float(reading["valor"])
            elif reading_type == "V1":
                v1 = float(reading["valor"])
            elif reading_type == "V2":
                v2 = float(reading["valor"])
            elif reading_type == "V3":
                v3 = float(reading["valor"])

        power_1_in_watts = v1 * i1
        power_2_in_watts = v2 * i2
        power_3_in_watts = v3 * i3

        return round(power_1_in_watts + power_2_in_watts + power_3_in_watts, 3)

    def get_current_usage_info(self) -> dict:
        """
        Get current usage info from device id

        Args:
            device_id (str): UTE Device id
            authorization (str): Authorization token

        Returns:
            dict: UTE info

        Raises:
            Exception: If the reading request fails
        """

        reading_request_url = f"{BASE_URL}/device/readingRequest"
        reading_url = f"{BASE_URL}/device/{self.device_id}/lastReading/30"

        data = {"AccountServicePointId": self.device_id}

        reading_request = self._make_request("POST", reading_request_url, data=data)

        if reading_request.status_code != 200:
            raise Exception("Error getting reading request")

        response = self._make_request("GET", reading_url).json()

        while not response["success"]:
            sleep(5)
            response = self._make_request("GET", reading_url).json()

        readings = response["data"]["readings"]

        power_in_watts = self._convert_triphasic_powers_to_power_in_watts(readings)

        return_dict = {**response}
        return_dict["data"]["power_in_watts"] = power_in_watts

        return return_dict

    def get_average_price(self, plan: str) -> float:
        """
        Get the average price for a plan

        Args:
            plan (str): Plan name. Can be "triple" or "doble"

        Returns:
            float: Average price

        Raises:
            Exception: If the plan is invalid
        """

        if plan == "triple":
            # 10.680 UYU/kwh * 16.67% of the day (4 hours)
            # 2.223 UYU/kwh * 29.17% of the day (7 hours)
            # 4.875 UYU/kwh * 54.16% of the day (13 hours)
            return (10.680 * 0.1667) + (2.223 * 0.2917) + (4.875 * 0.5416)
        if plan == "doble":
            # 10.680 UYU/kwh * 16.67% of the day (4 hours)
            # 4.280 UYU/kwh * 83.33% of the day (20 hours)
            return (10.680 * 0.1667) + (4.280 * 0.8333)

        raise Exception("Invalid plan")
