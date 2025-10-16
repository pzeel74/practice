#!/bin/bash

echo "============================================"
echo "  Architecture Test"
echo "============================================"
echo ""
echo "Shell architecture:"
arch
echo ""
echo "Python architecture:"
python3 -c "import platform; print(platform.machine())"
echo ""
echo "Virtual env Python:"
source .venv/bin/activate
python -c "import platform; print(platform.machine())"
echo ""
echo "Package test:"
python -c "import openai; import pinecone; print('✓ Packages load successfully!')"
echo ""
echo "============================================"
echo "  If all show 'arm64' → You're good!"
echo "============================================"
