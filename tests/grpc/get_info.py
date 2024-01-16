#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/tests/grpc/get_info.py
# VERSION: 	   0.1.0
# CREATED: 	   2024-01-16 14:54
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from time import time

### Local modules ###
from src.services.lightning import GetInfoResponse, Lightning
from tests.grpc import lightning


def test_get_info(lightning: Lightning) -> None:
    info_response: GetInfoResponse = lightning.get_info()
    assert info_response is not None
    assert info_response.identity_pubkey is not None
    assert isinstance(info_response.identity_pubkey, str)
    assert info_response.alias is not None
    assert isinstance(info_response.alias, str)
    assert info_response.num_pending_channels is not None
    assert isinstance(info_response.num_pending_channels, int)
    assert info_response.num_active_channels is not None
    assert isinstance(info_response.num_active_channels, int)
    assert info_response.num_peers is not None
    assert isinstance(info_response.num_peers, int)
    assert info_response.block_height
    assert isinstance(info_response.block_height, int)
    assert info_response.block_height > 0
    assert info_response.block_hash is not None
    assert isinstance(info_response.block_hash, str)
    assert info_response.synced_to_chain is not None
    assert isinstance(info_response.synced_to_chain, bool)
    assert info_response.synced_to_chain is True
    assert info_response.uris is not None
    assert len(info_response.uris) != 0
    for uri in info_response.uris:
      assert isinstance(uri, str)
      pubkey, node = uri.split("@")
      assert pubkey == info_response.identity_pubkey
      host, port = node.split(":")
      assert host is not None
      assert port is not None
      assert port == "9735"
    assert info_response.best_header_timestamp is not None
    assert isinstance(info_response.best_header_timestamp, int)
    assert info_response.best_header_timestamp < time()
    assert info_response.version is not None
    assert isinstance(info_response.version, str)
    assert info_response.version == "0.17.2-beta commit=v0.17.2-beta"
    assert info_response.chains is not None
    chain = info_response.chains[0]
    assert chain.chain is not None
    assert isinstance(chain.chain, str)
    assert chain.chain == "bitcoin"
    assert chain.network is not None
    assert isinstance(chain.network, str)
    assert chain.network == "regtest"
    assert info_response.features is not None
    assert len(info_response.features) != 0
    for feature in info_response.features.values():
        assert feature.name is not None
        assert isinstance(feature.name, str)
        assert feature.is_known is not None
        assert isinstance(feature.is_known, bool)
        assert feature.is_known is True
        if feature.is_required is not None:
          assert isinstance(feature.is_required, bool)
    assert info_response.commit_hash is not None
    assert isinstance(info_response.commit_hash, str)
