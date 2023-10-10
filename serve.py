#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/serve.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-Party Packages ###
### v3.10.4 API ###
from apscheduler.schedulers.asyncio import AsyncIOScheduler as AsyncScheduler

### TODO: v4.0.0a3 API ###
# from apscheduler import AsyncScheduler
from fastapi import FastAPI, Request
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise

### Local Modules ###
from src.configs import DATABASE_URL, DATABASE_NAME, SECRET_KEY
from src.middlewares import ChannelSchedulerMiddleware
from src.routes import earn_router, inbound_router, swap_router

### Initiate FastAPI App ###

app: FastAPI = FastAPI()

### Set up Cachette and CsrfProtect ###


class CsrfSettings(BaseModel):
    secret_key: str = SECRET_KEY
    max_age: int = 300  # 5 minutes


@CsrfProtect.load_config
def get_csrf_config() -> CsrfSettings:
    return CsrfSettings()


### Routing ###

app.include_router(earn_router)
app.include_router(inbound_router)
app.include_router(swap_router)


@app.get("/")
async def redirect_to_swagger_docs() -> RedirectResponse:
    """
    Redirects from root base route to Swagger Documentation
    """
    return RedirectResponse("/docs")


@app.get("/health", response_class=PlainTextResponse, status_code=200)
async def health() -> str:
    """
    Health Check
    """
    return "OK"


### Mount static files from /static directory ###

app.mount("/static", StaticFiles(directory="static"), name="static")

## Integrate Cross Origin Resource Sharing Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler: AsyncScheduler = AsyncScheduler()
app.add_middleware(ChannelSchedulerMiddleware, scheduler=scheduler)

### Register Tortoise ORM to FastAPI app ###

register_tortoise(
    app,
    db_url=f"{ DATABASE_URL }/{ DATABASE_NAME }",
    generate_schemas=True,  # If true, creates new database at first launch
    modules={"models": ["src.models"]},
)

### Exception Handlers ###


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError) -> ORJSONResponse:
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(IOError)
def validation_exception_handler(request: Request, exc: IOError) -> ORJSONResponse:
    return ORJSONResponse(status_code=exc.errno, content={"detail": exc.strerror})


__all__ = ["app"]
