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
from typing import Any, Callable, Optional

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
from pydantic import BaseModel, StrictInt, StrictStr, validate_arguments

### Local modules ###
from src.configs import LND_HOST_URL, LND_MACAROON_PATH, LND_TLSCERT_PATH
from src.protos.lightning_pb2 import (
    AddInvoiceResponse,
    ChannelPoint,
    ConnectPeerRequest,
    ConnectPeerResponse,
    DisconnectPeerRequest,
    DisconnectPeerResponse,
    LightningAddress,
    ListChannelsRequest,
    ListChannelsResponse,
    ListInvoiceRequest,
    ListInvoiceResponse,
    ListPeersRequest,
    ListPeersResponse,
    GetInfoRequest,
    GetInfoResponse,
    Invoice,
    OpenChannelRequest,
)
from src.protos.lightning_pb2_grpc import LightningStub


class MacaroonMetadataPlugin(AuthMetadataPlugin, BaseModel):
    """Metadata plugin to include macaroon in metadata of each RPC request"""

    macaroon: str

    def __call__(self, _: Any, callback: Callable) -> Any:
        callback([("macaroon", self.macaroon)], None)


class Lightning(BaseModel):
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
    def stub(self) -> LightningStub:
        return LightningStub(self.channel)  # type: ignore[no-untyped-call]

    @validate_arguments
    def add_invoice(self, value: StrictInt, memo: StrictStr = "") -> AddInvoiceResponse:
        return self.stub.AddInvoice(Invoice(value=value, memo=memo))

    @validate_arguments
    def connect_peer(self, host: StrictStr, pubkey: StrictStr) -> ConnectPeerResponse:
        addr: LightningAddress = LightningAddress(pubkey=pubkey, host=host)
        return self.stub.ConnectPeer(ConnectPeerRequest(addr=addr, perm=True, timeout=0))

    @validate_arguments
    def disconnect_peer(self, pubkey: StrictStr) -> DisconnectPeerResponse:
        return self.stub.DisconnectPeer(DisconnectPeerRequest(pub_key=pubkey))

    def get_info(self) -> GetInfoResponse:
        """Fetch node policy and information"""
        return self.stub.GetInfo(GetInfoRequest())

    def list_channels(self) -> ListChannelsResponse:
        """List all open channels"""
        return self.stub.ListChannels(ListChannelsRequest())

    def list_invoices(self) -> ListInvoiceResponse:
        return self.stub.ListInvoices(ListInvoiceRequest())

    def list_peers(self) -> ListPeersResponse:
        """List all active, currently connected peers"""
        return self.stub.ListPeers(ListPeersRequest())

    @validate_arguments
    def open_channel(
        self, amount: StrictInt, pubkey: StrictStr, sat_per_byte: StrictInt
    ) -> ChannelPoint:
        """Open a channel to an existing peer"""
        return self.stub.OpenChannelSync(
            OpenChannelRequest(
                local_funding_amount=amount,
                node_pubkey=bytes.fromhex(pubkey),
                sat_per_byte=sat_per_byte,
            )
        )


__all__ = ["AddInvoiceResponse", "ChannelPoint", "Lightning"]
