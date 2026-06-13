# vault-manager

Repository for managing the **RPDevs Vault** organization. This project serves as the central command center for automation, governance, and status reporting across all 260+ repositories.

---

## 📊 Comprehensive Status

### 📦 [Organization Packages](https://github.com/orgs/RPDevs-Vault/packages)

| Metric | Status | Last Updated |
| :--- | :--- | :--- |
| **Org-Wide Sync** | ![Sync Status](https://img.shields.io/badge/Status-Active-brightgreen) | Daily |
| **Fork Health** | ![Fork Health](https://img.shields.io/badge/Health-Monitoring-brightgreen) | Weekly |
| **Governance** | ![Policy Enforcement](https://img.shields.io/badge/Governance-Active-brightgreen) | Weekly |
| **Cleanup Operations** | ![Cleanup](https://img.shields.io/badge/Cleanup-Active-brightgreen) | Weekly |

### 🛠️ Active Modules
- **[Sync All Forks](./.github/workflows/sync-forks.yml):** Daily synchronization of forked repositories.
- **[Label Standardizer](./.github/workflows/label-standardizer.yml):** Weekly enforcement of standard issue labels.
- **[Stale Fork Auditor](./.github/workflows/stale-fork-auditor.yml):** Weekly check for archived/deleted upstream repos.
- **[Merged Branch Cleanup](./.github/workflows/cleanup-branches.yml):** Weekly removal of merged git branches.
- **[Notification Streamliner](./.github/workflows/streamline-notifications.yml):** Daily noise reduction for GitHub notifications.
- **[Organization Archive Engine](./.github/workflows/archive-engine.yml):** Weekly monorepo backup of all fork upstreams in IamRPDev and RPDevs-Vault.
- **[Organization Health Dashboard](./.github/workflows/health-dashboard.yml):** Weekly automated reporting on organization metrics and metadata health.

---

<!-- HEALTH_DASHBOARD_START -->
## 🛡️ Repository Health Overview

| Metric | Count |
| :--- | :--- |
| **Total Repositories** | 21 |
| **Total Forks** | 0 |
| **Standalone Projects** | 21 |
| **Archived Projects** | 0 |

### ⚠️ Attention Required
The following repositories are missing descriptions:
- `IamRPDev/iamrpdev.github.io`
- `IamRPDev/dotfiles`
- `IamRPDev/openwrt-blackhole-feed`
- `IamRPDev/mkdocs_wiki.iamrpdev.github.io`
- `IamRPDev/hugo_main.iamrpdev.github.io`
- `IamRPDev/blackhole-server`
- `IamRPDev/luci-app-blackhole`
- `IamRPDev/llmdata-core`
- `IamRPDev/netboot_menu`
- `IamRPDev/llm-project`
- `IamRPDev/llm-thinktank`
- `IamRPDev/cinn-agent-monitor`
- `IamRPDev/cyan-resonance`
- `IamRPDev/.github`
- `IamRPDev/otaku-docker`
- `IamRPDev/otaku-ui`
- `IamRPDev/otaku-api`
- `IamRPDev/RPDev-Archive`
- `IamRPDev/codex-arcana`
- `IamRPDev/rf-board-tv`
- `IamRPDev/FenlightAnonyMouse.github.io`

<!-- HEALTH_DASHBOARD_END -->

## 📋 Management Tasks

See [Issues](https://github.com/RPDevs-Vault/vault-manager/issues) for the active roadmap. Key initiatives:
- [#1] Label Standardization
- [#2] Stale Fork Auditing
- [#4] Merged Branch Cleanup

---

## 🚀 Setup & Requirements

1. **SYNC_TOKEN:** Ensure a Personal Access Token with `repo` scope is added as a repository secret named `SYNC_TOKEN`.
2. **Permissions:** Actions in this repository operate organization-wide. Verify access before adding new modules.
