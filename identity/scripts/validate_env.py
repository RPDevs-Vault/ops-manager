#!/usr/bin/env python3
import os
import sys
import json
import re

def validate_env():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "schemas", "env.schema.json")
    env_path = os.path.expanduser("~/.env")

    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)

    with open(schema_path, "r") as f:
        schema = json.load(f)

    # Simple env loader
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    else:
        # Load from os.environ as fallback
        for key in schema.get("properties", {}).keys():
            if key in os.environ:
                env_vars[key] = os.environ[key]

    errors = []
    
    # Required keys check
    for req in schema.get("required", []):
        if req not in env_vars:
            errors.append(f"Missing required environment variable: {req}")

    # Regex patterns check
    properties = schema.get("properties", {})
    for key, val in env_vars.items():
        if key in properties:
            pattern = properties[key].get("pattern")
            if pattern and not re.match(pattern, val):
                errors.append(f"Variable {key} does not match security format constraint.")

    if errors:
        print("❌ Environment Validation Failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    
    print("✅ Environment variables match validation schema.")
    sys.exit(0)

if __name__ == "__main__":
    validate_env()
