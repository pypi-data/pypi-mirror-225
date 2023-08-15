# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel(briegel@mpia.de)
# @Date: 2022-04-06
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio
import pathlib

from clu import AMQPActor

from lvmtelemetry import __version__

from .commands.status import emit_status


class LVMTelemetryActor(AMQPActor):
    """LVM Telemetry actor."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, version=__version__, **kwargs)

        self._schema_path = pathlib.Path(__file__).parents[1] / "etc/schema.json"
        self.sensor_host: str = self.config["sensor"]["host"]

        self.sensor_lock = asyncio.Lock()

    async def start(self):
        """Start actor"""

        await super().start()

        self.load_schema(str(self._schema_path))

        asyncio.create_task(self._emit_status_loop())

    async def _emit_status_loop(self, delay: float = 5.0):
        """Emits the sensor status on a loop."""

        while True:
            try:
                await emit_status(self, internal=True)
            except Exception as err:
                self.write("w", error=f"Failed emitting status with error: {err}")
            await asyncio.sleep(delay)
