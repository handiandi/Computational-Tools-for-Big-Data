#!/usr/bin/env bash

CONTAINER_ID="$(docker run -i -t -P -d --link spark_master:spark_master test)"
echo "CONTAINER ID:"
echo "${CONTAINER_ID}"
echo "trying to CP"
docker cp "$@" "${CONTAINER_ID}:/usr/local/spark-1.3.0-bin-hadoop2.4/"
docker cp "exercise1_data.txt" "${CONTAINER_ID}:/usr/local/spark-1.3.0-bin-hadoop2.4/"
echo "trying to exec"
docker exec "${CONTAINER_ID}" "/spark-submit.sh" "$@"
echo "trying to stop and rm"
docker stop "${CONTAINER_ID}"
docker rm "${CONTAINER_ID}"
