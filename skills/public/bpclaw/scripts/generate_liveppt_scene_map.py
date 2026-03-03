#!/usr/bin/env python3
"""Generate a LivePPT scene-map draft from BP markdown."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


def parse_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^##\s+(.+)$", text, re.MULTILINE))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        title = match.group(1).strip()
        body = text[start:end].strip()
        sections[title] = body
    return sections


def pick_points(section: str, limit: int = 3) -> list[str]:
    points = []
    for line in section.splitlines():
        normalized = line.strip()
        if normalized.startswith("- "):
            points.append(normalized[2:].strip())
        elif re.match(r"^\d+\.\s+", normalized):
            points.append(re.sub(r"^\d+\.\s+", "", normalized))
        if len(points) >= limit:
            break
    if not points:
        sentence = re.sub(r"\s+", " ", section).strip()
        if sentence:
            points = [sentence[:90] + ("..." if len(sentence) > 90 else "")]
    return points or ["待补充"]


def find_section(sections: dict[str, str], keyword: str) -> str:
    for title, body in sections.items():
        if keyword in title:
            return body
    return ""


def build_scene_map(bp_path: Path, content: str) -> str:
    sections = parse_sections(content)
    macro = find_section(sections, "宏观")
    micro = find_section(sections, "微观")
    strategy = find_section(sections, "战略")
    tactical = find_section(sections, "战术")
    resource = find_section(sections, "资源")
    vision = find_section(sections, "愿景")

    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "融资商业计划"
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    scene_points = {
        "S02 行业机会（宏观）": pick_points(macro),
        "S03 公司现状与问题（微观）": pick_points(micro),
        "S04 战略解法": pick_points(strategy),
        "S05 战术与短期抓手": pick_points(tactical),
        "S06 资源与执行保障": pick_points(resource),
        "S07 财务与资本回报预期": pick_points(vision),
    }

    lines = [
        "# LivePPT Scene Map（由BP自动生成）",
        "",
        "## 基本信息",
        "",
        f"- 来源文件：{bp_path}",
        f"- 生成时间：{now}",
        f"- 项目标题：{title}",
        "- 建议风格：minimal-editorial",
        "- 叙事主线：用可验证执行计划把行业机会转化为融资回报",
        "",
        "## 场景规划",
        "",
        "### S01 封面",
        "",
        f"- 核心信息：{title}",
        "- 辅助信息：融资阶段、目标金额、核心一句话价值主张",
        "",
    ]

    for scene_title, points in scene_points.items():
        lines.append(f"### {scene_title}")
        lines.append("")
        lines.append(f"- 核心信息：{points[0]}")
        for point in points[1:]:
            lines.append(f"- 证据点：{point}")
        lines.append("")

    lines.extend(
        [
            "### S08 结尾CTA",
            "",
            "- 希望投资人下一步动作：安排尽调会议并确认投资流程",
            "- 联系方式/会后动作：补充联系人、数据室链接与会后材料",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LivePPT scene map from BP markdown.")
    parser.add_argument("--input", required=True, help="Path to BP markdown")
    parser.add_argument("--output", required=True, help="Path to scene-map markdown")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    content = input_path.read_text(encoding="utf-8")
    scene_map = build_scene_map(input_path, content)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(scene_map, encoding="utf-8")
    print(f"Scene map written to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
