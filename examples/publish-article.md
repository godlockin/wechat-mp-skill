# 示例: 从 markdown 文件到发布上线

完整会话:doctor 自检 → 封面准备 → 预览(草稿)→ 确认发布 → 拿到 article_url。

## 0. 准备文件

```
my-article/
├── article.md      # 文章正文,可选 frontmatter
└── imgs/
    └── cover.png   # 封面(publish 会自动识别,或用 --cover 指定)
```

`article.md` 支持简单 frontmatter(title/author/digest):

```markdown
---
title: 用 CLI 管理公众号
author: chenchen
digest: 一条命令完成封面上传、草稿创建与发布。
---

正文段落...

![架构图](./imgs/arch.png)
```

正文中相对路径的本地图片会被自动上传(`uploadimg`)并替换为微信 URL。

## 1. 自检环境

```bash
python3 scripts/wechat_mp.py doctor
```

```
[PASS] credentials
[PASS] stable_token
[PASS] quota
```

任一 FAIL 按提示修复后再继续。

## 2. 封面准备

封面必须是永久素材(≥一张图,建议 900x383)。两种来源:

- 约定路径:文章目录下 `imgs/cover.png`,`publish` 自动取用
- 显式指定:`--cover path/to/cover.jpg`

publish 无封面会直接报错退出:

```
cover image required: --cover or imgs/cover.png
```

## 3. 预览:不带 --yes(只建草稿)

```bash
python3 scripts/wechat_mp.py publish my-article/article.md
```

```json
{
  "draft_media_id": "R8ItYY1IqgGeD4Syt4TT7YIM_IpRKBv3tbaeyGPRlKrNnbW8A",
  "hint": "draft created; run again with --yes to publish"
}
```

此时文章只是草稿,可先到公众号后台预览排版,或用 `draft get --media-id <id>` 查看内容。确认无误前**不会**推送给任何用户。

## 4. 确认发布:加 --yes

```bash
python3 scripts/wechat_mp.py publish my-article/article.md --yes
```

发布链路:上传封面(add_material)→ draft/add → freepublish/submit → 每 3 秒轮询 freepublish/get(最多 20 次)。

成功输出:

```json
{
  "publish_id": "100000001",
  "state": "success",
  "article_urls": [
    "https://mp.weixin.qq.com/s/AbCdEfGh1234567890"
  ],
  "draft_media_id": "R8ItYY1IqgGeD4Syt4TT7YIM_IpRKBv3tbaeyGPRlKrNnbW8A"
}
```

`article_urls[0]` 即线上文章链接。

## 5. 常见后续

- 轮询超时(发布仍在进行):稍后手动查状态

```bash
python3 scripts/wechat_mp.py raw POST /cgi-bin/freepublish/get --data '{"publish_id": "100000001"}'
```

- 多篇合并发布(JSON 输入,封面统一覆盖为 --cover 指定图):

```bash
python3 scripts/wechat_mp.py publish multi.json --cover cover.png --yes
```

`multi.json` 格式: `{"articles": [{"title": "...", "content": "<p>...</p>", "thumb_media_id": "可省略"}]}`

- 发布失败(state 2/3):输出含 `fail_idx` 与 `raw`,按其中 errcode 查 [references/errors.md](../references/errors.md)
