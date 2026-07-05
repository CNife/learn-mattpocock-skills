"""Tests for scripts/check-updates.py pure logic seams."""
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-updates.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_updates", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def mod():
    return _load_module()


@pytest.fixture
def skills_tree(tmp_path):
    """Fake mattpocock-skills/skills/ tree spanning several buckets."""
    base = tmp_path / "mattpocock-skills" / "skills"
    layout = [
        ("engineering", ["ask-matt", "tdd", "new-skill"]),
        ("productivity", ["grilling", "grill-me"]),
        ("in-progress", ["wayfinder"]),
        ("deprecated", ["old"]),
    ]
    for bucket, names in layout:
        for n in names:
            (base / bucket / n).mkdir(parents=True)
            (base / bucket / n / "SKILL.md").write_text(f"# {n}\n")
    return tmp_path / "mattpocock-skills"


def test_find_skill_path_engineering(mod, skills_tree):
    assert mod.find_skill_path(skills_tree / "skills", "ask-matt") == \
        "skills/engineering/ask-matt"


def test_find_skill_path_productivity(mod, skills_tree):
    assert mod.find_skill_path(skills_tree / "skills", "grilling") == \
        "skills/productivity/grilling"


def test_find_skill_path_missing(mod, skills_tree):
    assert mod.find_skill_path(skills_tree / "skills", "nope") is None


def test_compute_new_skills(mod, skills_tree):
    """New = (engineering + productivity dirs) - manifest names."""
    manifest_names = {"ask-matt", "grilling"}
    new = mod.compute_new_skills(skills_tree / "skills", manifest_names)
    # engineering: ask-matt, tdd, new-skill ; productivity: grilling, grill-me
    # minus {ask-matt, grilling} => {tdd, new-skill, grill-me}
    assert new == {"tdd", "new-skill", "grill-me"}


def test_compute_new_skills_ignores_other_buckets(mod, skills_tree):
    """in-progress (wayfinder) and deprecated (old) must NOT be flagged."""
    new = mod.compute_new_skills(skills_tree / "skills", set())
    assert "wayfinder" not in new
    assert "old" not in new
    assert new == {"ask-matt", "tdd", "new-skill", "grilling", "grill-me"}


def test_load_manifest(mod, tmp_path):
    m = {
        "upstream": {"url": "u", "ref": "main"},
        "skills": {
            "ask-matt": {
                "source_commit": "abc",
                "translated_at": "2026-01-01",
                "source_path": "skills/engineering/ask-matt",
            }
        },
    }
    f = tmp_path / "m.json"
    f.write_text(json.dumps(m))
    upstream, skills = mod.load_manifest(f)
    assert upstream["ref"] == "main"
    assert "ask-matt" in skills
    assert skills["ask-matt"]["source_commit"] == "abc"
