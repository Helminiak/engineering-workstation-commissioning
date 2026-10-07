#!/usr/bin/env python3
"""Read-only verification of the authorized private repository and task branch."""

import datetime
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "Helminiak/engineering-workstation-commissioning"
BRANCH = "commissioning/main-work"


def run(args):
    p = subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, timeout=60, check=False
    )
    if p.returncode:
        raise RuntimeError(f"{args[0]} read check failed (exit {p.returncode})")
    return p.stdout.strip()


def main():
    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "repository": REPO,
        "branch": BRANCH,
        "operation": "read-only verification",
    }
    try:
        login = run(["gh", "api", "user", "--jq", ".login"])
        assert login == "Helminiak", "Unexpected GitHub account"
        metadata = json.loads(
            run(
                [
                    "gh",
                    "repo",
                    "view",
                    REPO,
                    "--json",
                    "nameWithOwner,isPrivate,url,viewerPermission",
                ]
            )
        )
        assert metadata["nameWithOwner"] == REPO and metadata["isPrivate"], (
            "Repository identity/privacy mismatch"
        )
        assert metadata["viewerPermission"] in ["ADMIN", "MAINTAIN", "WRITE"], (
            "Insufficient repository permissions"
        )
        branch = run(["git", "branch", "--show-current"])
        assert branch == BRANCH, "Unexpected local branch"
        origin = run(["git", "remote", "get-url", "origin"])
        assert origin in [
            f"https://github.com/{REPO}.git",
            f"https://github.com/{REPO}",
        ], "Unexpected origin"
        local = run(["git", "rev-parse", "HEAD"])
        remote_line = run(
            ["git", "ls-remote", "--exit-code", "origin", f"refs/heads/{BRANCH}"]
        )
        remote = remote_line.split()[0]
        api = run(
            ["gh", "api", f"repos/{REPO}/git/ref/heads/{BRANCH}", "--jq", ".object.sha"]
        )
        assert local == remote == api, "Local/remote/API commit mismatch"
        report.update(
            status="PASS",
            login=login,
            metadata=metadata,
            local_commit=local,
            remote_commit=remote,
            api_commit=api,
            privacy="PRIVATE",
            limitation="Read/branch/commit/push verified; PR creation, merge and deployment NOT_TESTED and not authorized.",
        )
    except (
        OSError,
        subprocess.SubprocessError,
        ValueError,
        AssertionError,
        RuntimeError,
        KeyError,
    ) as e:
        report.update(status="FAIL", error_type=type(e).__name__, reason=str(e))
    (ROOT / "evidence/github-remote-verification.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
