#!/bin/bash

# Navigate to script directory
cd "$(dirname "$0")"

# Force ARM64 architecture and run
exec arch -arm64 /bin/bash -c "source .venv/bin/activate && python chat.py"
