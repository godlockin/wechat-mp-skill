# 申请与注册 AppID / AppSecret 指南

> 从零拿到微信公众号 API 凭证的完整流程 (约 10 分钟,免费)。

## 1. 注册公众号 (已有账号跳过)

1. 打开 [mp.weixin.qq.com](https://mp.weixin.qq.com) → 右上角 **立即注册** → 选择 **订阅号**
2. 填写邮箱 (未绑定过任何公众号/小程序) → 激活邮件 → 设置密码 → 选择地区
3. 选择主体类型:
   - **个人**: 身份证姓名 + 号码 + 管理员微信扫码验证。免费、当天可用,但**无法微信认证**,且 2025-07 起官方已回收发布类 API 权限 (`freepublish`、留言管理不可用,见下文权限对照)
   - **企业/个体户**: 需营业执照、对公信息;可后续做微信认证 (300 元/次/年,个体户常有 30 元优惠),认证后全量 API 可用
4. 设置账号名称、功能介绍,完成注册

## 2. 获取 AppID / AppSecret

> 路径: 登录 [mp.weixin.qq.com](https://mp.weixin.qq.com) → 左下角 **设置与开发** → **基本配置** → 「开发者ID」

| 项 | 说明 |
|---|---|
| **AppID (开发者ID)** | 页面直接可见,`wx` 开头 16-18 位 |
| **AppSecret (开发者密码)** | 首次需点击 **生成** 或 **重置** → 管理员微信扫码确认 → **只显示一次,立即保存** (之后只能重置,重置后旧 secret 立即失效) |

注意事项:

- 重置 AppSecret 会使旧 secret 立即失效;多端共用时同步更新
- 长期不用的 secret 可在后台「冻结」,冻结期间无法换取 access_token (`40243`)
- **必须配置 IP 白名单** (同页下方「IP白名单」→ 添加你调用 API 的出口 IP): 不在白名单的机器调 token 类接口会报 `40164`。本机出口 IP 可用 `curl ifconfig.me` 或 `ipconfig getifaddr en0` (局域网) 查看
- 本 skill 只**调用** API,不接收微信回调,**无需填写**「服务器配置 (URL/Token/EncodingAESKey)」,保持未启用即可

## 3. 配置到本 skill

```bash
# 方式 1: 引导式 (推荐,secret 不回显,文件自动 chmod 600)
python3 scripts/wechat_mp.py init

# 方式 2: 手动写文件
mkdir -p .wechat-mp
cat > .wechat-mp/.env <<'CONF'
WECHAT_APP_ID=wx1234567890abcdef
WECHAT_APP_SECRET=your_secret_here
CONF
chmod 600 .wechat-mp/.env

# 方式 3: 环境变量
export WECHAT_APP_ID=wx1234567890abcdef
export WECHAT_APP_SECRET=your_secret_here
```

配置完自检:

```bash
python3 scripts/wechat_mp.py doctor
# [PASS] credentials / stable_token / quota → 全通
```

## 4. 账号权限对照 (哪些接口能用)

| 能力 | 个人订阅号 (未认证) | 认证订阅号/服务号 |
|---|---|---|
| `doctor` / token / quota | ✅ | ✅ |
| 草稿箱 (`draft_*`) | ✅ | ✅ |
| 素材 (`material_*` / `media_*`) | ✅ | ✅ |
| 自定义菜单 / 用户 / 标签 / 客服 / 数据统计 | ✅ | ✅ |
| 发布 (`freepublish/submit`) | ❌ `48001` (2025-07 起个人主体被回收) | ✅ |
| 留言管理 (`comment_*`) | ❌ | 需账号有留言权限 |
| 群发 (`mass_*`) | 个人号每月限额,后台手动更稳妥 | ✅ |

未认证号的推荐工作流: 用本 skill 建草稿 (`publish` 不带 `--yes`) → 在后台「草稿箱」手动点发表。

## 5. 常见错误

| 现象 | 处理 |
|---|---|
| `40164 invalid ip` | 本机出口 IP 未加白名单,见上文第 2 节 |
| `40125 invalid secret` | secret 复制错误/末尾带空格;重置后未同步 |
| `48001 api unauthorized` | 账号无该接口权限 (个人主体发发布类接口),见权限对照 |
| `41002 appid missing` | 该端点读 URL query 不读 body,用 `call` 时 CLI 会自动处理 |
| AppSecret 忘了/丢了 | 后台重置一个新 secret,更新 `.env` 即可 |

完整错误码见 [errors.md](errors.md)。
