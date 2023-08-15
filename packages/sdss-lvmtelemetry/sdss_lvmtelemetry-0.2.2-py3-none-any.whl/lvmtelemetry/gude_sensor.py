#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: gude_sensor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from httpx import AsyncClient


__all__ = ["get_sensor_json"]


async def get_sensor_json(
    host: str,
    ssl: bool = False,
    timeout: float = 5,
    username: str | None = None,
    password: str | None = None,
    skipcomplex: bool = True,
    skipsimple: bool = False,
):
    """Get sensor data as JSON objects."""

    if ssl:
        url = "https://"
    else:
        url = "http://"

    url += host + "/" + "status.json"

    auth = None
    if username is not None and password is not None:
        auth = (username, password)

    DESCR = 0x10000
    VALUES = 0x4000
    EXTEND = 0x800000  # enables complex sensors-groups, such as Sensor 101, 20, etc...
    SENSORS = DESCR + VALUES

    if skipcomplex:
        # Simple-sensors only (fully backward compatible).
        cgi = {"components": SENSORS}
    elif skipsimple:
        # Complex sensors-groups only.
        cgi = {"components": SENSORS + EXTEND, "types": "C"}
    else:
        # Simple-sensors + complex sensors-groups in one merged view.
        cgi = {"components": SENSORS + EXTEND}

    async with AsyncClient(auth=auth, verify=False, timeout=timeout) as client:
        resp = await client.get(url, params=cgi)

    if resp.status_code == 200:
        return resp.json()
    else:
        raise ValueError(f"HTTP request error {resp.status_code}.")


def unpack_json(json_data: dict):
    """Unpacks the sensor returned JSON data into a list of sensor measurements."""

    sensors: list[dict[str, float]] = []

    descr = json_data["sensor_descr"]
    values = json_data["sensor_values"]

    for sensor_idx in range(len(descr)):
        fields = descr[sensor_idx]["fields"]
        sensors.append({})
        for field_idx in range(len(fields)):
            name = fields[field_idx]["name"].lower()
            value = values[sensor_idx]["values"][0][field_idx]["v"]
            sensors[-1][name] = value

    return sensors
