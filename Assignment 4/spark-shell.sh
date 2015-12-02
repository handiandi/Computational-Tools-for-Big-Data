#!/usr/bin/env bash
docker run -i -t -P --link spark_master:spark_master test /pyspark.sh "$@"
