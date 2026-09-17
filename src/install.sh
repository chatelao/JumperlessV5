#!/usr/bin/env bash
# src/install.sh - Install build dependencies for Jumperless V5-light application & firmware

set -euo pipefail

echo "==> [V5-light] Installing build tools and runtime dependencies..."

# Ensure python3 and pip are present
python3 -m pip install --upgrade pip

# Install application build & runtime dependencies
python3 -m pip install setuptools wheel flask pyyaml requests

echo "==> [V5-light] Build dependencies successfully installed."
