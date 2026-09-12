# wechat-mp-skill

**Full-coverage WeChat Official Account (微信公众号) API CLI & Agent Skill** — 134 endpoints, zero-dependency Python, built for AI agents.

[中文](#中文) | [English](#english)

## 中文

一个把微信公众号服务端 API 全量封装成「Claude/任意 Agent 可直接使用」的 skill,同时也是一个独立的零依赖 CLI 工具。

### 特性

- **全量覆盖**: 134 个端点 / 22 个模块 (素材、草稿、发布、留言、菜单、用户、客服、群发、数据统计、OCR、门店等),来自 `endpoints.json` 端点注册表 — 新增端点只需加一条 JSON,零代码
- **通用网关**: `raw`/`call` 任意端点一条命令直达,自动附带 access_token、失效自动续期重试
- **破坏性防护**: 删除/发布类端点强制 `--yes` 确认,缺省拒绝并说明将执行的操作
- **便利命令**: `doctor` 环境自检、`publish` 一键发文链路 (封面→草稿→发布→轮询)、`draft`/`material`/`comment` 高频流程
- **零依赖**: 纯 Python 3 标准库,clone 即用

### 快速开始

```bash
# 配置凭证 (二选一)
export WECHAT_APP_ID=wx... export WECHAT_APP_SECRET=...
# 或写入 .wechat-mp/.env

# 环境自检 (凭证 / token / 配额)
python3 scripts/wechat_mp.py doctor

# 建一篇草稿 (封面 + 正文本地图自动上传)
python3 scripts/wechat_mp.py publish article.md --cover cover.png

# 确认后发布 (需账号有发布权限)
python3 scripts/wechat_mp.py publish article.md --cover cover.png --yes

# 任意端点直达
python3 scripts/wechat_mp.py call draft_count
python3 scripts/wechat_mp.py raw GET /cgi-bin/draft/count
```

### 作为 Claude Skill 安装

拷贝本目录到 `~/.claude/skills/wechat-mp/` (或通过 [ultraskills](https://github.com/godlockin/ultraskills) 安装),SKILL.md 会自动路由「微信公众号」相关请求。

### 权限说明

- 未认证订阅号: 素材/草稿/用户/数据统计等 API 可用;`freepublish` 发布与留言 API 需认证主体 (2025-07 起个人主体账号已被回收发布类 API 权限)
- 完整接口清单见 [`references/api-catalog.md`](references/api-catalog.md),错误码速查见 [`references/errors.md`](references/errors.md)

## English

A WeChat Official Account (公众号) skill that wraps **all 134 server-side API endpoints** into a zero-dependency Python CLI, designed to be invoked directly by AI agents (Claude Code, etc.).

- **Endpoint registry** (`endpoints.json`): every endpoint's name/method/path/destructive flag — extend it with a JSON entry, not code
- **Safety gate**: destructive endpoints (delete/publish/mass-send) require an explicit `--yes`
- **Convenience layer**: `doctor` self-check, `publish` pipeline (cover → draft → submit → poll), `draft`/`material`/`comment`
- **Auth**: `stable_token` with local cache, single auto-retry on `40001/42001`

See the Chinese section above for full usage; CLI help: `python3 scripts/wechat_mp.py --help`.

## License

MIT © 2026 Steven Chen
