#!/usr/bin/env python3
"""Initialize a BP project workspace from BPClaw templates."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEMPLATE_MAP = {
    "inputs/0_background_and_goal.md": "background-goal-template.md",
    "research/1_source_log.md": "source-log-template.md",
    "outputs/2_bp_draft.md": "bp-draft-template.md",
    "outputs/3_liveppt_scene_map.md": "liveppt-scene-map-template.md",
}


def slugify(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "bp-project"


def write_text(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a reusable workspace for BP research and drafting."
    )
    parser.add_argument("project_name", help="Project name, e.g. textile-ai-bp")
    parser.add_argument("--out", default=".", help="Output base directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    template_dir = skill_dir / "assets" / "templates"

    if not template_dir.exists():
        raise SystemExit(f"Template directory missing: {template_dir}")

    project_root = Path(args.out).resolve() / slugify(args.project_name)
    project_root.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    skipped: list[Path] = []

    for rel_path, template_name in TEMPLATE_MAP.items():
        target = project_root / rel_path
        template_path = template_dir / template_name
        if not template_path.exists():
            raise SystemExit(f"Template missing: {template_path}")
        content = template_path.read_text(encoding="utf-8")
        changed = write_text(target, content, force=args.force)
        (created if changed else skipped).append(target)

    scorecard = project_root / "outputs/4_bp_review_scorecard.md"
    reflection = project_root / "outputs/5_reflection.md"

    scorecard_content = (
        "# BP评分卡\n\n"
        "- 总分：\n"
        "- 结论：\n"
        "- 最薄弱章节：\n"
        "- 下一轮改进动作：\n"
    )
    reflection_content = (
        "# 复盘沉淀\n\n"
        "## 本轮有效动作\n\n"
        "- \n\n"
        "## 本轮失效动作\n\n"
        "- \n\n"
        "## 人类反馈导致的关键修改\n\n"
        "- \n\n"
        "## 下一轮自动化改进项\n\n"
        "- \n"
    )

    for target, content in ((scorecard, scorecard_content), (reflection, reflection_content)):
        changed = write_text(target, content, force=args.force)
        (created if changed else skipped).append(target)

    print(f"BP workspace: {project_root}")
    if created:
        print("Created files:")
        for path in created:
            print(f"  + {path}")
    if skipped:
        print("Skipped existing files (use --force to overwrite):")
        for path in skipped:
            print(f"  - {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
