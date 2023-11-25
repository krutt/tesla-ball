#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/services/chain_kit.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-11-25 16:23
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from binascii import hexlify
from typing import Optional

### Third-party packages ###
from grpc import (
    CallCredentials,
    Channel,
    ChannelCredentials,
    composite_channel_credentials,
    metadata_call_credentials,
    secure_channel,
    ssl_channel_credentials,
)
from pydantic import BaseModel, StrictStr, validate_call

### Local modules ###
from src.configs import LND_HOST_URL, LND_MACAROON_PATH, LND_TLSCERT_PATH
from src.protos.chainkit_pb2 import GetBestBlockRequest, GetBestBlockResponse
from src.protos.chainkit_pb2_grpc import ChainKitStub
from src.services.macaroon_plugin import MacaroonPlugin


class ChainKit(BaseModel):
    macaroon_path: Optional[StrictStr] = LND_MACAROON_PATH
    tlscert_path: Optional[StrictStr] = LND_TLSCERT_PATH
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
        if not self.macaroon_path:
            raise ValueError("Macaroon path is empty.")
        auth_creds: Optional[CallCredentials] = None
        with open(self.macaroon_path, "rb") as macaroon_file:
            macaroon_bytes: bytes = macaroon_file.read()
            macaroon: str = hexlify(macaroon_bytes).decode()
            auth_creds = metadata_call_credentials(MacaroonPlugin(macaroon=macaroon))
        cert_creds: Optional[ChannelCredentials] = None
        if not self.tlscert_path:
            raise ValueError("TLS Certificate path is empty.")
        with open(self.tlscert_path, "rb") as tlscert_file:
            cert_creds = ssl_channel_credentials(tlscert_file.read())
        return composite_channel_credentials(cert_creds, auth_creds)

    @property
    def stub(self) -> ChainKitStub:
        return ChainKitStub(self.channel)  # type: ignore[no-untyped-call]

    @validate_call
    def best_block(self) -> GetBestBlockResponse:
        return self.stub.GetBestBlock(GetBestBlockRequest())


__all__ = ["ChainKit"]
