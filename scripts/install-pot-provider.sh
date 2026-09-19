#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROVIDER_DIR="${PROJECT_DIR}/.pot-provider"
PROVIDER_VERSION="1.3.2"

if [[ ! -d "${PROVIDER_DIR}/.git" ]]; then
    git clone --single-branch --branch "${PROVIDER_VERSION}" \
        https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git \
        "${PROVIDER_DIR}"
else
    git -C "${PROVIDER_DIR}" fetch --tags origin
    git -C "${PROVIDER_DIR}" checkout --detach "${PROVIDER_VERSION}"
fi

cd "${PROVIDER_DIR}/server"
npm ci
npx tsc

echo "PO-token provider installed in ${PROVIDER_DIR}"
