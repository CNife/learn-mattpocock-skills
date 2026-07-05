# /// script
# requires-python = ">=3.11"
# ///
"""Check upstream mattpocock/skills for updates against the translation manifest.

Read-only: fetches origin, diffs each translated skill's recorded ``source_commit``
against ``origin/main``, and reports which skills changed plus which new skills
exist in engineering/productivity. Does NOT advance the submodule or modify the
manifest — advancing the pointer happens only after explicit user confirmation
(see ``.agents/skills/check-upstream-updates/SKILL.md``).

Usage::

    uv run --script scripts/check-updates.py           # human-readable
    uv run --script scripts/check-updates.py --json    # machine-readable
    uv run --script scripts/check-updates.py --ref origin/v1.0.1

Exit codes: 0 = clean; 1 = environment error (submodule/manifest missing);
2 = data error (a recorded source_commit is not in upstream history).
"""
import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SUBMODULE = REPO_ROOT / "mattpocock-skills"
MANIFEST = REPO_ROOT / "docs" / "translated-skills.json"
NEW_SKILL_BUCKETS = ("engineering", "productivity")

EXIT_OK = 0
EXIT_ENV_ERROR = 1      # submodule or manifest missing
EXIT_DATA_ERROR = 2     # a source_commit is not in upstream history


class Status(str, Enum):
    CHANGED = "changed"
    UNCHANGED = "unchanged"
    MISSING = "missing"                    # skill deleted upstream
    MOVED = "moved"                        # source_path changed (bucket moved)
    UNKNOWN_BASELINE = "unknown_baseline"  # source_commit not in upstream history


# ── pure logic seams (unit-tested) ──────────────────────────────────────────

def find_skill_path(skills_root: Path, name: str) -> str | None:
    """Return ``skills/<bucket>/<name>`` if the skill exists in any bucket, else None."""
    if not skills_root.is_dir():
        return None
    for bucket in sorted(skills_root.iterdir()):
        if bucket.is_dir() and (bucket / name).is_dir():
            return f"skills/{bucket.name}/{name}"
    return None


def compute_new_skills(skills_root: Path, manifest_names: set[str]) -> set[str]:
    """Names present in engineering+productivity but absent from the manifest."""
    new: set[str] = set()
    if not skills_root.is_dir():
        return new
    for bucket_name in NEW_SKILL_BUCKETS:
        bucket = skills_root / bucket_name
        if not bucket.is_dir():
            continue
        for d in bucket.iterdir():
            if d.is_dir() and d.name not in manifest_names:
                new.add(d.name)
    return new


