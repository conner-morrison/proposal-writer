#!/bin/bash
# Starts the proposal UI on http://localhost:8765
cd "$(dirname "$0")"
exec python3 server.py "$@"
