#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_FILE="${PROJECT_DIR}/.pot-provider/server/build/main.js"

if [[ ! -f "${SERVER_FILE}" ]]; then
    echo "PO-token provider is not installed. Run scripts/install-pot-provider.sh first." >&2
    exit 1
fi

exec node "${SERVER_FILE}"
