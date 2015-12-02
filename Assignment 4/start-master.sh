#!/usr/bin/env bash
docker run -d -t -P --name spark_master test /start-master.sh "$@"
