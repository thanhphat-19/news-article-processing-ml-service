#!/bin/bash
set -euo pipefail

docker compose -f docker-compose-local.yaml up --build 
