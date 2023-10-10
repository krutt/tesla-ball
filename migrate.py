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
from argparse import ArgumentParser, Namespace
from asyncio import run

### Third-party packages
from aerich import Command

# from pendulum import now

### Local modules ###
from src.configs import DATABASE_NAME, DATABASE_URL


def main() -> None:
    parser: ArgumentParser = ArgumentParser()
    action = parser.add_mutually_exclusive_group()  # type: ignore[undefined]
    action.add_argument(
        "--drop",
        action="store_const",
        const="drop",
        default="upgrade",
        dest="action",
        help="Drop tables",
    )
    action.add_argument(
        "--upgrade",
        action="store_const",
        const="upgrade",
        dest="action",
        help="Migrate the latest changes",
    )
    action.add_argument(
        "--init", action="store_const", const="init", dest="action", help="Initiate database"
    )
    action.add_argument(
        "--inspect", action="store_const", const="inspect", dest="action", help="Inspect database"
    )
    args: Namespace = parser.parse_args()
    run(migrate(args.action))


async def migrate(action: str) -> None:
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
    if action == "drop":
        await command.downgrade(delete=True, version=0)
    elif action == "init":
        await command.init_db(safe=True)
    elif action == "inspect":
        print('"""')
        print(await command.inspectdb())
        print('"""')
    elif action == "upgrade":
        await command.migrate(DATABASE_NAME)


if __name__ == "__main__":
    main()
