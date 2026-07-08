#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

ORGS = ["RPDevs-Vault", "RPDevs-Builds"]

def github_request(url, token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "RPDevs-Action-Auditor")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"HTTP Error {e.code} for {url}: {e.read().decode()}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def get_repos_for_org(org, token):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}&sort=pushed"
        data = github_request(url, token)
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos

def get_workflow_runs(org, repo_name, token):
    url = f"https://api.github.com/repos/{org}/{repo_name}/actions/runs?per_page=5"
    data = github_request(url, token)
    if not data or "workflow_runs" not in data:
        return []
    return data["workflow_runs"]

def audit_repo(org, repo_name, token):
    runs = get_workflow_runs(org, repo_name, token)
    return repo_name, org, runs

MANAGERS = ["ops-manager", "builder-manager", "delivery-manager", "workspace-manager"]

def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("SYNC_TOKEN") or os.environ.get("GH_PAT")
    if not token:
        print("Error: GH_TOKEN, SYNC_TOKEN, or GH_PAT environment variable is required", file=sys.stderr)
        sys.exit(1)

    print("Auditing GitHub Actions across RPDevs ecosystem...")
    
    # 1. Fetch repositories and filter
    all_repos = []
    now = datetime.now(timezone.utc)
    cutoff_date = now - timedelta(days=14)

    for org in ORGS:
        repos = get_repos_for_org(org, token)
        print(f"Discovered {len(repos)} repositories in {org}")
        
        filtered_count = 0
        for r in repos:
            repo_name = r["name"]
            is_active = False
            
            # Always audit all of RPDevs-Builds
            if org == "RPDevs-Builds":
                is_active = True
            else:
                # For RPDevs-Vault, check if it is a manager or recently pushed
                if repo_name in MANAGERS:
                    is_active = True
                else:
                    pushed_at_str = r.get("pushed_at")
                    if pushed_at_str:
                        pushed_at = datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                        if pushed_at > cutoff_date:
                            is_active = True
            
            if is_active:
                all_repos.append((org, repo_name))
                filtered_count += 1
        
        print(f"Filtered to {filtered_count} active repositories in {org}")

    # 2. Audit in parallel
    print(f"Querying workflow runs for {len(all_repos)} active repositories...")
    active_runs = []
    recent_runs = []
    all_latest_runs = {}

    one_day_ago = now - timedelta(days=1)

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(audit_repo, org, name, token): (org, name) for org, name in all_repos}
        for future in as_completed(futures):
            org, repo_name = futures[future]
            try:
                name, org_name, runs = future.result()
                if runs:
                    # Keep track of latest run for each distinct workflow in this repo
                    repo_wf_runs = {}
                    for run in runs:
                        wf_name = run.get("name", "Unknown")
                        if wf_name not in repo_wf_runs:
                            repo_wf_runs[wf_name] = run
                        
                        status = run.get("status")
                        conclusion = run.get("conclusion")
                        created_at_str = run.get("created_at")
                        
                        if created_at_str:
                            created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                        else:
                            created_at = now
                            
                        # Categorize
                        if status in ["queued", "in_progress", "waiting"]:
                            active_runs.append((org_name, name, run))
                        elif created_at > one_day_ago:
                            recent_runs.append((org_name, name, run))
                            
                    all_latest_runs[(org_name, name)] = repo_wf_runs
            except Exception as e:
                print(f"Exception auditing {org}/{repo_name}: {e}", file=sys.stderr)

    # 3. Generate Dashboard Markdown
    lines = []
    lines.append(f"Last Updated: `{now.strftime('%Y-%m-%d %H:%M:%S UTC')}`\n")

    # API Status
    url = "https://api.github.com/rate_limit"
    rl_data = github_request(url, token)
    if rl_data and "resources" in rl_data:
        rl = rl_data["resources"]["core"]
        pct = (rl["remaining"] / rl["limit"]) * 100
        reset_time = datetime.fromtimestamp(rl["reset"], timezone.utc).strftime('%H:%M:%S UTC')
        lines.append("### 🔑 API Status")
        lines.append(f"- **Rate Limit Remaining:** `{rl['remaining']}/{rl['limit']}` ({pct:.1f}% remaining)")
        lines.append(f"- **Reset Time:** `{reset_time}`\n")

    # Active runs section
    lines.append("### 🔄 Active Workflows")
    if active_runs:
        lines.append("| Organization | Repository | Workflow | Status | Run Link | Started |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        # Sort by status
        for org, repo, run in sorted(active_runs, key=lambda x: x[2].get("status", "")):
            wf_name = run.get("name", "Unknown")
            status = run.get("status", "unknown")
            html_url = run.get("html_url", "#")
            run_num = run.get("run_number", 0)
            created_at_str = run.get("created_at", "")
            if created_at_str:
                dt = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                created_str = dt.strftime('%Y-%m-%d %H:%M UTC')
            else:
                created_str = "Unknown"
            
            emoji = "🔄" if status == "in_progress" else "⏳"
            lines.append(f"| `{org}` | [`{repo}`](https://github.com/{org}/{repo}) | {wf_name} | {emoji} `{status}` | [Run #{run_num}]({html_url}) | {created_str} |")
    else:
        lines.append("*No workflows currently running or queued.*\n")
    lines.append("")

    # Recent runs (last 24 hours) section
    lines.append("### ⏱️ Completed Workflows (Last 24 Hours)")
    if recent_runs:
        lines.append("| Organization | Repository | Workflow | Conclusion | Run Link | Completed |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for org, repo, run in sorted(recent_runs, key=lambda x: x[2].get("updated_at", ""), reverse=True):
            wf_name = run.get("name", "Unknown")
            conclusion = run.get("conclusion") or "unknown"
            html_url = run.get("html_url", "#")
            run_num = run.get("run_number", 0)
            updated_at_str = run.get("updated_at", "")
            if updated_at_str:
                dt = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                completed_str = dt.strftime('%Y-%m-%d %H:%M UTC')
            else:
                completed_str = "Unknown"
            
            emoji = "✅" if conclusion == "success" else "❌"
            lines.append(f"| `{org}` | [`{repo}`](https://github.com/{org}/{repo}) | {wf_name} | {emoji} `{conclusion}` | [Run #{run_num}]({html_url}) | {completed_str} |")
    else:
        lines.append("*No workflows completed in the last 24 hours.*\n")
    lines.append("")

    # Global Workflow Registry Table (Latest state of every workflow in active repositories)
    lines.append("### 📁 Global Workflow Registry")
    lines.append("| Organization | Repository | Workflow | Last Status | Conclusion | Last Run |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    
    # We only show repositories that actually have at least one workflow run in history
    for (org, repo), wf_dict in sorted(all_latest_runs.items(), key=lambda x: (x[0][0], x[0][1])):
        for wf_name, run in sorted(wf_dict.items()):
            status = run.get("status", "unknown")
            conclusion = run.get("conclusion") or "Running..."
            html_url = run.get("html_url", "#")
            run_num = run.get("run_number", 0)
            updated_at_str = run.get("updated_at", "")
            if updated_at_str:
                dt = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                last_run_str = dt.strftime('%Y-%m-%d %H:%M UTC')
            else:
                last_run_str = "Unknown"
                
            emoji = "⏳"
            if status == "completed":
                emoji = "✅" if conclusion == "success" else "❌"
            elif status == "in_progress":
                emoji = "🔄"
                
            lines.append(f"| `{org}` | [`{repo}`](https://github.com/{org}/{repo}) | {wf_name} | {emoji} `{status}` | `{conclusion}` | [{last_run_str}]({html_url}) |")

    # 4. Write back to README.md
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
    if not os.path.exists(readme_path):
        readme_path = "/home/llmuser/projects/managers/ops-manager/action/README.md"
        
    with open(readme_path, "r") as f:
        content = f.read()

    start_tag = "<!-- ACTIONS_DASHBOARD_START -->"
    end_tag = "<!-- ACTIONS_DASHBOARD_END -->"
    
    if start_tag not in content or end_tag not in content:
        print("Warning: Dashboard tags not found in README.md. Appending report.")
        new_content = content + "\n\n" + start_tag + "\n" + "\n".join(lines) + "\n" + end_tag + "\n"
    else:
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find(end_tag)
        new_content = content[:start_idx] + "\n\n" + "\n".join(lines) + "\n\n" + content[end_idx:]

    with open(readme_path, "w") as f:
        f.write(new_content)

    print("Actions dashboard updated successfully!")

if __name__ == "__main__":
    main()
