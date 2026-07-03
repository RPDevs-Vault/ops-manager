# 💡 Management & Automation Ideas (Fleet Stability V2)

This file tracks advanced concepts and features to be implemented for the **RPDevs-Vault** organization, aligned with the **GitHub Build Fleet (V2)** architecture.

## 🛡️ Security & Health
- [x] **Org-wide Dependabot:** Enable security alerts and automated PRs across all 260+ repositories.
- [x] **Organization Health Repository:** Create a `.github` repository to host global templates (LICENSE, CONTRIBUTING, ISSUE_TEMPLATES).
- [x] **Secret Scanning:** Implement automated secret scanning across both accounts to prevent credential leaks.
- [x] **Verified Base Image Registry:** (Builder Integration) Build and host hardened Alpine/Ubuntu images to be used as `FROM` targets by all other organization machines.

## 🏗️ Infrastructure & Build
- [x] **GitHub Container Registry (GHCR):** Migrate build artifacts to `ghcr.io` for versioned OCI image hosting.
- [x] **Environment Protection:** Implement GitHub Environments with manual approval gates for sensitive automation runs.
- [x] **Artifact Lifecycle Manager:** Automatically prune old build artifacts to stay within storage limits.
- [x] **Depends-as-a-Service (DaaS):** Host pre-compiled toolchains and dependencies as release assets to speed up heavy C++ and Kodi builds.

## ⚖️ Governance
- [x] **Global Repository Rulesets:** Enforce branch protection (no force-pushes, no deletions) across all repositories using a single org-level rule.
- [x] **License Auditing:** Automatically detect repositories missing a LICENSE file and inject a standard one.
- [x] **Archival Automator:** Automatically archive repositories where the upstream has been deleted or inactive for > 2 years.
- [x] **Hub Dispatch Orchestrator:** Use `vault-manager` to send events to `container-manager` only when necessary, reducing API polling and rate-limit exhaustion.

## 📊 Reporting
- [x] **Organization Health Dashboard:** Create a GH Action that generates a markdown report of all "unhealthy" repos (missing labels, outdated, etc.).
- [x] **Notification Heatmap:** Track which repos generate the most noise and auto-adjust notification settings.
- [x] **Digital Nervous System (Fleet Status):** Implement a centralized `fleet-status.json` and dashboard to track real-time build outcomes from all builder repositories.
