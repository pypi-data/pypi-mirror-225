#!/usr/bin/env python
# encoding: utf-8
#
# @Author: José Sánchez-Gallego
# @Date: Dec 1, 2017
# @Filename: cli.py
# @License: BSD 3-Clause
# @Copyright: José Sánchez-Gallego

import os
import pathlib

import click
from click_default_group import DefaultGroup

from sdsstools.daemonizer import DaemonGroup, cli_coro

from lvmtelemetry.actor import LVMTelemetryActor


@click.group(cls=DefaultGroup, default="actor")
@click.option(
    "-c",
    "--config",
    "config_file",
    type=str,
    help="Path to the user configuration file.",
)
@click.option(
    "-r",
    "--rmq_url",
    "rmq_url",
    default=None,
    type=str,
    help="RabbitMQ URL, eg: amqp://guest:guest@localhost:5672/",
)
@click.pass_context
def lvmtelemetry(ctx, config_file, rmq_url):
    """LVM Telemetry sensor"""

    ctx.obj = {
        "config_file": config_file,
        "rmq_url": rmq_url,
    }


@lvmtelemetry.group(cls=DaemonGroup, prog="lvmtelemetry_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro()
async def actor(ctx):
    """Runs the actor."""

    default_config_file = pathlib.Path(__file__).parent / "etc/lvmtelemetry.yml"
    config_file = ctx.obj["config_file"] or str(default_config_file)

    print("Configuration file", config_file)

    rmq_url = ctx.obj["rmq_url"]

    lvmtelemetry_obj = LVMTelemetryActor.from_config(config_file, url=rmq_url)

    await lvmtelemetry_obj.start()
    await lvmtelemetry_obj.run_forever()


def main():
    lvmtelemetry(auto_envvar_prefix="LVMTELEMETRY")


if __name__ == "__main__":
    main()
