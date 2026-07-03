# 🚨 Monitor Manager — Tier 0.5: Heartbeat & Alerts

Welcome to the **monitor-manager** terminal. This repository serves as the Tier 0.5 Observability Heartbeat for the **RPDevs-Vault** organization. It manages uptime verification scripts (probes) and alert routers (webhooks) to notify administrators when active runners or release gates fail.

* **Tier 0 Global Cockpit:** [github-manager](https://github.com/RPDevs-Vault/github-manager)
* **Tier 1 Governance Hub:** [vault-manager](https://github.com/RPDevs-Vault/vault-manager)
* **Tier 2 Builder Fleet:** [container-manager](https://github.com/RPDevs-Vault/container-manager)
* **Tier 3 Project Roadmap:** [project-manager](https://github.com/RPDevs-Vault/project-manager)
* **Tier 4 Release Gateway:** [distributor-manager](https://github.com/RPDevs-Vault/distributor-manager)
* **Tier 5 Knowledge Core:** [thought-manager](https://github.com/RPDevs-Vault/thought-manager)

---

## 🏛️ Structure

- **`/probes/`**: Connectivity scripts to verify active server services.
- **`/alerts/`**: Notifiers to route error traces to communication endpoints (e.g., Telegram, Discord).

---

## 🛠️ Usage

### Running Probes Manually
You can test the connectivity of the registered targets:
```bash
python3 probes/ping_endpoints.py
```
