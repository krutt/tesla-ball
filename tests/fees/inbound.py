#!/usr/bin/env python3.9
# Copyright (C) 2023 All rights reserved.
# FILENAME:  ~~/tests/fees/inbound.py
# VERSION: 	 0.1.0
# CREATED: 	 2023-10-26 15:29
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pytest import mark


@mark.parametrize(
    "channel_size, fee_rate, expected_fee",
    [
        (400_000, 3, 1_500),
        (400_000, 5, 2_100),
        (400_000, 15, 5_100),
        (400_000, 23, 7_500),
        (4_000_000, 3, 6_900),
        (4_000_000, 5, 7_500),
        (4_000_000, 14, 10_200),
        (4_000_000, 21, 12_300),
        (40_000_000, 3, 60_900),
        (40_000_000, 6, 61_800),
        (40_000_000, 13, 63_900),
        (40_000_000, 22, 66_600),
    ],
)
def test_01_calc_inbound_fees(channel_size: int, fee_rate: int, expected_fee: int) -> None:
    liquidity_fee_ppm: int = 1_500
    onchain_bytes_est: int = 300
    assert (fee_rate * onchain_bytes_est) + (channel_size * liquidity_fee_ppm / 1e6) == expected_fee
