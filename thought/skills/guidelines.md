# Agentic Skills & Guidelines Manual

This directory serves as the centralized repository for Agent custom skills and configuration.

## 📋 Rule Alignment
All custom skills compiled here should be audited before installation.

### Safety Standard
1. **Opt-in integrations only**: Never execute scripts that modify system configurations without explicit approval.
2. **Path sanity**: Do not write temporary configuration files outside the permissible projects directory.
3. **Secrets storage**: Never commit variables directly into a repository. Reference `identity-manager` variables instead.
