#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

docker run --name redis-vecdb -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest