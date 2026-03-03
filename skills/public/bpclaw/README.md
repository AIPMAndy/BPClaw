# BPClaw Skill

`BPClaw` 是一个深度调研驱动的融资 BP 产出 skill。

## 入口文件

- `SKILL.md`：工作流与触发规则
- `agents/openai.yaml`：Agent 显示信息
- `scripts/`：初始化、评分、导出、场景图生成脚本
- `references/`：评分标准与调研深度清单
- `assets/templates/`：项目初始化模板

## 本地 smoke test

```bash
python3 scripts/init_bp_project.py "demo-bp" --out /tmp --force
python3 scripts/score_bp.py --input /tmp/demo-bp/outputs/2_bp_draft.md --output /tmp/demo-bp/outputs/4_bp_review_scorecard.md
python3 scripts/generate_liveppt_scene_map.py --input /tmp/demo-bp/outputs/2_bp_draft.md --output /tmp/demo-bp/outputs/3_liveppt_scene_map.md
```