def load_manifest(path: Path) -> tuple[dict, dict]:
    """Return ``(upstream_meta, skills_dict)``."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("upstream", {}), data.get("skills", {})


def group_by_status(results: list["SkillResult"]) -> dict[Status, list["SkillResult"]]:
    """Bucket results by status — single source for both JSON and human output."""
    groups: dict[Status, list[SkillResult]] = {}
    for r in results:
        groups.setdefault(r.status, []).append(r)
    return groups


# ── git helpers ──────────────────────────────────────────────────────────────

def _git(repo: Path, *args: str) -> str:
    r = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed in {repo}:\n{r.stderr.strip()}"
        )
    return r.stdout


def get_ref_commit(repo: Path, ref: str) -> str:
    """Resolve a ref (e.g. ``origin/main``) to a full commit hash."""
    return _git(repo, "rev-parse", ref).strip()


def commit_exists(repo: Path, sha: str) -> bool:
    """True iff ``sha`` resolves to a commit in ``repo``."""
    r = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"],
        capture_output=True, text=True,
    )
    return r.returncode == 0


# ── result model ────────────────────────────────────────────────────────────

@dataclass
class SkillResult:
    name: str
    source_commit: str
    recorded_path: str | None
    current_path: str | None
    translated_at: str
    status: Status
    changed_files: list[str] = field(default_factory=list)
    commit_range: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "source_commit": self.source_commit,
            "recorded_path": self.recorded_path,
            "current_path": self.current_path,
            "translated_at": self.translated_at,
            "status": self.status.value,
            "changed_files": self.changed_files,
            "commit_range": self.commit_range,
        }

    def format_header(self) -> str:
        return f"  {self.name}  (translated {self.translated_at}, baseline {self.source_commit[:8]})"


# ── core check ──────────────────────────────────────────────────────────────

def check(ref: str | None, json_out: bool) -> int:
    if not SUBMODULE.is_dir():
        print(
            f"error: submodule not found at {SUBMODULE}\n"
            f"  run: git submodule update --init",
            file=sys.stderr,
        )
        return EXIT_ENV_ERROR
    if not MANIFEST.is_file():
        print(f"error: manifest not found at {MANIFEST}", file=sys.stderr)
        return EXIT_ENV_ERROR

    upstream, skills = load_manifest(MANIFEST)
    target_ref = ref or f"origin/{upstream.get('ref', 'main')}"

    print(f"fetching upstream ({upstream.get('url', '?')})...", file=sys.stderr)
    _git(SUBMODULE, "fetch", "origin")
    target = get_ref_commit(SUBMODULE, target_ref)

    skills_root = SUBMODULE / "skills"
    results: list[SkillResult] = []
    for name, info in skills.items():
        sc = info["source_commit"]
        recorded = info.get("source_path")
        current = find_skill_path(skills_root, name)
        translated_at = info.get("translated_at", "")
        rng = f"{sc[:8]}..{target[:8]}"

        if current is None:
            results.append(SkillResult(
                name=name, source_commit=sc, recorded_path=recorded,
                current_path=None, translated_at=translated_at, status=Status.MISSING,
            ))
            continue

        if not commit_exists(SUBMODULE, sc):
            results.append(SkillResult(
                name=name, source_commit=sc, recorded_path=recorded,
                current_path=current, translated_at=translated_at,
                status=Status.UNKNOWN_BASELINE,
            ))
            continue

        out = _git(SUBMODULE, "diff", "--name-status", f"{sc}..{target}", "--", current)
        files = [line for line in out.splitlines() if line.strip()]

        if current != recorded:
            # bucket moved upstream — flag even if content is unchanged
            results.append(SkillResult(
                name=name, source_commit=sc, recorded_path=recorded,
                current_path=current, translated_at=translated_at,
                status=Status.MOVED, changed_files=files, commit_range=rng,
            ))
        elif files:
            results.append(SkillResult(
                name=name, source_commit=sc, recorded_path=recorded,
                current_path=current, translated_at=translated_at,
                status=Status.CHANGED, changed_files=files, commit_range=rng,
            ))
        else:
            results.append(SkillResult(
                name=name, source_commit=sc, recorded_path=recorded,
                current_path=current, translated_at=translated_at,
                status=Status.UNCHANGED,
            ))

    new_names = sorted(compute_new_skills(skills_root, set(skills)))
    new_with_path = [(n, find_skill_path(skills_root, n)) for n in new_names]

    if json_out:
        print(json.dumps(
            _to_json(upstream, target_ref, target, results, new_with_path),
            indent=2, ensure_ascii=False,
        ))
    else:
        _print_human(upstream, target_ref, target, results, new_with_path)

    has_bad_baseline = any(r.status == Status.UNKNOWN_BASELINE for r in results)
    return EXIT_DATA_ERROR if has_bad_baseline else EXIT_OK


def _to_json(upstream, target_ref, target, results, new_with_path):
    groups = group_by_status(results)
    return {
        "upstream": upstream,
        "target_ref": target_ref,
        "target_commit": target,
        "summary": {s.value: len(groups.get(s, [])) for s in Status} | {"new": len(new_with_path)},
        "changed": [r.to_dict() for r in groups.get(Status.CHANGED, [])],
        "moved": [r.to_dict() for r in groups.get(Status.MOVED, [])],
        "missing": [r.to_dict() for r in groups.get(Status.MISSING, [])],
        "unknown_baseline": [r.to_dict() for r in groups.get(Status.UNKNOWN_BASELINE, [])],
        "new": [{"name": n, "path": p} for n, p in new_with_path],
    }


def _print_human(upstream, target_ref, target, results, new_with_path):
    groups = group_by_status(results)
    changed = groups.get(Status.CHANGED, [])
    moved = groups.get(Status.MOVED, [])
    missing = groups.get(Status.MISSING, [])
    unknown = groups.get(Status.UNKNOWN_BASELINE, [])
    unchanged = groups.get(Status.UNCHANGED, [])

    print(f"upstream: {upstream.get('url', '?')}")
    print(f"target:   {target_ref} ({target[:8]})")
    print()

    if changed:
        print(f"Changed skills ({len(changed)}) — need re-translation:")
        for r in changed:
            print(r.format_header())
            for f in r.changed_files:
                print(f"    {f}")
            print(f"    commits {r.commit_range}")
        print()

    if moved:
        print(f"Moved skills ({len(moved)}) — bucket changed upstream, refresh source_path:")
        for r in moved:
            print(f"  {r.name}  {r.recorded_path} -> {r.current_path}")
        print()

    if unknown:
        print(f"Unknown baseline ({len(unknown)}) — source_commit not in upstream history:")
        for r in unknown:
            print(f"  {r.name}  (recorded {r.source_commit[:8]})")
        print()

    if missing:
        print(f"Missing upstream ({len(missing)}) — skill no longer exists:")
        for r in missing:
            print(f"  {r.name}  (was {r.recorded_path})")
        print()

    print(f"Unchanged: {len(unchanged)}")
    print()

    if new_with_path:
        print(
            f"New translatable skills ({len(new_with_path)}) — "
            f"in {NEW_SKILL_BUCKETS}, not yet translated:"
        )
        for n, p in new_with_path:
            print(f"  {n}  at {p}")
    else:
        print(f"No new translatable skills in {NEW_SKILL_BUCKETS}.")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Check upstream mattpocock/skills for updates.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--ref", help="target ref (default: origin/<manifest ref>)")
    p.add_argument("--json", action="store_true", help="machine-readable JSON output")
    args = p.parse_args()
    return check(args.ref, args.json)


if __name__ == "__main__":
    sys.exit(main())
