#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
from datetime import datetime, timezone

ORG = "RPDevs-Vault"

def github_request(url, token):
    print(f"Fetching URL: {url} ...")
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "RPDevs-Project-Sync")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def fetch_org_issues(token):
    # Fetch open issues/PRs across all organization repos
    # We query the org issues endpoint which fetches all issues for the org
    issues = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{ORG}/issues?filter=all&state=open&per_page=100&page={page}"
        data = github_request(url, token)
        if not data:
            break
        issues.extend(data)
        if len(data) < 100:
            break
        page += 1
    return issues

def generate_roadmap(token):
    issues = fetch_org_issues(token)
    
    lines = []
    lines.append(f"Last Synced: `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`\n")
    
    if not issues:
        lines.append("### 🟢 No Active Issues or PRs found\n")
        lines.append("All repository queues are currently clear!")
        return "\n".join(lines)
        
    prs_grouped = {}
    issues_grouped = {}
    
    for item in issues:
        # Determine if it is a PR or Issue
        is_pr = "pull_request" in item
        repo_name = item.get("repository", {}).get("name", "Unknown")
        title = item.get("title", "No Title")
        number = item.get("number")
        html_url = item.get("html_url", "#")
        user = item.get("user", {}).get("login", "unknown")
        
        target_dict = prs_grouped if is_pr else issues_grouped
        if repo_name not in target_dict:
            target_dict[repo_name] = []
        target_dict[repo_name].append({
            "title": title,
            "number": number,
            "url": html_url,
            "user": user
        })
        
    # Group outputs
    if prs_grouped:
        lines.append("### 🔍 Open Pull Requests (Requires Review)")
        for repo, pr_list in sorted(prs_grouped.items()):
            lines.append(f"- **`RPDevs-Vault/{repo}`**")
            for pr in pr_list:
                lines.append(f"  - [PR #{pr['number']}: {pr['title']}]({pr['url']}) by @{pr['user']}")
        lines.append("")
        
    if issues_grouped:
        lines.append("### 📋 Open Tasks & Issues")
        for repo, issue_list in sorted(issues_grouped.items()):
            lines.append(f"- **`RPDevs-Vault/{repo}`**")
            for issue in issue_list:
                lines.append(f"  - [Issue #{issue['number']}: {issue['title']}]({issue['url']})")
        lines.append("")
        
    return "\n".join(lines)

def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("SYNC_TOKEN")
    if not token:
        print("Error: GH_TOKEN or SYNC_TOKEN environment variable is required", file=sys.stderr)
        sys.exit(1)
        
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        readme_path = "/home/llmuser/projects/managers/workspace-manager/README.md"
        
    if not os.path.exists(readme_path):
        print(f"Error: README.md not found", file=sys.stderr)
        sys.exit(1)
        
    with open(readme_path, "r") as f:
        content = f.read()
        
    start_tag = "<!-- ROADMAP_START -->"
    end_tag = "<!-- ROADMAP_END -->"
    
    if start_tag not in content or end_tag not in content:
        print("Warning: Roadmap tags not found in README.md. Appending report at the end.")
        roadmap_content = generate_roadmap(token)
        new_content = content + "\n\n" + start_tag + "\n" + roadmap_content + "\n" + end_tag + "\n"
    else:
        roadmap_content = generate_roadmap(token)
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find(end_tag)
        new_content = content[:start_idx] + "\n\n" + roadmap_content + "\n\n" + content[end_idx:]
        
    with open(readme_path, "w") as f:
        f.write(new_content)
        
    print("Project roadmap updated successfully!")

if __name__ == "__main__":
    main()
