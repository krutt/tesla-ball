#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/services/lightning.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:52
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from binascii import hexlify
from typing import Callable, Optional

### Third-party packages ###
from grpc import (
    AuthMetadataPlugin,
    CallCredentials,
    Channel,
    ChannelCredentials,
    composite_channel_credentials,
    metadata_call_credentials,
    secure_channel,
    ssl_channel_credentials,
)
from pydantic import BaseModel, StrictStr

### Local modules ###
from src.configs import LND_HOST_URL, LND_MACAROON_PATH, LND_TLSCERT_PATH
from src.services.lightning_pb2 import GetInfoRequest
from src.services.lightning_pb2_grpc import LightningStub

class MacaroonMetadataPlugin(AuthMetadataPlugin, BaseModel):
    """Metadata plugin to include macaroon in metadata of each RPC request"""
    macaroon: str
    def __call__(self, _, callback: Callable):
        callback([('macaroon', self.macaroon)], None)

class Lightning(BaseModel):
    macaroon_path: StrictStr = LND_MACAROON_PATH
    tlscert_path: StrictStr = LND_TLSCERT_PATH
    url: StrictStr = LND_HOST_URL

    @property
    def channel(self) -> Channel:
        return secure_channel(
            self.url,
            self.creds,
            options=[
                ("grpc.max_receive_message_length", 1024 * 1024 * 50),
                ("grpc.max_connection_idle_ms", 30000),
            ],
        )

    @property
    def creds(self) -> ChannelCredentials:
        auth_creds: Optional[CallCredentials] = None
        with open(self.macaroon_path, "rb") as macaroon_file:
            macaroon_bytes: bytes = macaroon_file.read()
            macaroon: str = hexlify(macaroon_bytes).decode()
            auth_creds = metadata_call_credentials(MacaroonMetadataPlugin(macaroon=macaroon))
        cert_creds: Optional[ChannelCredentials] = None
        with open(self.tlscert_path, "rb") as tlscert_file:
            cert_creds = ssl_channel_credentials(tlscert_file.read())
        return composite_channel_credentials(cert_creds, auth_creds)

    @property
    def stub(self) -> LightningStub:
        return LightningStub(self.channel)

    def get_info(self):
        return self.stub.GetInfo(GetInfoRequest())

__all__ = ["Lightning"]
