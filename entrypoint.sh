#!/bin/bash
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/entrypoint.sh
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-04 00:15
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************

CMD="${1:-serve}"
LVL="${2:-INFO}"
shift
echo "[${LVL}] Entrypoint: $CMD"

### Define Kill Hook for Process ###
kill_hook() {
  echo "[${LVL}] Exiting Elegantly..."
  if [ ! -z "$(pgrep python)" ]; then
    echo "[${LVL}] Killing Running Python Process"
    pkill python
  fi
}
trap 'kill_hook' TERM INT

### Entrypoint ###
if [ "${CMD}" == 'serve' ]; then
  echo "[${LVL}] Starting Server"
  uvicorn serve:app             \
    --host 0.0.0.0 --port $PORT \
    --log-config log_conf.yml   \
  &
elif [ "${CMD}" == 'tunnel' ]; then
  echo "[${LVL}] Creating bash run-time tunnel"
  exec /bin/bash
fi

wait $!