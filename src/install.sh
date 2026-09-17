#!/usr/bin/env bash
set -euo pipefail

echo "Installing build dependencies for JumperlessV5light..."
python3 -m pip install --quiet --upgrade pip || true
