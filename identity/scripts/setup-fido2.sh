#!/usr/bin/env bash
# setup-fido2.sh - Scaffolding tool to bind Age decryption to a physical FIDO2 key.
# Consistently aligned with global personal memory security heuristics.

set -euo pipefail

IDENTITY_FILE="${HOME}/.age-fido2-identity.txt"
RECOVERY_FILE="${HOME}/.age-master-recovery.txt"

echo "=== FIDO2 Age Hardware Binding Scaffolder ==="

# Check requirements
if ! command -v age &>/dev/null; then
    echo "Error: 'age' is not installed."
    exit 1
fi

if ! command -v age-plugin-fido2prf &>/dev/null; then
    echo "Warning: 'age-plugin-fido2prf' plugin not found. Please compile/install it first."
fi

echo "To generate a FIDO2 hardware bound symmetric key, execute:"
echo "  age-plugin-fido2prf -generate -o ${IDENTITY_FILE}"
echo ""
echo "Make sure to also generate a recovery key offline:"
echo "  age-keygen -o ${RECOVERY_FILE}"
echo ""
echo "For secure automation with Chezmoi templates, reference key decryption:"
echo "  chezmoi decrypt --passphrase --key ${IDENTITY_FILE} secret.txt.age"
echo "============================================="
