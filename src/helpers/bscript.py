#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023-2024 All rights reserved.
# FILENAME:    ~~/src/helpers/bscript.py
# VERSION: 	   0.1.0
# CREATED: 	   2024-02-03 13:48
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List


def num_size(value: int) -> int:
  if value > 0x7FFFFFFF:
    return 5
  elif value > 0x7FFFFF:
    return 4
  elif value > 0x7FFF:
    return 3
  elif value > 0x7F:
    return 2
  elif value > 0x00:
    return 1
  return 0


def encode_cltv(value: int) -> bytes:
  buffer_size: int = num_size(value)
  buffer: List[int] = buffer_size * [0x00]
  negative: bool = value < 0
  for index in range(buffer_size):
    buffer[index] = value & 0xFF
    value >>= 8
  if buffer[buffer_size - 1] & 0x80:
    buffer[buffer_size - 1] = 0x80 if negative else 0x00
  elif negative:
    buffer[buffer_size - 1] |= 0x80
  return bytes(bytearray(buffer))


__all__ = ["encode_cltv", "num_size"]
