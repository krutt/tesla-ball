#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/middlewares/tick_scheduler.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-06 22:18
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
### v3.10.4 API ###
from apscheduler.schedulers.asyncio import AsyncIOScheduler as AsyncScheduler

### TODO: v4.0.0a3 API ###
# from apscheduler import AsyncScheduler
from starlette.types import ASGIApp
from pendulum import now

### Local modules ###
from src.middlewares import SchedulerMiddleware


class TickSchedulerMiddleware(SchedulerMiddleware):
    def __init__(self, app: ASGIApp, scheduler: AsyncScheduler) -> None:
        self.app = app
        self.interval = 1
        self.scheduler = scheduler
        self.task = lambda: print(f"[INFO] Hello, the time is { now() }")


__all__ = ["TickSchedulerMiddleware"]
