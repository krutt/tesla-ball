#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/channel_open.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-28 00:58
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************


### Local modules ###
from src.services.lightning import Lightning, PendingChannelsResponse
from tests.grpc import lightning


def test_pending_channels(lightning: Lightning) -> None:
    pending_response: PendingChannelsResponse = lightning.pending_channels()
    print(pending_response)
    for channel in pending_response.pending_open_channels:
        assert channel is not None
        assert isinstance(channel.channel_point, str)
        dixt, port = channel.channel.channel_point.split(":")
        assert dixt is not None
        assert port is not None
        print(dixt, port)
