from pathlib import Path
import datetime
import hashlib
import json
import platform
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
proof = root / "proof"
proof.mkdir(exist_ok=True)
tests = subprocess.run([sys.executable, "-m", "unittest", "-v"], cwd=root, text=True, capture_output=True)
(proof / "tests.txt").write_text(tests.stdout + tests.stderr)
command = json.loads((root / "demo.json").read_text())
demo = subprocess.run([sys.executable, "main.py", *command], cwd=root, text=True, capture_output=True)
(proof / "demo.json").write_text(demo.stdout if demo.returncode == 0 else json.dumps({"stderr": demo.stderr}))
hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file() and not any(part in {"proof", ".git", "__pycache__"} for part in p.relative_to(root).parts)}
(proof / "sha256.json").write_text(json.dumps(hashes, indent=2) + "\n")
report = {"executed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "python": platform.python_version(), "platform": platform.system(), "tests_exit_code": tests.returncode, "demo_exit_code": demo.returncode, "demo_command": ["python", "main.py", *command], "scope": "Local synthetic fixtures; no remote security assessment", "ci_status": "Not asserted by this local report"}
(proof / "report.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
sys.exit(0 if tests.returncode == demo.returncode == 0 else 1)
