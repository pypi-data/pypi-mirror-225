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

from typing import Optional

import requests


def make_request(method: str, url: str, authorization: str = None, data: Optional[dict] = None) -> requests.Response:
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

    if authorization:
        headers["Authorization"] = f"Bearer {authorization}"

    if method == "GET":
        return requests.get(url, headers=headers)

    if method == "POST":
        return requests.post(url, headers=headers, json=data)

    raise Exception("Method not supported")


def get_average_price(plan: str) -> float:
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
