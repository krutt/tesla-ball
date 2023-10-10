#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/middlewares/scheduler.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-06 22:18
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from abc import ABC, ABCMeta
from typing import Callable

### Third-party packages ###
### v3.10.4 API ###
from apscheduler.schedulers.asyncio import AsyncIOScheduler as AsyncScheduler

### TODO: v4.0.0a3 API ###
# from apscheduler import AsyncScheduler
# from apscheduler.triggers.interval import IntervalTrigger
from starlette.types import ASGIApp, Receive, Scope, Send


class SchedulerMiddleware(ABC):
    __meta__ = ABCMeta

    app: ASGIApp
    interval: int
    scheduler: AsyncScheduler
    task: Callable

    def __init__(
        self, app: ASGIApp, scheduler: AsyncScheduler, task: Callable, interval: int = 3_600
    ) -> None:
        self.app = app
        self.interval = interval
        self.scheduler = scheduler
        self.task = task

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            ### v3.10.4 API ###
            self.scheduler.add_job(self.task, "interval", seconds=self.interval)
            self.scheduler.start()

            ### TODO:: v4.0.0a3 API ###
            # async with self.scheduler:
            #     await self.scheduler.add_schedule(
            #         self.task, IntervalTrigger(seconds=self.interval), id=uuid()
            #     )
            #     await self.scheduler.start_in_background()
            #     await self.app(scope, receive, send)

        await self.app(scope, receive, send)


__all__ = ["SchedulerMiddleware"]
