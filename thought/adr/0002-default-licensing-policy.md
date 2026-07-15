# ADR-0002: Default Licensing Policy
 
## Status
Approved

## Context
We need a standard licensing policy across the RPDevs ecosystem. Different types of repositories (infrastructure code, package engines, scripts, and build workflow templates) have varying legal and distribution requirements. Permissive licensing is ideal for reuse, whereas copyleft licensing is necessary to prevent our core software from being integrated into proprietary or telemetry-ridden distributions.

## Decision
We will establish a hybrid default licensing model across our organizations:
1. **Templates and Configurations (MIT License):** All workflow templates (such as `github-actions-repo`), boilerplate configs, and developer setup files will default to the **MIT License**. This enables frictionless adoption and reuse in both private and public downstream codebases.
2. **Core Applications, Feeds, and Binaries (GNU GPLv3 License):** All core manager applications (Tiers 0 to 5), routers tools, custom OpenWRT feeds, Kodi add-ons, and compilations will default to the **GNU GPLv3 License**. This ensures that any redistributions, forks, or enhancements remain open-source and respect user privacy-by-design.

## Consequences
- Every new repository initialized under **RPDevs-Builds** or **RPDevs-Vault** must include the appropriate default `LICENSE` file according to its category.
- Existing repositories will be updated to include the default license files corresponding to this policy.
- Third-party packages imported or forked will retain their upstream licenses as required.
