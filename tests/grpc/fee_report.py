#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/fee_report.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-28 00:58
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.services.lightning import FeeReportResponse, Lightning


def test_01_fee_report() -> None:
    lightning: Lightning = Lightning()
    fee_report: FeeReportResponse = lightning.fee_report()
    assert isinstance(fee_report, FeeReportResponse)
    for channel_fee in fee_report.channel_fees:
        assert isinstance(channel_fee.channel_point, str)
        assert len(channel_fee.channel_point) == 66
        assert isinstance(channel_fee.base_fee_msat, int)
        assert channel_fee.base_fee_msat == 1000
        assert isinstance(channel_fee.fee_per_mil, int)
        assert channel_fee.fee_per_mil == 1
        assert isinstance(channel_fee.fee_rate, float)
        assert channel_fee.fee_rate == 1e-6
        assert isinstance(channel_fee.chan_id, int)
