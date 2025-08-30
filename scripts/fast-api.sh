#!/bin/bash

PORT=8000
python -m venv .venv

OS_NAME=$(uname -s)

# Sourcing based on OS
case "$OS_NAME" in
  "Darwin")
    source .venv/bin/activate
    ;;
  *"MINGW"*|*"MSYS"*|*"CYGWIN"*)
    source .venv/Scripts/activate
    ;;
  *)
    echo "OS did not match given choices"
    exit 1
    ;;
esac

pip install -r requirements.txt

fastapi run app/main.py --reload --port $PORT