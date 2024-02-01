#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
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
from asyncpg import connect
from asyncpg.exceptions import InvalidCatalogNameError
from tortoise.exceptions import DBConnectionError

### Local modules ###
from src.configs import DATABASE_NAME, DATABASE_URL


def main() -> None:
  parser: ArgumentParser = ArgumentParser()
  action = parser.add_mutually_exclusive_group()  # type: ignore[undefined]
  action.add_argument(
    "--create",
    action="store_const",
    const="create",
    default="generate",
    dest="action",
    help="Create database identified by DATABASE_NAME constant.",
  )
  action.add_argument(
    "--downgrade",
    action="store_const",
    const="downgrade",
    dest="action",
    help="Downgrade the latest migration",
  )
  action.add_argument(
    "--dump",
    action="store_const",
    const="dump",
    dest="action",
    help="Dump database identified by DATABASE_NAME constant.",
  )
  action.add_argument(
    "--generate",
    action="store_const",
    const="generate",
    dest="action",
    help="Migrate the latest changes under '~~/migrations/models'",
  )
  action.add_argument(
    "--upgrade",
    action="store_const",
    const="upgrade",
    dest="action",
    help="Upgrade database to the latest migrations",
  )
  action.add_argument(
    "--init", action="store_const", const="init", dest="action", help="Initiate database"
  )
  action.add_argument(
    "--inspect", action="store_const", const="inspect", dest="action", help="Inspect database"
  )
  parser.add_argument("name", default="revision", help="Name of migration", nargs="?", type=str)
  args: Namespace = parser.parse_args()
  name: str = args.name.lower().replace(" ", "_").replace("-", "_")
  run(migrate(args.action, name))


async def migrate(action: str, name: str) -> None:
  ### Database creation / destruction ###
  if action == "create":
    try:
      await connect(f"{ DATABASE_URL }/{ DATABASE_NAME }")
      print(f"[ERROR] Database already exists: { DATABASE_NAME }")
    except InvalidCatalogNameError:
      connection = await connect(f"{ DATABASE_URL }/postgres")
      await connection.execute(f'CREATE DATABASE "{ DATABASE_NAME }";')
    return
  elif action == "dump":
    try:
      connection = await connect(f"{ DATABASE_URL }/postgres")
      await connection.execute(f'DROP DATABASE IF EXISTS "{ DATABASE_NAME }";')
    except InvalidCatalogNameError:
      print(f"[ERROR] Database does not exist: { DATABASE_NAME }")
    return

  ### Migration actions ###
  command: Command = Command(
    tortoise_config={
      "apps": {
        "models": {
          "models": ["aerich.models", "src.schema"],
          "default_connection": "default",
        }
      },
      "connections": {"default": f"{ DATABASE_URL }/{ DATABASE_NAME }"},
    }
  )
  try:
    await command.init()
  except DBConnectionError as err:
    print(f"[ERROR] Unable to migrate due to the following error: { err }")
    return
  if action == "downgrade":
    await command.downgrade(delete=True, version=-1)
  elif action == "generate":
    await command.migrate(name)
  elif action == "init":
    try:
      await command.init_db(safe=True)
    except FileExistsError:
      print(f"[ERROR] Database (name='{ DATABASE_NAME }') is already initiated.")
  elif action == "inspect":
    print('"""')
    print(await command.inspectdb())
    print('"""')
  elif action == "upgrade":
    await command.upgrade(True)


if __name__ == "__main__":
  main()
