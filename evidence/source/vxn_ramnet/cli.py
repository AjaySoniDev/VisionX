from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from vxn_ramnet.config import load_config
from vxn_ramnet.config.models import PipelineConfig
from vxn_ramnet.core.exceptions import VxnRamNetError
from vxn_ramnet.evaluation.runner import run_evaluation
from vxn_ramnet.evaluation.synthetic import generate_synthetic_dataset
from vxn_ramnet.pipeline import VxnPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vxn-ramnet", description="VXN-RAMNet camera-only constrained route-memory research pipeline"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run the complete pipeline from a JSON/YAML config")
    run.add_argument("--config", required=True, type=Path)
    validate = sub.add_parser("validate-config", help="Validate and normalize a config without running")
    validate.add_argument("--config", required=True, type=Path)
    sub.add_parser("print-config-schema", help="Print the current JSON schema")
    inspect = sub.add_parser("inspect-run", help="Print a concise run summary")
    inspect.add_argument("run_directory", type=Path)
    evaluate = sub.add_parser("evaluate", help="Evaluate cached descriptors from a checksum-pinned dataset manifest")
    evaluate.add_argument("--manifest", required=True, type=Path)
    evaluate.add_argument("--output", required=True, type=Path)
    evaluate.add_argument("--repeats", type=int, default=5)
    evaluate.add_argument("--warmups", type=int, default=1)
    synthetic = sub.add_parser("generate-synthetic", help="Generate clearly labeled vector stress scenarios")
    synthetic.add_argument("--output", required=True, type=Path)
    synthetic.add_argument("--seed", type=int, default=2026)
    return parser


def _execute(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "generate-synthetic":
        print(generate_synthetic_dataset(args.output, seed=args.seed).as_posix())
        return 0
    if args.command == "evaluate":
        report = run_evaluation(args.manifest, args.output, repeats=args.repeats, warmups=args.warmups)
        print(
            json.dumps(
                {
                    "dataset_id": report["dataset_id"],
                    "purpose": report["purpose"],
                    "report": (args.output / "report.json").as_posix(),
                },
                indent=2,
            )
        )
        return 0
    if args.command == "run":
        result = VxnPipeline(load_config(args.config)).run()
        print(
            json.dumps(
                {
                    "run_id": result.run_id,
                    "run_directory": result.run_directory.as_posix(),
                    "report_files": result.report_files,
                },
                indent=2,
            )
        )
        return 0
    if args.command == "validate-config":
        config = load_config(args.config)
        print(json.dumps(config.model_dump(mode="json"), indent=2))
        return 0
    if args.command == "print-config-schema":
        print(json.dumps(PipelineConfig.model_json_schema(), indent=2))
        return 0
    if args.command == "inspect-run":
        summary = args.run_directory / "reports" / "summary.json"
        if not summary.is_file():
            raise FileNotFoundError(f"Run summary not found: {summary}")
        data = json.loads(summary.read_text(encoding="utf-8"))
        print(
            json.dumps(
                {
                    "run_id": data.get("run_id"),
                    "implementation_status": data.get("implementation_status"),
                    "route_quality": data.get("route_memory", {}).get("quality", {}),
                    "query_results": data.get("query_results", []),
                },
                indent=2,
            )
        )
        return 0
    return 2


def main(argv: list[str] | None = None) -> int:
    try:
        return _execute(argv)
    except (VxnRamNetError, OSError, ValueError, RuntimeError, ValidationError) as exc:
        print(f"vxn-ramnet: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
