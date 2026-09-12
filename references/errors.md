# errcode 速查

CLI 内部错误码(负数,本地产生,不发网络请求)与服务端常见 errcode。完整官方列表见微信官方文档。

## 本地错误码

| errcode | 含义 | 修复动作 |
|---|---|---|
| -1 | 缺凭证(`missing credential`) | 设置 `WECHAT_APP_ID`/`WECHAT_APP_SECRET` 环境变量,或写入 `.wechat-mp/.env` |
| -2 | 网络错误(`network error`) | 检查网络/代理/DNS;API_BASE 固定为 `https://api.weixin.qq.com` |

## 服务端 errcode

| errcode | 含义 | 修复动作 |
|---|---|---|
| 40001 | access_token 无效或不合法 | CLI 自动 refresh token 重试一次;仍失败检查 AppSecret 是否被重置 |
| 40002 | 不合法的凭证类型 | 检查调用方式;stable_token 仅支持 `grant_type=client_credential` |
| 40013 | 不合法的 AppID | 核对 `WECHAT_APP_ID`(注意不要带空格/引号) |
| 40125 | 不合法的 AppSecret(secret 校验失败) | 检查 `.wechat-mp/.env` 中 `WECHAT_APP_SECRET`(注意大小写、末尾换行) |
| 40164 | 调用接口的 IP 不在白名单 | mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单,加入本机出口 IP |
| 40243 | AppSecret 已被冻结 | 公众号后台基本配置 → 重置 AppSecret → 更新 `.env` |
| 41004 | 缺少 secret 参数 | 凭证配置为空;同 -1,补全 env 或 `.env` |
| 45009 | API 调用次数超限(达到日配额) | 清空配额:`python3 scripts/wechat_mp.py call quota_clear_all --yes --data '{"appids":["wxXXXX"]}'`(每天限 1 次 clear_quota;或次日自动恢复) |
| 44002 | post data 为空 | 端点需要 body 但没传;注册表 params 声明 required 后 `call` 会在本地拦截并提示 missing_params |
| 41002 | appid 缺失 | 该端点只读 URL query string、不解析 JSON body(如 `clear_quota/v2`)— 用 `call` 时 CLI 自动把 in=query 参数移到 URL;用 `raw` 时需手动拼 query |
| 48001 | api unauthorized(账号无该接口权限) | 非代码问题:未认证订阅号无 `freepublish` 发布、留言等权限;需微信认证或改用后台手动操作 |
| 50004 | 用户已被拉黑 | 公众号后台 → 用户管理 → 移除黑名单 |
| 50007 | 用户已关注公众号,无需重复操作 | 忽略或检查业务逻辑是否重复触发 |

## 排查辅助

- 带着 errmsg 中的 rid 查详情:`python3 scripts/wechat_mp.py call rid_get --data '{"rid": "<rid>"}'`
- 环境整体自检:`python3 scripts/wechat_mp.py doctor`
- 查当前配额:`python3 scripts/wechat_mp.py call quota_get --data '{"cgi_path": "/cgi-bin/draft/count"}'`
