# GEMINI.md - RPDevs Vault Manager Workspace

This directory serves as the local orchestration hub for managing the **RPDevs-Vault** GitHub organization. It is primarily used for bulk repository operations, organization-wide policy enforcement, and managing the central `vault-manager` automation suite.

## 📁 Directory Overview

This is a **Non-Code Project** (Management Workspace). Its purpose is to facilitate the administration of the GitHub organization using the GitHub CLI (`gh`) and automated workflows.

### Key Components

*   **.gemini/**: Reserved for agent-specific configuration and temporary session data.
*   **vault-manager (Remote)**: The central repository ([RPDevs-Vault/vault-manager](https://github.com/RPDevs-Vault/vault-manager)) that houses the GitHub Actions used for organization-wide automation.

## 🚀 Usage & Workflow

The workspace is used to execute the following core management tasks:

1.  **Repository Transfers**: Moving forks and projects into the organization vault.
2.  **Notification Streamlining**: Standardizing notification settings (Releases/Security only) across all repositories.
3.  **Fork Synchronization**: Ensuring all 260+ forks are updated daily with their upstream parents.
4.  **Governance Enforcement**: Implementing labels, cleanup policies, and repository settings organization-wide.

## 🛠️ Management Commands

Commonly used commands in this workspace:

*   **List Org Repos**: `gh repo list RPDevs-Vault --limit 1000`
*   **Check Sync Status**: `gh workflow run sync-forks.yml --repo RPDevs-Vault/vault-manager`
*   **View Org Dashboard**: `gh repo view RPDevs-Vault/vault-manager --web`

## 📋 Development Conventions

*   **Automation First**: All repetitive tasks should be offloaded to the `vault-manager` GitHub Actions rather than run locally.
*   **Ticket-Driven**: Major changes or new automation modules should be tracked via issues in the `vault-manager` repository.
*   **Security**: Always use the `SYNC_TOKEN` (Repository Secret) for cross-repository operations. Never log or store the PAT locally in plain text.
