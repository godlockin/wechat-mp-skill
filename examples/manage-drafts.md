# 示例: 草稿 / 素材 / 留言日常管理

前置:`python3 scripts/wechat_mp.py doctor` 三项 PASS。

## 草稿箱 (draft)

### 列出草稿

```bash
python3 scripts/wechat_mp.py draft ls --offset 0 --count 5
```

```json
{
  "total_count": 12,
  "item_count": 5,
  "item": [
    {
      "media_id": "R8ItYY1IqgGeD4Syt4TT7YIM_IpRKBv3tbaeyGPRlKrNnbW8A",
      "update_time": 1726100000,
      "content": {
        "news_item": [
          { "title": "用 CLI 管理公众号", "url": "", "digest": "..." }
        ]
      }
    }
  ]
}
```

`ls` 默认 `no_content: 1`,不返回正文,省流量。

### 查看单篇草稿(含正文)

```bash
python3 scripts/wechat_mp.py draft get --media-id R8ItYY1IqgGeD4Syt4TT7YIM_IpRKBv3tbaeyGPRlKrNnbW8A
```

```json
{
  "news_item": [
    { "title": "用 CLI 管理公众号", "content": "<p>正文 HTML...</p>", "thumb_media_id": "..." }
  ]
}
```

### 草稿总数

```bash
python3 scripts/wechat_mp.py draft count
```

```json
{ "total_count": 12 }
```

### 删除草稿(destructive,需 --yes)

```bash
python3 scripts/wechat_mp.py draft del --media-id R8ItYY1IqgGeD4Syt4TT7YIM_IpRKBv3tbaeyGPRlKrNnbW8A
```

漏 `--yes` 时被安全闸拦截,返回码 2,不发请求:

```json
{
  "blocked": true,
  "endpoint": "draft_delete",
  "name": "删除草稿",
  "hint": "add --yes to confirm"
}
```

加 `--yes` 后:

```json
{ "errcode": 0, "errmsg": "ok" }
```

## 永久素材 (material)

### 上传图片素材

```bash
python3 scripts/wechat_mp.py material upload --file imgs/cover.png --type image --name 封面图
```

```json
{ "media_id": "COvNcBK1s3Y1IqgGeD4Syt4TT7YIM_IpRKBv3tbaeyGPRlKrNnbW8", "url": "" }
```

`--type` 支持 image / video / voice / news(video 需配合 description)。

### 列出素材

```bash
python3 scripts/wechat_mp.py material ls --type image --count 10
```

```json
{
  "total_count": 34,
  "item_count": 10,
  "item": [
    { "media_id": "COvNcBK1s3Y1IqgGeD4Syt4TT7YIM_IpRKBv3tbaeyGPRlKrNnbW8",
      "name": "封面图", "update_time": 1726100000 }
  ]
}
```

### 删除素材(destructive,需 --yes)

```bash
python3 scripts/wechat_mp.py material del --media-id COvNcBK1s3Y1IqgGeD4Syt4TT7YIM_IpRKBv3tbaeyGPRlKrNnbW8 --yes
```

```json
{ "errcode": 0, "errmsg": "ok" }
```

## 留言管理 (comment)

官方契约:留言接口一律用 `msg_data_id`(整数,群发返回的 `msg_data_id`,`--article-id` 即它)+ `--index`(多图文时第几篇,从 0 开始);精选/取消精选/删除/回复另需 `user_comment_id`(`--comment-id`,整数,从 `comment ls` 结果的 `comment_id` 获取)。`comment ls` 单页 `--count` 最大 50(>=50 会被拒绝)。

### 列出留言

```bash
python3 scripts/wechat_mp.py comment ls --article-id 1000000001 --count 20
```

```json
{
  "total": 3,
  "comment": [
    { "user_openid": "oXYZ123", "content": "写得不错!", "comment_id": 5001, "is_elected": 0 }
  ]
}
```

`--type 0` 全部留言 / `--type 1` 普通 / `--type 2` 仅精选。

### 回复留言

```bash
python3 scripts/wechat_mp.py comment reply --article-id 1000000001 --comment-id 5001 --content "感谢支持!"
```

```json
{ "errcode": 0, "errmsg": "ok" }
```

### 精选留言(destructive,需 --yes)

```bash
python3 scripts/wechat_mp.py comment elect --article-id 1000000001 --comment-id 5001 --yes
```

```json
{ "errcode": 0, "errmsg": "ok" }
```

取消精选:

```bash
python3 scripts/wechat_mp.py comment unelect --article-id 1000000001 --comment-id 5001 --yes
```

删除留言(destructive,需 --yes):

```bash
python3 scripts/wechat_mp.py comment delete --article-id 1000000001 --comment-id 5001 --yes
```

### 开关留言功能

```bash
python3 scripts/wechat_mp.py comment open --article-id 1000000001
python3 scripts/wechat_mp.py comment close --article-id 1000000001
```

注:open/close 非 destructive,无需 `--yes`;elect/unelect/delete 为 destructive,需 `--yes`。

## 通用:不确定参数时先查目录

```bash
python3 scripts/wechat_mp.py list --search 留言
python3 scripts/wechat_mp.py call comment_list --data '{"msg_data_id": 1000000001, "begin": 0, "count": 20}'
```

全量端点见 [references/api-catalog.md](../references/api-catalog.md),errcode 见 [references/errors.md](../references/errors.md)。
