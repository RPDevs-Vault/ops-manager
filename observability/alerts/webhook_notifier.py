#!/usr/bin/env python3
import urllib.request
import json
import os
import sys

def dispatch_alert(message):
    webhook_url = os.environ.get("ALERT_WEBHOOK_URL")
    if not webhook_url:
        print("Warning: ALERT_WEBHOOK_URL not set. Printing alert to stdout:")
        print(f"[ALERT] {message}")
        sys.exit(0)

    payload = {
        "text": f"🚨 **RPDevs-Vault Fleet Alert** 🚨\n{message}"
    }

    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            if res.getcode() == 200 or res.getcode() == 204:
                print("Alert dispatched successfully.")
            else:
                print(f"Failed to send alert. Status code: {res.getcode()}")
    except Exception as e:
        print(f"Error sending webhook alert: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: webhook_notifier.py <alert_message>")
        sys.exit(1)
    dispatch_alert(sys.argv[1])
