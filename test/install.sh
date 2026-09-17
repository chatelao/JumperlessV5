#!/usr/bin/env bash
# test/install.sh - Install testing tools and frameworks for Jumperless V5-light

set -euo pipefail

echo "==> [V5-light] Installing test tools and frameworks..."

python3 -m pip install --upgrade pip
python3 -m pip install pytest pytest-cov requests pyyaml

echo "==> [V5-light] Test tools successfully installed."
