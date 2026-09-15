#!/usr/bin/env bash
# Connect this machine's proposal-writer to the relay workspace.
#
# Reads credentials from .env (gitignored). The bridge dials out, so nothing
# here needs a public address or an open port. Jobs posted to the relay's
# channel land in the local UI's queue, exactly as if they had been typed in.
set -euo pipefail
cd "$(dirname "$0")"

[ -f .env ] || { echo "no .env: the relay worker id and token live there"; exit 1; }
set -a; . ./.env; set +a

exec python3 proposal_bridge.py \
  --relay "$RELAY_URL" \
  --local "${PROPOSAL_UI:-http://127.0.0.1:8765}" \
  --worker-id "$RELAY_WORKER" \
  --token "$RELAY_TOKEN" \
  --person "${PROPOSAL_PERSON:-Zachary}" \
  --guide "${PROPOSAL_GUIDE:-brainstormed}" \
  --label "Claude Code proposal writer (local)" \
  "$@"
