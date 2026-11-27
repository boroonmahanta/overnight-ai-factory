#!/usr/bin/env bash
# Spike 0.11: check the repository variables before any sign-in. No secrets are involved.
set -euo pipefail
guid='^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
for name in TENANT_ID TEST_APP_ID; do
  [[ "${!name}" =~ $guid ]] || { echo "::error::$name is not a GUID"; exit 1; }
done
# Australia only (rule 15): the Oceania Dataverse host is crm6. Test is fixed, with the
# trailing slash the workflow's URLs are built on.
[[ "$TEST_URL" =~ ^https://factory-test\.crm6\.dynamics\.com/$ ]] || { echo "::error::TEST_URL must be https://factory-test.crm6.dynamics.com/"; exit 1; }
[ "$KEYVAULT" = "kv-getai-factory-aue" ] || { echo "::error::KEYVAULT must be kv-getai-factory-aue"; exit 1; }
[ "$TEST_USER" = "factory-test-nwt@getai.com.au" ] || { echo "::error::TEST_USER must be the nwt test user"; exit 1; }
[ "$TEST_USER_CERT" = "factory-test-nwt" ] || { echo "::error::TEST_USER_CERT must be factory-test-nwt"; exit 1; }
[[ "$VAULT_DELAY" =~ ^[0-9]+$ ]] || { echo "::error::VAULT_DELAY must be whole minutes"; exit 1; }
echo "variables look right"
