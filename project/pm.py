import os
import sys
import argparse
import subprocess
from datetime import datetime

class ProjectManager:
    def __init__(self):
        self.root = os.getcwd()
        self.inventory_path = os.path.join(self.root, ".gemini/docs/projects/INVENTORY.md")
        self.template_dir = os.path.join(self.root, "projectmanager/templates")
        self.core_dir = os.path.join(self.root, "projectmanager/core")

    def setup_pmo(self):
        """Initializes the global PMO directory in the workspace."""
        pmo_dir = os.path.join(self.root, ".gemini/pmo")
        print(f"[*] Initializing Workspace PMO at {pmo_dir}...")
        
        for subdir in ["skills", "artifacts", "reference"]:
            src = os.path.join(self.core_dir, subdir)
            dest = os.path.join(pmo_dir, subdir)
            if os.path.exists(src):
                subprocess.run(["mkdir", "-p", dest], check=True)
                subprocess.run(f"cp -r {src}/* {dest}/", shell=True, check=True)
        
        print("[+] PMO Setup Complete. Workspace is now PMBOK 8 Compliant.")

    def get_last_active(self, count=5):
        """Finds the last N active projects based on file modifications."""
        print(f"[*] Fetching last {count} active projects (excluding docs)...")
        cmd = [
            "find", ".", "-maxdepth", "4", "-type", "f", 
            "-not", "-name", "GEMINI.md", "-not", "-name", "README.md",
            "-not", "-path", "*/.*", "-not", "-path", "./.gemini/*",
            "-not", "-path", "./llmdata/*",
            "-printf", "%T@ %p\n"
        ]
        try:
            output = subprocess.check_output(cmd).decode()
            lines = output.strip().split("\n")
            # Sort by timestamp, get unique project names
            lines.sort(key=lambda x: float(x.split()[0]), reverse=True)
            projects = []
            seen = set()
            for line in lines:
                path = line.split()[1]
                parts = path.split('/')
                if len(parts) > 1:
                    proj = parts[1]
                    if proj not in seen and proj != ".":
                        projects.append(proj)
                        seen.add(proj)
                if len(projects) >= count:
                    break
            
            for p in projects:
                print(f"  - {p}")
        except Exception as e:
            print(f"[!] Error: {e}")

    def scan(self):
        """Updates the workspace inventory."""
        print("[*] Updating workspace inventory...")
        dirs = [d for d in os.listdir(self.root) if os.path.isdir(d) and not d.startswith(".")]
        dirs.sort()
        
        checkpoint_dir = os.path.expanduser("~/.gemini/checkpoints")

        lines = [
            "# Workspace Project Inventory\n",
            "This file provides a summary of all top-level project directories in the workspace.\n",
            "## Project Documentation Status\n",
            "| Directory | Documentation Found | Summary / Title |\n",
            "| :--- | :--- | :--- |\n"
        ]

        for d in dirs:
            docs = []
            summary = "Baseline Initialized"
            gemini_path = os.path.join(d, ".gemini/GEMINI.md")
            readme_path = os.path.join(d, "README.md")
            
            # Check for checkpoints
            latest_checkpoint = None
            if os.path.exists(checkpoint_dir):
                checkpoints = [c for c in os.listdir(checkpoint_dir) if c.startswith(f"checkpoint_{d}_") and c.endswith(".md")]
                if checkpoints:
                    checkpoints.sort(reverse=True)
                    latest_checkpoint = os.path.join(checkpoint_dir, checkpoints[0])
                    docs.append("`[Checkpoint Active]`")

            if os.path.exists(gemini_path):
                docs.append("`.gemini/GEMINI.md`")
                with open(gemini_path, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith("#"):
                        summary = first_line.replace("#", "").strip()
            
            if os.path.exists(readme_path):
                docs.append("`README.md`")
                if summary == "Baseline Initialized":
                    with open(readme_path, 'r') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith("#"):
                            summary = first_line.replace("#", "").strip()

            # If we found a checkpoint, maybe extract a snippet or append a note
            if latest_checkpoint:
                summary += " **(State: See Checkpoint)**"

            docs_str = ", ".join(docs) if docs else "None"
            lines.append(f"| **{d}** | {docs_str} | {summary} |\n")

        with open(self.inventory_path, 'w') as f:
            f.writelines(lines)
            f.write(f"\n---\n*Last scanned: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        print(f"[+] Inventory updated at {self.inventory_path}")

    def scaffold(self, name, tier="Tier-4"):
        """Creates a new project structure with PMO Spectrum baseline."""
        proj_dir = os.path.join(self.root, name)
        gemini_dir = os.path.join(proj_dir, ".gemini")
        os.makedirs(gemini_dir, exist_ok=True)

        # Create standard directories
        for std_dir in ["docs", "logs", "tmp", "bin", "tools"]:
            os.makedirs(os.path.join(proj_dir, std_dir), exist_ok=True)

        # Methodology Selection
        methodology = {
            "Tier-1": "Waterfall-Hybrid",
            "Tier-2": "Hybrid",
            "Tier-3": "Agile/Scrum",
            "Tier-4": "Lean/Kanban"
        }.get(tier, "Lean/Kanban")

        print(f"[*] Applying {tier} ({methodology}) governance baseline...")

        # Inject Governance Artifacts for Tier 1 & 2
        if tier in ["Tier-1", "Tier-2"]:
            charter_src = os.path.join(self.core_dir, "artifacts/initiating/A04-project-charter-template.md")
            if os.path.exists(charter_src):
                with open(charter_src, 'r') as f:
                    content = f.read()
                with open(os.path.join(proj_dir, "docs/A04-PROJECT-CHARTER.md"), 'w') as f:
                    f.write(content.replace("[FIELD: Full name of the project]", name))

        # Create GEMINI.md from template
        template_path = os.path.join(self.template_dir, "BASELINE_GEMINI.md")
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                content = f.read()
            with open(os.path.join(gemini_dir, "GEMINI.md"), 'w') as f:
                f.write(content.replace("Baseline Manager", f"{tier} Manager").replace("METHODOLOGY", methodology))
        
        # Create README.md
        with open(os.path.join(proj_dir, "README.md"), 'w') as f:
            f.write(f"# {name}\n\nProject initialized under the **{tier}** ({methodology}) spectrum.\n\n---\n*Managed by Gemini PMO Director (High-Fidelity Engineering Standard)*\n")
        
        print(f"[+] Scaffolded project: {name}")

    def audit(self, name):
        """Audits a project for compliance and waste (TIMWOODS)."""
        print(f"[*] Auditing project: {name} for TIMWOODS defects...")
        proj_dir = os.path.join(self.root, name)
        
        issues = []
        # Mandatory File Verification
        if not os.path.exists(os.path.join(proj_dir, ".gemini/GEMINI.md")):
            issues.append("DEFECT: Missing .gemini/GEMINI.md (Agent Instructions)")
        
        # Placeholder Verification (Waste: Over-processing)
        try:
            grep_out = subprocess.check_output(["grep", "-r", r"\[...\]", proj_dir]).decode()
            if grep_out:
                issues.append("WASTE: Uninstantiated placeholders [ ... ] found in artifacts.")
        except subprocess.CalledProcessError:
            pass

        # State Verification
        if not os.path.exists(os.path.join(proj_dir, "README.md")):
            issues.append("DEFECT: Missing README.md (Human Overview)")

        # Output results
        if not issues:
            print("[+] Audit Passed: Project is Lean and Compliant.")
        else:
            print("[!] Audit Findings:")
            for issue in issues:
                print(f"  - {issue}")

def main():
    pm = ProjectManager()
    parser = argparse.ArgumentParser(description="Gemini Workspace Project Manager CLI - Realignment V2")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("scan", help="Update workspace inventory")
    subparsers.add_parser("status", help="Show last 5 active projects")
    subparsers.add_parser("setup-pmo", help="Initialize workspace PMO standards")
    
    audit_parser = subparsers.add_parser("audit", help="Audit a project for compliance")
    audit_parser.add_argument("name", help="Name of the project directory to audit")
    
    scaffold_parser = subparsers.add_parser("scaffold", help="Initialize a new project")
    scaffold_parser.add_argument("name", help="Name of the project directory")
    scaffold_parser.add_argument("--tier", choices=["Tier-1", "Tier-2", "Tier-3", "Tier-4"], default="Tier-4")

    args = parser.parse_args()

    if args.command == "scan":
        pm.scan()
    elif args.command == "status":
        pm.get_last_active()
    elif args.command == "scaffold":
        pm.scaffold(args.name, args.tier)
    elif args.command == "setup-pmo":
        pm.setup_pmo()
    elif args.command == "audit":
        pm.audit(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
