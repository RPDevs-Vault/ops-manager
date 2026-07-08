#!/usr/bin/env python3
import urllib.request
import sys
import json

TARGET_ENDPOINTS = {
    "GitHub API": "https://api.github.com",
    "GitHub Status": "https://www.githubstatus.com/api/v2/status.json",
    "GHCR Registry": "https://ghcr.io"
}

def ping_targets():
    results = {}
    has_failed = False
    
    for name, url in TARGET_ENDPOINTS.items():
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (RPDevs-Monitor)'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.getcode()
                results[name] = {"status": "ONLINE", "code": status}
        except Exception as e:
            results[name] = {"status": "OFFLINE", "error": str(e)}
            has_failed = True

    print(json.dumps(results, indent=2))
    
    if has_failed:
        print("❌ One or more endpoints are OFFLINE.")
        sys.exit(1)
        
    print("✅ All endpoints are reachable.")
    sys.exit(0)

if __name__ == "__main__":
    ping_targets()
