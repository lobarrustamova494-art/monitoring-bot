#!/usr/bin/env bash
# Render build script

set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies with pre-compiled wheels
pip install --only-binary=:all: -r requirements.txt || pip install -r requirements.txt

echo "Build completed successfully!"
