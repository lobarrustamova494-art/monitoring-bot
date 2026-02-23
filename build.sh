#!/usr/bin/env bash
# Render build script

set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install pydantic with pre-compiled binary wheels first
pip install --only-binary=:all: pydantic pydantic-core pydantic-settings || echo "Binary install failed, trying source"

# Install remaining dependencies
pip install -r requirements.txt

echo "Build completed successfully!"
