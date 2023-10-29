#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/src/services/walletkit.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-28 18:44
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
from pydantic import BaseModel, StrictStr

### Local modules ###
from src.configs import LND_HOST_URL, LND_MACAROON_PATH, LND_TLSCERT_PATH
from src.protos.walletkit_pb2_grpc import WalletKitStub
from src.services import MacaroonMetadataPlugin


class WalletKit(BaseModel):
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
            auth_creds = metadata_call_credentials(MacaroonMetadataPlugin(macaroon=macaroon))
        cert_creds: Optional[ChannelCredentials] = None
        if not self.tlscert_path:
            raise ValueError("TLS Certificate path is empty.")
        with open(self.tlscert_path, "rb") as tlscert_file:
            cert_creds = ssl_channel_credentials(tlscert_file.read())
        return composite_channel_credentials(cert_creds, auth_creds)

    @property
    def stub(self) -> WalletKitStub:
        return WalletKitStub(self.channel)  # type: ignore[no-untyped-call]
