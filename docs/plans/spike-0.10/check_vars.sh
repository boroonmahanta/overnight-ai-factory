#!/usr/bin/env bash
# Spike 0.10: check the repository variables before any sign-in. No secrets are involved.
set -euo pipefail
guid='^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
for name in TENANT_ID LANE_APP_ID TEST_APP_ID; do
  [[ "${!name}" =~ $guid ]] || { echo "::error::$name is not a GUID"; exit 1; }
done
# Australia only (rule 15): the Oceania Dataverse host is crm6. Lane and Test are fixed.
[[ "$LANE_URL" =~ ^https://factory-lane-1\.crm6\.dynamics\.com/?$ ]] || { echo "::error::LANE_URL must be factory-lane-1"; exit 1; }
[[ "$TEST_URL" =~ ^https://factory-test\.crm6\.dynamics\.com/?$ ]] || { echo "::error::TEST_URL must be factory-test"; exit 1; }
[ "$LANE_APP_ID" != "$TEST_APP_ID" ] || { echo "::error::the lane and Test identities must differ"; exit 1; }
echo "variables look right"
