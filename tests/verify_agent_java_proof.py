import datetime
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
folder = ROOT / "scratch/local-agent-java-proof"
report = json.loads((folder / "report.json").read_text())
assert report["java"]["result"] == 385
assert report["java"]["javac_exit_code"] == 0 and report["java"]["java_exit_code"] == 0
assert (
    report["git"]["repository"] == str(ROOT)
    and report["git"]["branch"] == "commissioning/main-work"
)
p = subprocess.run(
    ["javac", "-Xlint:all", "-Werror", "EngineeringProbe.java"],
    cwd=folder,
    capture_output=True,
    text=True,
    check=True,
)
q = subprocess.run(
    ["java", "EngineeringProbe"], cwd=folder, capture_output=True, text=True, check=True
)
assert q.stdout.strip() == "JAVA_RESULT=385"
p = ROOT / "state/local-agent-java-proof.json"
state = json.loads(p.read_text())
state["status"] = "PASS"
state["independent_verification"] = {
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "javac_exit_code": 0,
    "java_exit_code": 0,
    "result": 385,
    "git_repository": str(ROOT),
    "correction": "Initial wrong fixture repository rejected, commissioning repo corrected by agent.",
}
p.write_text(json.dumps(state, indent=2) + "\n")
p.chmod(0o600)
(ROOT / "evidence/local-agent-java-verification.json").write_text(
    json.dumps(state["independent_verification"], indent=2) + "\n"
)
print(
    "PASS independent local-agent Java compile/execution and corrected commissioning Git inspection"
)
