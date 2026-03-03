# BPClaw

深度调研驱动的融资 BP 文档 Agent 体系。  
把“写 BP”从一次性文档任务升级为“可复用流程 + 评分闭环 + 多格式产出”。

## 为什么需要 BPClaw

| 能力 | 传统 BP 写作 | BPClaw |
| --- | :---: | :---: |
| 调研证据链 | 片段化 | 系统化（宏观/微观 + 来源日志） |
| 结构完整度 | 依赖个人经验 | 固定流程（6 大章节 + 评分标准） |
| 可执行性 | 叙事多、落地弱 | 强制里程碑、owner、止损条件 |
| 二次复用 | 难以沉淀 | 脚本化模板，可持续迭代 |

## 30 秒快速开始

```bash
# 1) 初始化 BP 工作区
python3 skills/public/bpclaw/scripts/init_bp_project.py "textile-financing-bp" --out .

# 2) 在 outputs/2_bp_draft.md 填入内容后评分
python3 skills/public/bpclaw/scripts/score_bp.py \
  --input textile-financing-bp/outputs/2_bp_draft.md \
  --output textile-financing-bp/outputs/4_bp_review_scorecard.md

# 3) 从 BP 草案自动生成 LivePPT 场景图
python3 skills/public/bpclaw/scripts/generate_liveppt_scene_map.py \
  --input textile-financing-bp/outputs/2_bp_draft.md \
  --output textile-financing-bp/outputs/3_liveppt_scene_map.md

# 4) 可选：导出 DOCX（需要本机安装 pandoc）
python3 skills/public/bpclaw/scripts/export_doc.py \
  --input textile-financing-bp/outputs/2_bp_draft.md \
  --output textile-financing-bp/outputs/2_bp_draft.docx
```

## 核心命令

```bash
python3 skills/public/bpclaw/scripts/init_bp_project.py "<project-name>" --out .
python3 skills/public/bpclaw/scripts/score_bp.py --input <bp.md> --output <scorecard.md>
python3 skills/public/bpclaw/scripts/generate_liveppt_scene_map.py --input <bp.md> --output <scene-map.md>
python3 skills/public/bpclaw/scripts/export_doc.py --input <bp.md> --output <bp.docx>
```

## 工作流

1. 输入背景与融资目标。
2. 宏观/微观深调研并记录证据链。
3. 第一性原理拆解（Musk Drill）。
4. 输出 BP 草案并自动评分。
5. 导出 DOCX 与 LivePPT 场景图。
6. 复盘沉淀为下一轮自动化能力。

## 项目结构

```text
skills/public/bpclaw/
├── README.md
├── SKILL.md
├── agents/openai.yaml
├── scripts/
│   ├── init_bp_project.py
│   ├── score_bp.py
│   ├── export_doc.py
│   └── generate_liveppt_scene_map.py
├── references/
│   ├── evaluation-rubric.md
│   └── research-depth-checklist.md
└── assets/templates/
    ├── background-goal-template.md
    ├── source-log-template.md
    ├── bp-draft-template.md
    └── liveppt-scene-map-template.md
```

## 核心产物

- `inputs/0_background_and_goal.md`
- `research/1_source_log.md`
- `outputs/2_bp_draft.md`
- `outputs/3_liveppt_scene_map.md`
- `outputs/4_bp_review_scorecard.md`
- `outputs/5_reflection.md`

## Roadmap

- [x] v0.1.x：完成 BP 工作流与评分脚本首版。
- [x] v0.2.x：补齐开源发布文档与 CI smoke 校验。
- [ ] v0.3.x：加入行业模板包（制造业/消费品/企业服务）。
- [ ] v0.4.x：加入指标抽取与自动证据完整性检查。

## 贡献

- Bug / 建议：提 [Issue](https://github.com/AIPMAndy/LivePPT/issues)
- 贡献代码：Fork -> Branch -> PR
- 详细规则见 [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[Apache-2.0](LICENSE) + ADDITIONAL TERMS / 附加条款。

## 作者

AI酋长Andy  
商业授权联系：微信 `AIPMAndy`
