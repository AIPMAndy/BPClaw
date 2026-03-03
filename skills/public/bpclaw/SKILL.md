---
name: bpclaw
description: 深度调研驱动的融资BP文档助手。用于从“背景+目标+提纲”快速产出可融资BP文档（Markdown），覆盖宏观分析、微观分析、战略规划、战术安排、资源规划、成果愿景，并配套评估打分、MD转DOC、转LivePPT场景图。Use when users ask to 写BP、融资路演材料、行业与公司深度调研、战略/战术拆解，或要求将BP结果沉淀为可复用Agent工作流。
---

# BPClaw

## Overview

把“写BP”从临时写作任务升级为“深度调研 + 第一性原理拆解 + 评分闭环”的可复用流程。
默认先输出 Markdown 融资文档，再转 DOC 与 LivePPT 场景图。

## Input Contract

先收集最小输入，再开工：

- `背景`：公司现状、董事长目标、融资阶段、关键约束。
- `文档目标`：融资金额、估值诉求、里程碑承诺。
- `行业范围`：主赛道、子赛道、地理范围（国内/出海）。
- `提纲偏好`：是否沿用宏观/微观/战略/战术/资源/愿景六段结构。
- `短期出活点`：默认优先 AI 营销数字员工（可替换）。

## Workflow

### Step 1: Initialize Project Workspace

运行初始化脚本，生成输入、调研、输出目录和模板文件。

```bash
python3 scripts/init_bp_project.py "textile-ai-bp" --out .
```

优先填写 `inputs/0_background_and_goal.md`，禁止先写结论再补证据。

### Step 2: Run Deep Research Pass

执行宏观与微观两层调研，先事实后判断：

- 宏观层：行业现状、二级市场、研报、趋势、主要玩家。
- 微观层：销售（toG/toB/toC）、营销（线上/线下）、SKU、生产、内部数字化、组织优劣。

维护 `research/1_source_log.md`，每条关键论断至少对应一个来源。
若用户提供外链（如行业板块页），优先纳入证据链。

### Step 3: Apply Musk First-Principles Drill

在微观分析和战略规划之间，强制插入第一性原理拆解：

1. 定义 Mission：在 12-24 个月把什么指标提升到多少。
2. 拆假设：列出 5-10 条默认假设并删除无法量化项。
3. 建模型：给出单位经济、瓶颈、AI 赋能上限与现实区间。
4. 出选项：保守/平衡/激进三案并写明失败信号。
5. 强执行：给出 30-90 天里程碑和 kill criteria。

### Step 4: Draft and Score BP

基于模板生成 BP 文档后，使用评分脚本做质量评估：

```bash
python3 scripts/score_bp.py --input outputs/2_bp_draft.md --output outputs/4_bp_review_scorecard.md
```

评分低于 `80/100` 时必须重写弱项段落，直到通过。

### Step 5: Export Formats

先转 DOC，再转 LivePPT 场景图：

```bash
python3 scripts/export_doc.py --input outputs/2_bp_draft.md --output outputs/2_bp_draft.docx
python3 scripts/generate_liveppt_scene_map.py --input outputs/2_bp_draft.md --output outputs/3_liveppt_scene_map.md
```

如本机缺少 `pandoc`，先安装后再执行 DOC 导出。

### Step 6: Reflect and Systemize

在 `outputs/5_reflection.md` 记录：

- 本轮最有效方法与失败点。
- 人类反馈导致的关键修改。
- 下次可自动化的决策点与脚本改造项。

## Standard Deliverables

- `inputs/0_background_and_goal.md`
- `research/1_source_log.md`
- `outputs/2_bp_draft.md`
- `outputs/2_bp_draft.docx`（可选）
- `outputs/3_liveppt_scene_map.md`
- `outputs/4_bp_review_scorecard.md`
- `outputs/5_reflection.md`

## Quality Bar

- 证据完整：关键结论均可追溯到来源。
- 逻辑闭环：宏观 -> 微观 -> 战略 -> 战术 -> 资源 -> 愿景前后一致。
- 可执行性：含 owner、节奏、优先级、止损条件。
- 资本可读性：融资叙事清晰，指标可验证，里程碑可审计。

## Resources

### scripts/

- `scripts/init_bp_project.py`：创建 BP 项目骨架与初始模板。
- `scripts/score_bp.py`：按评分维度自动打分并给出改进建议。
- `scripts/export_doc.py`：使用 pandoc 将 MD 导出为 DOCX。
- `scripts/generate_liveppt_scene_map.py`：把 BP 文档转成 LivePPT 场景图草案。

### references/

- `references/evaluation-rubric.md`：BP 评分标准（100 分制）。
- `references/research-depth-checklist.md`：深调研清单与证据要求。

### assets/

- `assets/templates/background-goal-template.md`
- `assets/templates/bp-draft-template.md`
- `assets/templates/source-log-template.md`
- `assets/templates/liveppt-scene-map-template.md`
