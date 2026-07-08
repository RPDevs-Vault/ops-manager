#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
from datetime import datetime, timezone

ORGS = ["RPDevs-Vault", "RPDevs-Builds"]
VAULT_REPOS = [
    "vault-manager", "container-manager", "github-manager", 
    "project-manager", "monitor-manager", "deploy-manager", 
    "distributor-manager", "identity-manager"
]
BUILDS_REPOS = [
    "kodi-build", "xbmc-build", "rpdevs-builds.github.io", 
    "script.service.megacloud", "script.service.flaresolverr", 
    "nextdns-firefox-addon", "vlc-live-555"
]

def github_request(url, token):
    print(f"Fetching URL: {url} ...")
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "RPDevs-Health-Aggregator")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode())
            print(f"Successfully fetched {url}")
            return res
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def get_workflow_runs(org, repo, token):
    url = f"https://api.github.com/repos/{org}/{repo}/actions/runs?per_page=5"
    data = github_request(url, token)
    if not data or "workflow_runs" not in data:
        return []
    return data["workflow_runs"]

def get_runners(org, token):
    url = f"https://api.github.com/orgs/{org}/actions/runners"
    data = github_request(url, token)
    if not data or "runners" not in data:
        return []
    return data["runners"]

def get_rate_limit(token):
    url = "https://api.github.com/rate_limit"
    data = github_request(url, token)
    if not data or "resources" not in data:
        return None
    return data["resources"]["core"]

