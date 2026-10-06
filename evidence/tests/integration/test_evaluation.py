import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from vxn_ramnet.evaluation.manifest import DatasetManifest, load_dataset
from vxn_ramnet.evaluation.runner import METHODS, run_evaluation
from vxn_ramnet.evaluation.synthetic import generate_synthetic_dataset
from vxn_ramnet.io.checksums import sha256_file


def test_complete_evaluation_retains_numeric_raw_evidence_and_denominators(tmp_path):
    manifest_path = generate_synthetic_dataset(tmp_path / "data")
    payload = json.loads(manifest_path.read_text())
    payload["queries"] = [payload["queries"][i] for i in (0, 24, 48, 72)]
    manifest_path.write_text(json.dumps(payload))
    report = run_evaluation(manifest_path, tmp_path / "evidence", repeats=1, warmups=0)
    assert set(report["methods"]) == set(METHODS)
    for method in report["methods"].values():
        assert method["metrics"]["journeys"] == 4
        assert method["metrics"]["unknown_journeys"] == 1
        assert method["classification_timing"]["samples"] == 4
    default = report["methods"]["vxn_default"]["metrics"]
    assert default["correct_known"] == 2
    assert default["unknown_false_accepts"] == 0
    hashes = json.loads((tmp_path / "evidence/checksums.json").read_text())
    assert all(sha256_file(tmp_path / "evidence" / p) == digest for p, digest in hashes.items())
    assert "threshold-sweep.csv" in hashes
    with pytest.raises(FileExistsError):
        run_evaluation(manifest_path, tmp_path / "evidence", repeats=1, warmups=0)


def test_manifest_rejects_checksum_duplicates_and_session_leakage(tmp_path):
    path = generate_synthetic_dataset(tmp_path / "data")
    payload = json.loads(path.read_text())
    payload["purpose"] = "held_out"
    payload["learning"]["split"] = "enrollment"
    for record in payload["queries"]:
        record["split"] = "test"
    payload["queries"][0]["session_id"] = payload["learning"]["session_id"]
    with pytest.raises(ValidationError):
        DatasetManifest.model_validate(payload)
    payload["queries"][0]["session_id"] = "independent-session"
    payload["queries"][1]["sha256"] = payload["queries"][0]["sha256"]
    with pytest.raises(ValidationError):
        DatasetManifest.model_validate(payload)


def test_manifest_checksum_failure_creates_no_output(tmp_path):
    path = generate_synthetic_dataset(tmp_path / "data")
    payload = json.loads(path.read_text())
    payload["queries"][0]["sha256"] = "0" * 64
    path.write_text(json.dumps(payload))
    with pytest.raises(Exception, match="checksum"):
        run_evaluation(path, tmp_path / "evidence", repeats=1, warmups=0)
    assert not (tmp_path / "evidence").exists()


def test_manifest_blocks_path_escape(tmp_path):
    path = generate_synthetic_dataset(tmp_path / "data")
    payload = json.loads(path.read_text())
    payload["learning"]["path"] = "../outside.npz"
    path.write_text(json.dumps(payload))
    with pytest.raises(Exception, match="contained"):
        load_dataset(path)


def test_fixture_manifest_is_valid_without_tensorflow():
    path = Path(__file__).resolve().parents[2] / "benchmarks/manifests/notebook04.json"
    manifest, learning, queries = load_dataset(path)
    assert manifest.purpose == "regression"
    assert learning.embeddings.shape == (270, 1280)
    assert len(queries) == 2
