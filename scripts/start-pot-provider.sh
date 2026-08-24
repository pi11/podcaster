#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_FILE="${PROJECT_DIR}/.pot-provider/server/build/main.js"

if [[ ! -f "${SERVER_FILE}" ]]; then
    echo "PO-token provider is not installed. Run scripts/install-pot-provider.sh first." >&2
    exit 1
fi

# yt-dlp passes the active download proxy to the provider in each token request.
# Inherited proxy variables would make Axios apply the same proxy a second time.
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy

exec node "${SERVER_FILE}"
