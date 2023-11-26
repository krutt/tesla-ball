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
from pydantic import BaseModel, StrictBool, StrictInt, StrictStr, validate_call

### Local modules ###
from src.configs import LND_HOST_URL, LND_MACAROON_PATH, LND_TLSCERT_PATH
from src.protos.lightning_pb2 import (
    AddInvoiceResponse,
    ChannelPoint,
    ConnectPeerRequest,
    ConnectPeerResponse,
    DisconnectPeerRequest,
    DisconnectPeerResponse,
    EstimateFeeRequest,
    EstimateFeeResponse,
    FeeLimit,
    FeeReportRequest,
    FeeReportResponse,
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
    PaymentHash,
    PayReq,
    PayReqString,
    PendingChannelsRequest,
    PendingChannelsResponse,
    SendRequest,
    SendResponse,
    WalletBalanceRequest,
    WalletBalanceResponse,
)
from src.protos.lightning_pb2_grpc import LightningStub
from src.services.macaroon_plugin import MacaroonPlugin


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
            auth_creds = metadata_call_credentials(MacaroonPlugin(macaroon=macaroon))
        cert_creds: Optional[ChannelCredentials] = None
        if not self.tlscert_path:
            raise ValueError("TLS Certificate path is empty.")
        with open(self.tlscert_path, "rb") as tlscert_file:
            cert_creds = ssl_channel_credentials(tlscert_file.read())
        return composite_channel_credentials(cert_creds, auth_creds)

    @property
    def stub(self) -> LightningStub:
        return LightningStub(self.channel)  # type: ignore[no-untyped-call]

    @validate_call
    def add_invoice(self, value: StrictInt, memo: StrictStr = "") -> AddInvoiceResponse:
        return self.stub.AddInvoice(Invoice(value=value, memo=memo))

    @validate_call
    def connect_peer(self, host: StrictStr, pubkey: StrictStr) -> ConnectPeerResponse:
        """Connect to a remote lnd peer"""
        addr: LightningAddress = LightningAddress(pubkey=pubkey, host=host)
        return self.stub.ConnectPeer(ConnectPeerRequest(addr=addr, perm=True, timeout=0))

    @validate_call
    def decode_pay_req(self, payment_request: StrictStr) -> PayReq:
        """Decode a payment request"""
        return self.stub.DecodePayReq(PayReqString(pay_req=payment_request))

    @validate_call
    def disconnect_peer(self, pubkey: StrictStr) -> DisconnectPeerResponse:
        """Disconnect a remote peer identified by public key"""
        return self.stub.DisconnectPeer(DisconnectPeerRequest(pub_key=pubkey))

    @validate_call
    def estimate_fee(
        self,
        address: StrictStr,
        amount: StrictInt,
        confirmations: StrictInt = 6,
        spend_unconfirmed: StrictBool = True,
    ) -> EstimateFeeResponse:
        """Asks the chain backend to estimate the fee rate and total fees for a transaction that
        pays to multiple specified outputs.
        """
        return self.stub.EstimateFee(
            EstimateFeeRequest(
                AddrToAmount={address: amount},
                target_conf=confirmations,
                spend_unconfirmed=spend_unconfirmed,
            )
        )

    def fee_report(self) -> FeeReportResponse:
        """Display the current fee policies of all active channels"""
        return self.stub.FeeReport(FeeReportRequest())

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

    @validate_call
    def lookup_invoice(self, r_hash: StrictStr) -> Invoice:
        """Lookup an existing invoice by its payment hash"""
        payment_hash: PaymentHash = PaymentHash(r_hash_str=r_hash)
        return self.stub.LookupInvoice(payment_hash)

    @validate_call
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

    def pending_channels(self) -> PendingChannelsResponse:
        """Display information pertaining to pending channels"""
        return self.stub.PendingChannels(PendingChannelsRequest())

    @validate_call
    def send_payment(
        self, payment_request: StrictStr, fee_limit_msat: StrictInt = 1_000
    ) -> SendResponse:
        """Send a payment over lightning"""
        fee_limit: FeeLimit = FeeLimit(fixed_msat=fee_limit_msat)
        return self.stub.SendPaymentSync(
            SendRequest(fee_limit=fee_limit, payment_request=payment_request)
        )

    def wallet_balance(self) -> WalletBalanceResponse:
        return self.stub.WalletBalance(WalletBalanceRequest())


__all__ = ["Lightning"]
