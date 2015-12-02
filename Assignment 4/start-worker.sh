#!/usr/bin/env bash
docker run -d -t -P --link spark_master:spark_master test /start-worker.sh "$@"
