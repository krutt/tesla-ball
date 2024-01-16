#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/list_channels.py
# VERSION: 	   0.1.0
# CREATED: 	   2024-01-16 14:04
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.services.lightning import Lightning, ListChannelsResponse
from tests import LND_TARGET_PUBKEY as PUBKEY
from tests.grpc import lightning


def test_list_channels(lightning: Lightning) -> None:
    list_channels_response: ListChannelsResponse = lightning.list_channels()
    assert list_channels_response is not None
    assert list_channels_response.channels is not None
    for channel in list_channels_response.channels:
        assert channel.active is True
        assert channel.remote_pubkey == PUBKEY
