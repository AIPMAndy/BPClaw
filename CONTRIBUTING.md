# Contributing

感谢你为 `BPClaw` 贡献代码与文档。

## 1. 贡献范围

- 流程能力：调研、评分、导出、场景图生成。
- 模板能力：`assets/templates/` 下的可复用模板。
- 文档能力：README、SKILL、参考文档、发布材料。

## 2. 基本要求

- 中文优先，必要时补英文。
- 每个 PR 聚焦一个主题，避免混合无关改动。
- 行为变更必须同步更新相关文档。
- 任何自动化改动都要保留人工审批口。

## 3. 本地验证

```bash
# 脚本语法检查
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile skills/public/bpclaw/scripts/*.py

# 初始化工作区 smoke test
python3 skills/public/bpclaw/scripts/init_bp_project.py "contrib-smoke" --out /tmp --force

# 评分 smoke test
python3 skills/public/bpclaw/scripts/score_bp.py \
  --input /tmp/contrib-smoke/outputs/2_bp_draft.md \
  --output /tmp/contrib-smoke/outputs/4_bp_review_scorecard.md

# 场景图 smoke test
python3 skills/public/bpclaw/scripts/generate_liveppt_scene_map.py \
  --input /tmp/contrib-smoke/outputs/2_bp_draft.md \
  --output /tmp/contrib-smoke/outputs/3_liveppt_scene_map.md
```

`export_doc.py` 依赖 `pandoc`，CI 默认不强制。

## 4. Pull Request 规范

- 推荐标题：`feat: ...`、`fix: ...`、`docs: ...`、`refactor: ...`
- 需说明：改动目的、核心变更、验证方式、潜在风险。
- 涉及结构性调整时，需说明回滚方案。

## 5. 安全与合规

- 严禁提交 token、密钥、账号凭据。
- 不接受绕过平台安全机制的自动化。
- 署名与品牌约束见 `LICENSE` 附加条款。
