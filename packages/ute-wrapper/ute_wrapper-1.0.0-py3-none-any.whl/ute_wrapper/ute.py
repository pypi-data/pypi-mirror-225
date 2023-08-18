"""
    UTE (Administración Nacional de Usinas y Trasmisiones Eléctricas) api wrapper
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

from .utils import make_request

BASE_URL = "https://rocme.ute.com.uy/api/v1"


def login(email: str, phone_number: str) -> str:
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
        "Email": email,
        "PhoneNumber": phone_number,
    }

    return make_request("POST", url, data=data).text


def get_ute_device_list(authorization: str) -> List[dict]:
    """
    Get UTE device list

    Returns:
        List[dict]: List of devices
    """

    accounts_url = f"{BASE_URL}/accounts"
    return make_request("GET", accounts_url, authorization=authorization).json()["data"]


def get_ute_account_info(device_id: str, authorization: str) -> dict:
    """
    Get UTE account info from device id

    Args:
        device_id (str): UTE Device id

    Returns:
        dict: UTE account info
    """

    accounts_by_id_url = f"{BASE_URL}/accounts/{device_id}"
    return make_request("GET", accounts_by_id_url, authorization=authorization).json()["data"]


def get_ute_peak_info(device_id: str, authorization: str) -> dict:
    """
    Get UTE peak info from device id

    Args:
        device_id (str): UTE Device id

    Returns:
        dict: UTE peak info
    """

    peak_by_id_url = f"{BASE_URL}/accounts/{device_id}/peak"
    return make_request("GET", peak_by_id_url, authorization=authorization).json()["data"]


def get_ute_network_status(authorization: str) -> dict:
    """
    Get UTE network status from device id

    Returns:
        dict: UTE network status
    """

    network_status_url = f"{BASE_URL}/info/network/status"
    return make_request("GET", network_status_url, authorization=authorization).json()["data"]["summary"]


def get_ute_renewable_sources(authorization: str) -> str:
    """
    Get UTE renewable sources

    Returns:
        str: UTE renewable sources percentage
    """

    global_demand_url = f"{BASE_URL}/info/demand/global"
    return make_request("GET", global_demand_url).json()["data"]["renewableSources"]


def get_ute_historic_info(
    device_id: str,
    authorization: str,
    average_price: float,
    cost_per_kwh: float,
    date_start: Optional[str] = None,
    date_end: Optional[str] = None,
) -> dict:
    """
    Generate UTE historic info from device id and date range

    Args:
        device_id (str): UTE Device id
        authorization (str): Authorization token
        cost_per_kwh (float): Cost per kwh
        date_start (str): Start date to check
        date_end (str): End date to check

    Returns:
        dict: UTE info
    """

    if date_start is None:
        yesterday = datetime.now() - timedelta(days=1)
        date_start = yesterday.strftime("%Y-%m-%d")

    if date_end is None:
        yesterday = datetime.now() - timedelta(days=1)
        date_end = yesterday.strftime("%Y-%m-%d")

    historic_url = f"https://rocme.ute.com.uy/api/v2/device/{device_id}/curvefromtodate/D/{date_start}/{date_end}"

    response = make_request("GET", historic_url, authorization=authorization).json()

    active_energy = {"total": {"sum_in_kwh": 0}}

    for item in response["data"]:
        if item["magnitudeVO"] == "IMPORT_ACTIVE_ENERGY":
            date = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S%z")
            day_in_week = date.strftime("%A")
            value = round(float(item["value"]), 3)

            active_energy[date.strftime("%d/%m/%Y")] = {
                "kwh": value,
                "aproximated_cost_in_uyu": round(value * cost_per_kwh, 3),
                "day_in_week": day_in_week,
            }
            active_energy["total"]["sum_in_kwh"] = active_energy["total"]["sum_in_kwh"] + value

    active_energy["total"]["aproximated_cost_in_uyu"] = round(active_energy["total"]["sum_in_kwh"] * average_price, 3)
    active_energy["total"]["daily_average_cost"] = round(
        active_energy["total"]["aproximated_cost_in_uyu"] / (len(active_energy) - 1), 3
    )
    return active_energy


def get_current_usage_info(device_id: str, authorization: str) -> dict:
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
    reading_url = f"{BASE_URL}/device/{device_id}/lastReading/30"

    data = {"AccountServicePointId": device_id}

    reading_request = make_request("POST", reading_request_url, authorization=authorization, data=data)

    if reading_request.status_code != 200:
        raise Exception("Error getting reading request")

    response = make_request("GET", reading_url, authorization=authorization).json()

    while not response["success"]:
        sleep(5)
        response = make_request("GET", reading_url, authorization=authorization).json()

    readings = response["data"]["readings"]

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

    power_in_watts = round(power_1_in_watts + power_2_in_watts + power_3_in_watts, 3)

    return_dict = {**response}
    return_dict["data"]["power_in_watts"] = power_in_watts

    return return_dict
