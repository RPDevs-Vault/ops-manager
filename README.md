# 🛡️ Identity Manager — Tier 1.5: Secret & Key Broker

Welcome to the **identity-manager** console. This repository serves as the Tier 1.5 Secrets, Keys, and IAM broker for the **RPDevs-Vault** organization. It manages environment variable validation schemas, SSH public keys, GPG configuration records, and runner setup instructions.

* **Tier 0 Global Cockpit:** [github-manager](https://github.com/RPDevs-Vault/github-manager)
* **Tier 1 Governance Hub:** [vault-manager](https://github.com/RPDevs-Vault/vault-manager)
* **Tier 2 Builder Fleet:** [container-manager](https://github.com/RPDevs-Vault/container-manager)
* **Tier 3 Project Roadmap:** [project-manager](https://github.com/RPDevs-Vault/project-manager)
* **Tier 4 Release Gateway:** [distributor-manager](https://github.com/RPDevs-Vault/distributor-manager)
* **Tier 5 Knowledge Core:** [thought-manager](https://github.com/RPDevs-Vault/thought-manager)

---

## 🏛️ Structure

- **`/schemas/`**: Validation schemas (JSON Schema) for environments.
- **`/keys/`**: Public record files containing SSH and GPG public keys.
- **`/scripts/`**: Utilities for environment verification and hardware-token integration.

---

## 🛠️ Usage

### Environment Validation
Before starting a development session, run the verification script to check your local environment health:
```bash
python3 scripts/validate_env.py
```
