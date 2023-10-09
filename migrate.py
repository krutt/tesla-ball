#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/migrate.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-09 13:59
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from asyncio import run

### Third-party packages
from aerich import Command

# from pendulum import now

### Local modules ###
from src.configs import DATABASE_NAME, DATABASE_URL


def main() -> None:
    run(migrate())


async def migrate() -> None:
    command: Command = Command(
        tortoise_config={
            "apps": {
                "models": {
                    "models": ["aerich.models", "src.models"],
                    "default_connection": "default",
                }
            },
            "connections": {"default": DATABASE_URL},
        }
    )
    await command.init()
    await command.init_db(safe=True)
    await command.migrate(DATABASE_NAME)


if __name__ == "__main__":
    main()
