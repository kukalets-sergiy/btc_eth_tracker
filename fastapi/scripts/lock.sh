#!/bin/bash
set -e

echo "Locking root..."
poetry lock

echo "Locking fastapi..."
cd fastapi
poetry lock

echo "Done."
