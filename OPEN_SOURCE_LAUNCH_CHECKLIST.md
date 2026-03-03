# Open Source Launch Checklist

适用于 `BPClaw` 首次公开发布与后续版本迭代。

## 1) Pre-Launch Validation

- [ ] 运行脚本语法检查：`PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile skills/public/bpclaw/scripts/*.py`
- [ ] 运行初始化 smoke test：`init_bp_project.py`
- [ ] 运行评分 smoke test：`score_bp.py`
- [ ] 运行场景图 smoke test：`generate_liveppt_scene_map.py`
- [ ] 如发布 DOC 能力，确认 `pandoc` 可用并完成一次导出。

## 2) Repository Hygiene

- [ ] `README.md`、`SKILL.md`、`CONTRIBUTING.md` 与当前行为一致。
- [ ] `LICENSE`、`ROADMAP.md`、`CHANGELOG.md` 已更新。
- [ ] 无敏感信息（token、密钥、账号凭据）进入版本库。
- [ ] 忽略规则正确，缓存与临时产物不会误提交。

## 3) Release Preparation

- [ ] 更新 `CHANGELOG.md` 的 `Unreleased` 区块。
- [ ] 核对版本号、发布日期、Roadmap 阶段一致。
- [ ] 准备本次发布说明（新增/优化/修复/用户价值）。

## 4) Public Publishing

- [ ] 推送 `main` 并打标签（如 `v0.2.0`）。
- [ ] 发布 GitHub Release（附 changelog 摘要）。
- [ ] 发布后 48 小时内处理首批 issue/PR 反馈。
