# 🗺️ Project Manager — Tier 3: Workspace & Task Sync

Welcome to the **project-manager** console. This repository serves as the Tier 3 Task Synchronization Hub, containing custom automation used to manage the workspace and sync automatically with organization deliverables.

* **Tier 0:** [github-manager](https://github.com/RPDevs-Vault/github-manager) | **Tier 0.5:** [monitor-manager](https://github.com/RPDevs-Vault/monitor-manager)
* **Tier 1:** [vault-manager](https://github.com/RPDevs-Vault/vault-manager) | **Tier 1.5:** [identity-manager](https://github.com/RPDevs-Vault/identity-manager)
* **Tier 2:** [container-manager](https://github.com/RPDevs-Vault/container-manager) | **Tier 3:** [project-manager](https://github.com/RPDevs-Vault/project-manager)
* **Tier 4:** [distributor-manager](https://github.com/RPDevs-Vault/distributor-manager) | **Tier 4.5:** [deploy-manager](https://github.com/RPDevs-Vault/deploy-manager)
* **Tier 5:** [thought-manager](https://github.com/RPDevs-Vault/thought-manager)

---

## 🛠️ CLI Toolchain (`pm.py`)

The workspace comes equipped with a custom Python-based management CLI (`pm.py`) to automate inventory tracking, project initialization, and quality auditing.

### Commands

| Command | Description |
| :--- | :--- |
| **`scan`** | Scans all workspace directories and compiles/updates the master `INVENTORY.md`. |
| **`status`** | Identifies and displays the top 5 most recently active projects based on code modifications. |
| **`scaffold <name>`** | Initializes a new project directory with standardized `.gemini/GEMINI.md` and `README.md`. Optional: `--tier {Hobbyist,Consulting,Gov}` to auto-inject PMO templates. |
| **`audit <name>`** | Audits a project's files for missing required assets and structural waste (unresolved `[...]` placeholders). |
| **`setup-pmo`** | Installs/initializes the workspace `.gemini/pmo` directory with the PMOSkills manuals and templates. |

### CLI Usage Examples
```bash
# Scan and compile master inventory
./pm.py scan

# Show active coding projects
./pm.py status

# Scaffold a consulting tier project
./pm.py scaffold MyNewProject --tier Consulting

# Audit a project for compliance
./pm.py audit MyNewProject
```

---

## 📁 Directory Structure

```
.
├── bin/          # Executable shims for PM commands
├── core/         # PMOSkills Reference Architecture (Manuals, Templates, Routing)
├── templates/    # Standard templates for project scaffolding
├── pm.py         # Main Project Manager CLI source code
└── pm_sync.py    # GHA issues and roadmap synchronization agent
```

---

## 🗺️ Live Organization Roadmap & Task Tracker

The section below compiles all open issues, tasks, and pull requests from across the entire **RPDevs-Vault** organization, updated automatically on a daily schedule by the [Project Roadmap Sync](.github/workflows/pm-sync.yml) workflow using `pm_sync.py`.

<!-- ROADMAP_START -->

Last Synced: `2026-07-03 08:26:16 UTC`

### 🔍 Open Pull Requests (Requires Review)
- **`RPDevs-Vault/MALSync`**
  - [PR #4: Auto Urls: Update Permissions](https://github.com/RPDevs-Vault/MALSync/pull/4) by @github-actions[bot]
  - [PR #2: Auto Urls](https://github.com/RPDevs-Vault/MALSync/pull/2) by @github-actions[bot]

### 📋 Open Tasks & Issues
- **`RPDevs-Vault/container-manager`**
  - [Issue #35: Weekly Docker Asset Collection Summary](https://github.com/RPDevs-Vault/container-manager/issues/35)
  - [Issue #34: Weekly Docker Asset Collection Summary](https://github.com/RPDevs-Vault/container-manager/issues/34)
  - [Issue #33: Weekly Docker Asset Collection Summary](https://github.com/RPDevs-Vault/container-manager/issues/33)
  - [Issue #32: Weekly Docker Asset Collection Summary](https://github.com/RPDevs-Vault/container-manager/issues/32)
  - [Issue #31: Weekly Docker Asset Collection Summary](https://github.com/RPDevs-Vault/container-manager/issues/31)
  - [Issue #30: Weekly Docker Asset Collection Summary](https://github.com/RPDevs-Vault/container-manager/issues/30)
  - [Issue #29: Weekly Docker Asset Collection Summary](https://github.com/RPDevs-Vault/container-manager/issues/29)
  - [Issue #28: Weekly GHCR Audit Report](https://github.com/RPDevs-Vault/container-manager/issues/28)
  - [Issue #27: Weekly Docker Asset Collection Summary](https://github.com/RPDevs-Vault/container-manager/issues/27)
  - [Issue #1: Implement Organization-wide GHCR Auditor](https://github.com/RPDevs-Vault/container-manager/issues/1)
- **`RPDevs-Vault/demo-repository`**
  - [Issue #1: Test](https://github.com/RPDevs-Vault/demo-repository/issues/1)
- **`RPDevs-Vault/vault-manager`**
  - [Issue #13: License Audit: 20 projects missing licenses](https://github.com/RPDevs-Vault/vault-manager/issues/13)
  - [Issue #12: Weekly Notification Heatmap](https://github.com/RPDevs-Vault/vault-manager/issues/12)


<!-- ROADMAP_END -->
