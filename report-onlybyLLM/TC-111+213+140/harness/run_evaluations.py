"""Run three isolated deeplogic-cli inspections with reproducible logging."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time

import yaml


OUT = Path(__file__).resolve().parents[1]
HARNESS = Path(__file__).resolve().parent
MODEL_CONFIG = Path(
    "/Users/a1234/Documents/project/gitlab/deeplogic-cli/.deeplogic/inspect_config.yaml"
)
CLI = Path("/Users/a1234/.browser-use-env/bin/deeplogic-cli")
CASES = ("TC-111", "TC-213", "TC-140")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", nargs="*", choices=CASES)
    parser.add_argument("--request-timeout", type=int, default=600)
    parser.add_argument("--check-level", choices=("L1", "L2", "L3"), default="L2")
    parser.add_argument("--concurrency", type=int, default=2)
    args = parser.parse_args()
    selected = tuple(args.cases) or CASES
    model = yaml.safe_load(MODEL_CONFIG.read_text())["model"]
    env = os.environ.copy()
    env.update(
        {
            "LLM_PROVIDER": model["provider"],
            "LLM_API_KEY": model["api_key"],
            "LLM_MODEL_ID": model["model_id"],
            "LLM_BASE_URL": model["base_url"],
            "DEEPLOGIC_COMPAT": "1",
            "PYTHONPATH": str(HARNESS)
            + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""),
        }
    )

    failed: list[str] = []
    for case in selected:
        run_dir = OUT / "runs" / case
        log_path = run_dir / "console.log"
        command = [
            str(CLI),
            "inspect",
            "--config",
            str(run_dir / "inspect_config.yaml"),
            "--check-level",
            args.check_level,
            "--verbose",
            "--timeout",
            "1800",
            "--token-budget",
            "200000",
            "--concurrency",
            str(args.concurrency),
            "--request-timeout",
            str(args.request_timeout),
        ]
        started = time.monotonic()
        print(f"[start] {case} at {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
        with log_path.open("w", encoding="utf-8") as log:
            process = subprocess.Popen(
                command,
                cwd=str(OUT),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            assert process.stdout is not None
            for line in process.stdout:
                sys.stdout.write(f"[{case}] {line}")
                sys.stdout.flush()
                log.write(line)
                log.flush()
            code = process.wait()
        elapsed = time.monotonic() - started
        print(f"[done] {case}: exit={code}, elapsed={elapsed:.1f}s", flush=True)
        if code != 0:
            failed.append(case)

    print(f"[summary] failed={','.join(failed) if failed else 'none'}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
