---
name: wechat-mp
description: 微信公众号全量 API skill (WeChat MP)。纯标准库 CLI 通用网关 raw/call 直达全部 134 个服务端接口(素材、草稿、发布、留言、菜单、用户、客服、群发、数据统计等),内置 doctor 自检与 publish 一键发文链路(封面→草稿→发布→取 URL)。当用户提到微信公众号、公众号接口、公众号素材、草稿、发布、留言、菜单、群发、数据统计时使用。
version: 1.0.0
tags: [wechat, weixin, 公众号, api, publish]
---

# wechat-mp — 微信公众号全量 API CLI

纯 Python 标准库实现,无第三方依赖。单一入口 `scripts/wechat_mp.py`,覆盖 134 个端点(22 分类)。

## 快速开始

> 还没有 AppID/AppSecret? 看申请注册指南: [references/account-setup.md](references/account-setup.md) (注册公众号 → 生成凭证 → IP 白名单 → 权限对照,约 10 分钟)

凭证支持两种方式(env 优先):

```bash
# 方式 0: 引导式配置(推荐首次使用;Secret 输入不回显,文件自动 chmod 600)
python3 scripts/wechat_mp.py init

# 方式 1: 项目根目录 .wechat-mp/.env
mkdir -p .wechat-mp
cat > .wechat-mp/.env <<'CONF'
WECHAT_APP_ID=wx1234567890abcdef
WECHAT_APP_SECRET=your_secret_here
CONF

# 方式 2: 环境变量
export WECHAT_APP_ID=wx1234567890abcdef
export WECHAT_APP_SECRET=your_secret_here
```

首次使用先自检(凭证 / stable_token / quota 三步):

```bash
python3 scripts/wechat_mp.py doctor
```

期望输出:

```
[PASS] credentials
[PASS] stable_token
[PASS] quota
```

FAIL 时按提示行修复(如 40164 → mp.weixin.qq.com 加 IP 白名单)。

## 4 层用法

| 层 | 命令 | 适用场景 | 示例 |
|---|---|---|---|
| L1 通用网关 | `raw` | 直达任意端点,无需注册 | `python3 scripts/wechat_mp.py raw GET /cgi-bin/user/info?openid=oXYZ&lang=zh_CN` |
| L2 注册调用 | `list` + `call` | 按注册名调用,查目录 | `python3 scripts/wechat_mp.py list --search 草稿`<br>`python3 scripts/wechat_mp.py call draft_count` |
| L3 领域子命令 | `draft` / `material` / `comment` | 高频业务操作,免手写 JSON | `python3 scripts/wechat_mp.py draft ls --count 5` |
| L4 一键发文 | `publish` | markdown → 封面→草稿→发布→取 URL | `python3 scripts/wechat_mp.py publish article.md --cover cover.png --yes` |

各子命令完整 flag 见 `--help`;发布全流程见 [examples/publish-article.md](examples/publish-article.md),草稿/素材/留言日常操作见 [examples/manage-drafts.md](examples/manage-drafts.md)。

通用参数:

- `--data '<json>'` 或 `--data @body.json` — 请求 body
- `--file <path>` — multipart 上传文件(素材)
- exit code: `0` 成功 / `1` 服务端 errcode≠0 / `2` 本地错误(参数、blocked、网络)

## 安全规则

- **destructive 端点必须 `--yes`**:注册表标记 `destructive: true` 的端点(删除类、群发、菜单覆盖等),不加 `--yes` 会输出 `blocked` JSON 并退出 2,不做任何网络请求。
- **`raw` 网关不做 destructive 拦截**:`--yes` 闸仅覆盖 `call`/`draft`/`material`/`comment`;`raw` 是逃生通道,直达任意端点。破坏性操作建议优先用 `call`。
- **secret 不落日志**:输出统一脱敏,`WECHAT_APP_SECRET` 永不出现在 stdout/token 缓存中;`.wechat-mp/.env` 勿提交进 git(加 `.gitignore`)。
- 群发 (`mass_sendall`)、`quota_clear_all` 等高影响操作,先在测试号验证。

## 常见 errcode

| errcode | 含义 | 动作 |
|---|---|---|
| -1 | 本地: 缺凭证 | 设置 env 或 `.wechat-mp/.env` |
| -2 | 本地: 网络错误 | 检查网络/代理 |
| 40164 | IP 不在白名单 | 公众号后台加 IP 白名单 |
| 45009 | API 调用次数超限 | `call quota_clear_all --yes` |

完整表见 [references/errors.md](references/errors.md)。

## 端点目录

全部 134 个端点(22 分类,id/name/method/path/destructive)见 [references/api-catalog.md](references/api-catalog.md)。该文件生成自 `scripts/endpoints.json`,改注册表后重新生成。
