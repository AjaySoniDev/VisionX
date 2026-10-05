import json

import pytest

from vxn_ramnet.cli import main
from vxn_ramnet.config.loader import dump_config, load_config
from vxn_ramnet.config.models import PipelineConfig
from vxn_ramnet.core.exceptions import ConfigurationError


def test_cli_config_schema_and_friendly_failure(capsys, tmp_path):
    assert main(["print-config-schema"]) == 0
    assert json.loads(capsys.readouterr().out)["additionalProperties"] is False
    assert main(["validate-config", "--config", str(tmp_path / "missing.yaml")]) == 2
    assert "ConfigurationError" in capsys.readouterr().err
    assert main(["inspect-run", str(tmp_path)]) == 2


def test_config_paths_are_resolved_relative_to_config_file(tmp_path):
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    path = config_dir / "run.yaml"
    path.write_text(
        "project_root: ..\nlearning_video: {id: learning, path: learning.mp4}\nquery_videos: [{id: query-a, path: query.mp4}]\n"
    )
    config = load_config(path)
    assert config.project_root == tmp_path
    assert config.resolve_input(config.learning_video) == tmp_path / "learning.mp4"
    for suffix in (".json", ".yaml"):
        output = tmp_path / ("copy" + suffix)
        dump_config(config, output)
        assert load_config(output).model_dump() == config.model_dump()


def test_config_rejects_invalid_format_and_unknown_fields(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("unexpected: true")
    with pytest.raises(ConfigurationError):
        load_config(path)
    path.write_text("- invalid\n- root\n")
    with pytest.raises(ConfigurationError):
        load_config(path)


def test_resume_requires_explicit_id_and_excludes_overwrite():
    payload = {
        "learning_video": {"id": "learning", "path": "learn.mp4"},
        "query_videos": [{"id": "query-a", "path": "query.mp4"}],
    }
    with pytest.raises(ValueError):
        PipelineConfig.model_validate({**payload, "artifacts": {"resume": True}})
    with pytest.raises(ValueError):
        PipelineConfig.model_validate(
            {**payload, "artifacts": {"resume": True, "run_id": "run-test", "overwrite_existing_run": True}}
        )
