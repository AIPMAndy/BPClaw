#!/usr/bin/env python3
"""Score a BP markdown draft using BPClaw rubric heuristics."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


DIMENSIONS = [
    ("目标与融资命题清晰度", 10),
    ("宏观分析深度", 20),
    ("微观分析深度", 20),
    ("战略规划一致性", 15),
    ("战术可执行性", 15),
    ("资源规划可落地性", 10),
    ("愿景与资本叙事", 10),
]


def extract_section(text: str, start_tokens: list[str], end_tokens: list[str]) -> str:
    start_idx = min((text.find(token) for token in start_tokens if token in text), default=-1)
    if start_idx == -1:
        return ""
    end_candidates = [text.find(token, start_idx + 1) for token in end_tokens]
    end_candidates = [idx for idx in end_candidates if idx != -1]
    end_idx = min(end_candidates) if end_candidates else len(text)
    return text[start_idx:end_idx]


def ratio_hits(text: str, keywords: list[str]) -> float:
    if not keywords:
        return 0.0
    lowered = text.lower()
    hits = sum(1 for kw in keywords if kw.lower() in lowered)
    return hits / len(keywords)


def numeric_density(text: str) -> float:
    num_count = len(re.findall(r"\d+(?:\.\d+)?(?:%|亿|万|元|人)?", text))
    return min(num_count / 12.0, 1.0)


def url_density(text: str) -> float:
    links = re.findall(r"https?://[^\s)]+", text)
    return min(len(links) / 6.0, 1.0)


def score_dimension(weight: int, coverage: float, url_bonus: float = 0.0, num_bonus: float = 0.0) -> int:
    # Coverage dominates; evidence density contributes to robustness.
    total = 0.7 * coverage + 0.15 * url_bonus + 0.15 * num_bonus
    return round(weight * min(max(total, 0.0), 1.0))


def evaluate(md: str) -> tuple[list[tuple[str, int, int]], int]:
    background_cov = ratio_hits(md, ["背景", "文档目标", "融资", "估值", "目标"])
    macro = extract_section(md, ["一、宏观分析"], ["二、微观分析"])
    micro = extract_section(md, ["二、微观分析"], ["三、战略规划"])
    strategy = extract_section(md, ["三、战略规划"], ["四、战术安排"])
    tactical = extract_section(md, ["四、战术安排"], ["五、资源规划"])
    resource = extract_section(md, ["五、资源规划"], ["六、成果愿景"])
    vision = extract_section(md, ["六、成果愿景"], ["附录", "## 附录", "# 附录"])

    macro_cov = ratio_hits(
        macro, ["行业现状", "二级市场", "研报", "行业趋势", "全球化", "AI化", "行业玩家", "公司分析"]
    )
    micro_cov = ratio_hits(
        micro,
        [
            "toG",
            "toB",
            "toC",
            "线上",
            "线下",
            "SKU",
            "生产",
            "数字化",
            "信息化",
            "组织",
            "优点",
            "缺点",
        ],
    )
    strategy_cov = ratio_hits(strategy, ["战略方向", "方向规划", "拥抱AI", "数字员工"])
    tactical_cov = ratio_hits(
        tactical, ["战术拆解", "优先级", "短期重点", "里程碑", "数字员工", "运营", "设计"]
    )
    resource_cov = ratio_hits(resource, ["HC", "权限", "节奏"])
    vision_cov = ratio_hits(vision, ["短期成果", "长期成果", "未来愿景", "亿", "市值"])

    rows: list[tuple[str, int, int]] = []
    rows.append((DIMENSIONS[0][0], score_dimension(10, background_cov, url_density(md), numeric_density(md)), 10))
    rows.append(
        (
            DIMENSIONS[1][0],
            score_dimension(20, macro_cov, url_density(macro), numeric_density(macro)),
            20,
        )
    )
    rows.append(
        (
            DIMENSIONS[2][0],
            score_dimension(20, micro_cov, url_density(micro), numeric_density(micro)),
            20,
        )
    )
    rows.append(
        (
            DIMENSIONS[3][0],
            score_dimension(15, strategy_cov, url_density(strategy), numeric_density(strategy)),
            15,
        )
    )
    rows.append(
        (
            DIMENSIONS[4][0],
            score_dimension(15, tactical_cov, url_density(tactical), numeric_density(tactical)),
            15,
        )
    )
    rows.append((DIMENSIONS[5][0], score_dimension(10, resource_cov, 0.0, numeric_density(resource)), 10))
    rows.append((DIMENSIONS[6][0], score_dimension(10, vision_cov, 0.0, numeric_density(vision)), 10))
    total = sum(r[1] for r in rows)
    return rows, total


def band(total: int) -> str:
    if total >= 90:
        return "可直接进入融资沟通版本"
    if total >= 80:
        return "可用于内部评审或小范围预沟通"
    if total >= 70:
        return "结构完整但说服力不足"
    return "不建议对外，需重做关键章节"


def weak_points(rows: list[tuple[str, int, int]]) -> list[str]:
    return [name for name, score, weight in rows if score < int(weight * 0.7)]


def build_report(rows: list[tuple[str, int, int]], total: int, source: Path) -> str:
    weak = weak_points(rows)
    weak_line = "、".join(weak) if weak else "无明显短板"
    actions = (
        "- 补充关键结论的数据来源与链接\n"
        "- 为短期抓手补齐 30-90 天里程碑、owner 和验收指标\n"
        "- 把“AI方向”细化为岗位、流程、工具、指标"
    )
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# BP评分卡",
        "",
        f"- 评估时间：{now}",
        f"- 输入文件：{source}",
        "",
        "| 维度 | 得分 | 满分 |",
        "| --- | --- | --- |",
    ]
    for name, score, weight in rows:
        lines.append(f"| {name} | {score} | {weight} |")

    lines.extend(
        [
            "",
            f"- 总分：**{total}/100**",
            f"- 结论：**{band(total)}**",
            f"- 最薄弱章节：{weak_line}",
            "",
            "## 下一轮改进动作",
            "",
            actions,
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Score BP markdown draft.")
    parser.add_argument("--input", required=True, help="Path to BP markdown")
    parser.add_argument("--output", required=True, help="Path to scorecard markdown")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    rows, total = evaluate(text)
    report = build_report(rows, total, input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Score written to: {output_path}")
    print(f"Total score: {total}/100 ({band(total)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
