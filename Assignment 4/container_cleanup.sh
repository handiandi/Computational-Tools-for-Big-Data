#!/bin/bash
sudo docker ps -a | awk '{print $1}' | tail -n +2 | xargs sudo docker stop
sudo docker ps -a | awk '{print $1}' | tail -n +2 | xargs sudo docker rm
