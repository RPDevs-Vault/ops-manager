#!/usr/bin/env python3
import json
import os
import shutil
import socket
import psutil
from datetime import datetime, timezone

def collect_telemetry():
    host = socket.gethostname()
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memory
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    
    # Disk (Sharedroot)
    shared_root = "/mnt/sharedroot"
    if os.path.exists(shared_root):
        disk = shutil.disk_usage(shared_root)
        disk_percent = (disk.used / disk.total) * 100
    else:
        disk_percent = 0.0

    # Temperature (if available)
    temps = {}
    try:
        if hasattr(psutil, "sensors_temperatures"):
            temp_sensors = psutil.sensors_temperatures()
            for name, entries in temp_sensors.items():
                if entries:
                    temps[name] = entries[0].current
    except Exception:
        pass

    telemetry = {
        "hostname": host,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_percent": cpu_percent,
        "memory_percent": mem_percent,
        "sharedroot_disk_percent": round(disk_percent, 2),
        "temperatures": temps
    }
    
    # Write to a shared NFS location that the manager can read, or local
    output_dir = "/mnt/sharedroot/github_runners/shared/telemetry"
    try:
        os.makedirs(output_dir, exist_ok=True)
    except PermissionError:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "telemetry")
        os.makedirs(output_dir, exist_ok=True)
        
    try:
        file_path = os.path.join(output_dir, f"{host}_telemetry.json")
        with open(file_path, "w") as f:
            json.dump(telemetry, f, indent=2)
        print(f"Telemetry written to {file_path}")
    except Exception as e:
        print(f"Failed to write telemetry: {e}. Data: {telemetry}")

if __name__ == "__main__":
    collect_telemetry()