def generate_dashboard(token):
    lines = []
    lines.append(f"Last Updated: `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`\n")
    
    # 1. Rate Limit
    rl = get_rate_limit(token)
    if rl:
        limit = rl["limit"]
        remaining = rl["remaining"]
        reset_time = datetime.fromtimestamp(rl["reset"], timezone.utc).strftime('%H:%M:%S UTC')
        pct = (remaining / limit) * 100
        lines.append("### 🔑 API Rate Limits")
        lines.append(f"- **Core Rate Limit:** `{remaining}/{limit}` ({pct:.1f}% remaining)")
        lines.append(f"- **Reset Time:** `{reset_time}`\n")
        
    # 2. Self-Hosted Runners for each Org
    lines.append("### 🖥️ Self-Hosted Runner Fleet")
    has_runners = False
    for org in ORGS:
        runners = get_runners(org, token)
        if runners:
            has_runners = True
            lines.append(f"#### `{org}` Runner Fleet")
            lines.append("| Runner Name | OS | Status | Labels |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for r in runners:
                name = r.get("name", "Unknown")
                os_name = r.get("os", "Unknown")
                status = r.get("status", "offline")
                labels = ", ".join([l["name"] for l in r.get("labels", []) if l["name"] not in ["self-hosted", os_name]])
                status_emoji = "🟢 Online" if status == "online" else "🔴 Offline"
                lines.append(f"| `{name}` | {os_name.capitalize()} | {status_emoji} | `{labels}` |")
            lines.append("")
            
    if not has_runners:
        lines.append("*No active self-hosted runners discovered or unauthorized access.*\n")

    # 2.5 Hardware Telemetry
    import glob
    telemetry_dirs = [
        "/mnt/sharedroot/github_runners/shared/telemetry",
        "/home/llmuser/projects/managers/github-manager/telemetry"
    ]
    telemetry_files = []
    for d in telemetry_dirs:
        if os.path.exists(d):
            telemetry_files.extend(glob.glob(os.path.join(d, "*_telemetry.json")))
            
    if telemetry_files:
        lines.append("### 🌡️ Hardware Telemetry")
        lines.append("| Hostname | CPU | Memory | Shared Disk | Temperatures | Last Updated |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for t_file in telemetry_files:
            try:
                with open(t_file, "r") as f:
                    data = json.load(f)
                host = data.get("hostname", "Unknown")
                cpu = f"{data.get('cpu_percent', 0)}%"
                mem = f"{data.get('memory_percent', 0)}%"
                disk = f"{data.get('sharedroot_disk_percent', 0)}%"
                temps_raw = data.get("temperatures", {})
                temps = ", ".join([f"{k}: {v}°C" for k, v in temps_raw.items()]) if temps_raw else "N/A"
                ts = data.get("timestamp", "")
                if ts:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    ts_str = dt.strftime('%H:%M:%S UTC')
                else:
                    ts_str = "Unknown"
                lines.append(f"| `{host}` | {cpu} | {mem} | {disk} | {temps} | {ts_str} |")
            except Exception as e:
                print(f"Error reading {t_file}: {e}", file=sys.stderr)
        lines.append("")

    # Helper function to append workflow runs for an org/repos list
    def append_workflows_section(section_title, org, repos_list):
        lines.append(f"### {section_title}")
        lines.append("| Repository | Workflow | Status | Conclusion | Run Link | Last Run |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        
        for repo in repos_list:
            runs = get_workflow_runs(org, repo, token)
            if not runs:
                lines.append(f"| `{repo}` | *No runs discovered* | - | - | - | - |")
                continue
            
            # Group runs by workflow name and keep only the latest run for each
            latest_runs = {}
            for run in runs:
                wf_name = run.get("name", "Unknown")
                if wf_name not in latest_runs:
                    latest_runs[wf_name] = run
                    
            for wf_name, run in sorted(latest_runs.items()):
                status = run.get("status", "unknown")
                conclusion = run.get("conclusion") or "Running..."
                html_url = run.get("html_url", "#")
                run_number = run.get("run_number", 0)
                
                # Status Emojis
                status_emoji = "⏳"
                if status == "completed":
                    status_emoji = "✅" if conclusion == "success" else "❌"
                elif status == "in_progress":
                    status_emoji = "🔄"
                    
                updated_at_str = run.get("updated_at", "")
                if updated_at_str:
                    dt = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    last_run = dt.strftime('%Y-%m-%d %H:%M UTC')
                else:
                    last_run = "Unknown"
                    
                lines.append(f"| `{repo}` | {wf_name} | {status_emoji} `{status}` | `{conclusion}` | [Run #{run_number}]({html_url}) | {last_run} |")
        lines.append("")

    # 3. Manager Repos Workflow Health
    append_workflows_section("📦 Manager Workflows Health (RPDevs-Vault)", "RPDevs-Vault", VAULT_REPOS)

    # 4. Build Repos Workflow Health
    append_workflows_section("🛠️ Build Workflows Health (RPDevs-Builds)", "RPDevs-Builds", BUILDS_REPOS)
            
    return "\n".join(lines)

def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("SYNC_TOKEN") or os.environ.get("GH_PAT")
    if not token:
        print("Error: GH_TOKEN, SYNC_TOKEN, or GH_PAT environment variable is required", file=sys.stderr)
        sys.exit(1)
        
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        readme_path = "/home/llmuser/projects/managers/github-manager/README.md"
        
    if not os.path.exists(readme_path):
        print(f"Error: README.md not found", file=sys.stderr)
        sys.exit(1)
        
    with open(readme_path, "r") as f:
        content = f.read()
        
    start_tag = "<!-- HEALTH_DASHBOARD_START -->"
    end_tag = "<!-- HEALTH_DASHBOARD_END -->"
    
    if start_tag not in content or end_tag not in content:
        print("Warning: Health Dashboard tags not found in README.md. Appending report at the end.")
        dashboard_content = generate_dashboard(token)
        new_content = content + "\n\n" + start_tag + "\n" + dashboard_content + "\n" + end_tag + "\n"
    else:
        dashboard_content = generate_dashboard(token)
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find(end_tag)
        new_content = content[:start_idx] + "\n\n" + dashboard_content + "\n\n" + content[end_idx:]
        
    with open(readme_path, "w") as f:
        f.write(new_content)
        
    print("Health dashboard updated successfully!")

if __name__ == "__main__":
    main()
