#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2021-02-14
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

from clu import Command

from lvmtelemetry.gude_sensor import get_sensor_json, unpack_json

from . import lvmtel_parser


if TYPE_CHECKING:
    from lvmtelemetry.actor import LVMTelemetryActor

__all__ = ["status"]


async def emit_status(
    command_or_actor: Command[LVMTelemetryActor] | LVMTelemetryActor,
    internal: bool = False,
):
    """Retrieves and emits the sensor status."""

    if isinstance(command_or_actor, Command):
        lock = command_or_actor.actor.sensor_lock
        host = command_or_actor.actor.sensor_host
    else:
        lock = command_or_actor.sensor_lock
        host = command_or_actor.sensor_host

    async with lock:
        data = unpack_json(await get_sensor_json(host))

    status_output = {}
    for ii in range(len(data)):
        status_output[f"sensor{ii+1}"] = data[ii]

    if isinstance(command_or_actor, Command):
        command_or_actor.info(message=status_output, internal=internal)
    else:
        command_or_actor.write("i", message=status_output, internal=internal)

    return status_output


@lvmtel_parser.command()
async def status(command: Command[LVMTelemetryActor]):
    """Returns the sensor telemetry."""

    try:
        await emit_status(command, internal=False)
        return command.finish()
    except Exception as ex:
        return command.error(error=ex)
