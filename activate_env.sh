#!/bin/bash
# Quick activation script for the Twitter Clone CrewAI environment

if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "🐍 Virtual environment activated!"
    echo "Python: $(which python)"
    echo "Pip: $(which pip)"
    echo ""
    echo "🚀 Ready to develop! Available commands:"
    echo "  python scripts/test_setup.py          # Test environment"
    echo "  python TwitterClone_CrewAI_Configuration.py  # Run CrewAI"
    echo "  deactivate                           # Exit environment"
else
    echo "❌ Virtual environment not found. Run setup.sh first."
fi
