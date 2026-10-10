import json
import tempfile
from pathlib import Path

import pytest

from malexgen.core.generator import MalExtGenerator


@pytest.fixture
def temp_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_generator_init(temp_output):
    gen = MalExtGenerator(output_dir=temp_output)
    assert gen.output_dir == temp_output


def test_generate_basic(temp_output):
    gen = MalExtGenerator(output_dir=temp_output)
    ext_dir = gen.generate("vpn", "cookie_stealer")

    assert ext_dir.exists()
    assert (ext_dir / "manifest.json").exists()
    assert (ext_dir / "background.js").exists()
    assert (ext_dir / "content.js").exists()
    assert (ext_dir / "popup.html").exists()
    assert (ext_dir / "popup.js").exists()
    assert (ext_dir / "styles.css").exists()
    assert (ext_dir / "README.md").exists()
    assert (ext_dir / "REPORT.md").exists()
    assert (ext_dir / "meta.json").exists()


def test_manifest_is_valid_json(temp_output):
    gen = MalExtGenerator(output_dir=temp_output)
    ext_dir = gen.generate("adblock", "keylogger")

    manifest = json.loads((ext_dir / "manifest.json").read_text())
    assert manifest["manifest_version"] == 3
    assert "name" in manifest
    assert "version" in manifest
    assert "permissions" in manifest


def test_meta_contains_ids(temp_output):
    gen = MalExtGenerator(output_dir=temp_output)
    ext_dir = gen.generate("translator", "form_grabber")

    meta = json.loads((ext_dir / "meta.json").read_text())
    assert meta["legend_id"] == "translator"
    assert meta["payload_id"] == "form_grabber"


def test_unknown_legend_raises(temp_output):
    gen = MalExtGenerator(output_dir=temp_output)
    with pytest.raises(ValueError, match="легенда"):
        gen.generate("unknown_legend", "cookie_stealer")


def test_unknown_payload_raises(temp_output):
    gen = MalExtGenerator(output_dir=temp_output)
    with pytest.raises(ValueError, match="payload"):
        gen.generate("vpn", "unknown_payload")


def test_custom_output_name(temp_output):
    gen = MalExtGenerator(output_dir=temp_output)
    ext_dir = gen.generate("vpn", "cookie_stealer", output_name="my_test_ext")

    assert ext_dir.name == "my_test_ext"


def test_list_available(temp_output):
    gen = MalExtGenerator(output_dir=temp_output)
    available = gen.list_available()

    assert "legends" in available
    assert "payloads" in available
    assert len(available["legends"]) > 0
    assert len(available["payloads"]) > 0


@pytest.mark.parametrize("legend_id,payload_id", [
    ("vpn", "cookie_stealer"),
    ("adblock", "keylogger"),
    ("translator", "form_grabber"),
    ("password_manager", "session_hijacker"),
    ("dark_theme", "script_injector"),
])
def test_generate_multiple_combinations(temp_output, legend_id, payload_id):
    gen = MalExtGenerator(output_dir=temp_output)
    ext_dir = gen.generate(legend_id, payload_id)

    assert ext_dir.exists()
    assert (ext_dir / "manifest.json").exists()
