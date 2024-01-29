#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/tests/grpc/list_peers.py
# VERSION: 	   0.1.0
# CREATED: 	   2024-01-29 14:28
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pendulum import now

### Local modules ###
from src.services.lightning import Lightning, ListPeersResponse
from tests import LND_TARGET_PUBKEY as PUBKEY
from tests.grpc import lightning


def test_01_list_empty_peers(lightning: Lightning) -> None:
  response: ListPeersResponse = lightning.list_peers()
  assert response is not None
  assert response.peers is not None
  assert len(response.peers) > 0
  for peer in response.peers:
    assert peer.address is not None
    assert peer.bytes_sent is not None
    assert isinstance(peer.bytes_sent, int)
    assert peer.bytes_recv is not None
    assert isinstance(peer.bytes_recv, int)
    assert peer.features is not None
    assert peer.features is not None
    assert len(peer.features) > 0
    for feature in peer.features.values():
      assert feature.name is not None
      assert isinstance(feature.name, str)
      assert feature.is_known is not None
      assert isinstance(feature.is_known, bool)
      assert feature.is_known is True
      if feature.is_required is not None:
        assert isinstance(feature.is_required, bool)
    assert peer.flap_count is not None
    assert isinstance(peer.flap_count, int)
    assert peer.last_flap_ns is not None
    assert isinstance(peer.last_flap_ns, int)
    assert int(now().format("x")) * 1e6 > peer.last_flap_ns
    assert peer.last_ping_payload is not None
    assert isinstance(peer.last_ping_payload, bytes)
    assert peer.ping_time is not None
    assert isinstance(peer.ping_time, int)
    assert peer.pub_key is not None
    assert isinstance(peer.pub_key, str)
    assert peer.pub_key == PUBKEY
    assert peer.sync_type is not None
    assert isinstance(peer.sync_type, int)
    assert peer.sync_type == 1  # ACTIVE_SYNC
