#!/usr/bin/env python3
"""wechat-mp: 微信公众号全量 API CLI (纯标准库)."""
import os
import uuid

CONFIG_DIR = ".wechat-mp"


def load_config():
    """返回 (app_id, secret)。env 优先,回退 .wechat-mp/.env。"""
    app_id = os.environ.get("WECHAT_APP_ID")
    secret = os.environ.get("WECHAT_APP_SECRET")
    env_path = os.path.join(CONFIG_DIR, ".env")
    if app_id is None or secret is None:
        if os.path.isfile(env_path):
            data = {}
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        data[k.strip()] = v.strip()
            app_id = app_id or data.get("WECHAT_APP_ID")
            secret = secret or data.get("WECHAT_APP_SECRET")
    return app_id, secret


import json, time

TOKEN_FILE = os.path.join(CONFIG_DIR, "token.json")


def write_token_cache(token, expires_in, now=None):
    if now is None:
        now = time.time()
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump({"token": token, "expires_at": now + expires_in - 300}, f)


def read_token_cache(now=None):
    if now is None:
        now = time.time()
    try:
        with open(TOKEN_FILE, encoding="utf-8") as f:
            cached = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(cached, dict):
        return None
    token, expires_at = cached.get("token"), cached.get("expires_at")
    if not token or not isinstance(expires_at, (int, float)) or now >= expires_at or expires_at - now > 7200:
        return None  # 过期或异常(倒退超过一个周期)
    return token


import urllib.request, urllib.error, urllib.parse

API_BASE = "https://api.weixin.qq.com"


class WechatApiError(Exception):
    """服务端返回 errcode != 0。payload 为原始 JSON dict。"""
    def __init__(self, payload):
        self.payload = payload
        super().__init__(payload.get("errmsg", "unknown"))


class WechatNetworkError(Exception):
    pass


def http_json(method, path, query=None, body=None):
    """底层 HTTP: 返回解析后的 dict。errcode!=0 抛 WechatApiError,网络问题抛 WechatNetworkError。"""
    url = API_BASE + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))  # 微信 5xx 也回 JSON
        except ValueError:
            raise WechatNetworkError(f"HTTP {e.code}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise WechatNetworkError(str(e)) from e


def fetch_stable_token(app_id, secret, force_refresh=False):
    body = {"grant_type": "client_credential", "appid": app_id, "secret": secret,
            "force_refresh": force_refresh}
    payload = http_json("POST", "/cgi-bin/stable_token", body=body)
    if payload.get("errcode", 0) != 0:
        raise WechatApiError(payload)
    return payload["access_token"], payload["expires_in"]


def get_access_token(force_refresh=False):
    if not force_refresh:
        cached = read_token_cache()
        if cached:
            return cached
    app_id, secret = load_config()
    if not app_id or not secret:
        missing = "WECHAT_APP_ID" if not app_id else "WECHAT_APP_SECRET"
        print(json.dumps({"errcode": -1, "errmsg": f"missing credential: {missing} "
                          f"(set env or .wechat-mp/.env)"}, indent=2, ensure_ascii=False))
        raise SystemExit(2)
    token, expires_in = fetch_stable_token(app_id, secret, force_refresh)
    write_token_cache(token, expires_in)
    return token


def build_multipart(fields, file_field, filename, content, file_mime="application/octet-stream"):
    boundary = "----wechatmp" + uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'
        f'Content-Type: {file_mime}\r\n\r\n'.encode() + content + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def _upload_multipart(url, fields, file_field, filename, content):
    body, ctype = build_multipart(fields, file_field, filename, content)
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except ValueError:
            raise WechatNetworkError(f"HTTP {e.code}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise WechatNetworkError(str(e)) from e


RETRYABLE_CODES = {40001, 42001}


def api_call(method, path, body=None, file=None, file_field="media",
             extra_query=None, token=None):
    """网关: 附 token 调任意端点。file=(filename, bytes)。返回服务端 dict。"""
    for attempt in (0, 1):  # 最多两次
        if token is None:
            token = get_access_token(force_refresh=attempt == 1)
        query = dict(extra_query or {})
        query["access_token"] = token
        url = API_BASE + path + "?" + urllib.parse.urlencode(query)
        try:
            if file is not None:
                payload = _upload_multipart(url, body or {}, file_field, file[0], file[1])
            else:
                payload = http_json(method, path, query=query, body=body)
        except WechatNetworkError:
            raise
        if payload.get("errcode", 0) in RETRYABLE_CODES and attempt == 0:
            token = None
            continue
        return payload


import argparse, sys


def _emit(payload):
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _load_data_arg(val):
    if val is None:
        return None
    if val.startswith("@"):
        with open(val[1:], encoding="utf-8") as f:
            return json.load(f)
    return json.loads(val)


def _split_path(path):
    if "?" in path:
        p, q = path.split("?", 1)
        extra = dict(urllib.parse.parse_qsl(q))
        return p, extra
    return path, {}


def cmd_raw(args):
    path, extra = _split_path(args.path)
    try:
        payload = api_call(args.method, path,
                           body=_load_data_arg(args.data),
                           file=_read_file(args.file) if args.file else None,
                           extra_query=extra)
    except WechatNetworkError as e:
        _emit({"errcode": -2, "errmsg": f"network error: {e}", "rid": None})
        return 2
    _emit(payload)
    return 0 if payload.get("errcode", 0) == 0 else 1


def _read_file(path):
    with open(path, "rb") as f:
        return (os.path.basename(path), f.read())


ENDPOINTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "endpoints.json")


def load_endpoints():
    with open(ENDPOINTS_PATH, encoding="utf-8") as f:
        return json.load(f)


def validate_endpoints(registry):
    errs = []
    seen_paths = {}
    for eid, e in registry.items():
        if e.get("method") not in ("GET", "POST"):
            errs.append(f"{eid}: method must be GET/POST")
        if not str(e.get("path", "")).startswith("/"):
            errs.append(f"{eid}: path must start with /")
        for field in ("name", "category", "params", "destructive"):
            if field not in e:
                errs.append(f"{eid}: missing field {field}")
        if e.get("auth", "token") not in ("token", "none"):
            errs.append(f"{eid}: auth must be token/none")
        key = (e.get("method"), e.get("path"))
        if key in seen_paths:
            errs.append(f"{eid}: duplicate method+path with {seen_paths[key]}")
        seen_paths[key] = eid
    return errs


def cmd_list(args):
    registry = load_endpoints()
    errs = validate_endpoints(registry)
    if errs:
        print(json.dumps(errs, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    rows = [{"id": k, **v} for k, v in registry.items()
             if (not args.category or v["category"] == args.category)
             and (not args.search or args.search in v["name"] or args.search in k)]
    _emit(rows)
    return 0


def cmd_call(args):
    registry = load_endpoints()
    ep = registry.get(args.endpoint)
    if ep is None:
        print(f"unknown endpoint: {args.endpoint} (run 'list' to see all)", file=sys.stderr)
        return 2
    if ep.get("destructive") and not args.yes:
        print(json.dumps({"blocked": True, "endpoint": args.endpoint,
                          "name": ep["name"], "path": ep["path"],
                          "hint": "destructive operation, add --yes to confirm"},
                         ensure_ascii=False, indent=2))
        return 2
    try:
        payload = api_call(ep["method"], ep["path"], body=_load_data_arg(args.data),
                           file=_read_file(args.file) if args.file else None)
    except WechatNetworkError as e:
        _emit({"errcode": -2, "errmsg": f"network error: {e}", "rid": None})
        return 2
    _emit(payload)
    return 0 if payload.get("errcode", 0) == 0 else 1


DOCTOR_HINTS = {
    40164: "IP 不在白名单: mp.weixin.qq.com → 设置与开发 → 基本配置 → IP白名单, 加入本机出口 IP",
    40125: "secret 无效: 检查 .wechat-mp/.env 中 WECHAT_APP_SECRET (注意大小写)",
    40013: "appid 无效: 检查 WECHAT_APP_ID",
    40243: "AppSecret 已冻结: mp.weixin.qq.com → 基本配置 → 重置后更新 .env",
    48001: "api 无权限: 账号未微信认证或无该接口权限 (如未认证订阅号无 freepublish 发布/留言权限)",
}


def _report_doctor(steps):
    all_ok = True
    for name, ok, hint in steps:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            all_ok = False
        line = f"[{mark}] {name}" + (f" — {hint}" if hint and not ok else "")
        print(line)
    return 0 if all_ok else 1


def cmd_doctor(args):
    steps = []
    app_id, secret = load_config()
    steps.append(("credentials", app_id and secret,
                  "set WECHAT_APP_ID/WECHAT_APP_SECRET or .wechat-mp/.env"))
    if not (app_id and secret):
        return _report_doctor(steps)
    try:
        token, _ = fetch_stable_token(app_id, secret)
        steps.append(("stable_token", True, ""))
        write_token_cache(token, 7200)
        quota = http_json("POST", "/cgi-bin/openapi/quota/get",
                          query={"access_token": token},
                          body={"cgi_path": "/cgi-bin/draft/count"})
        ok = quota.get("errcode", 0) == 0
        hint = DOCTOR_HINTS.get(quota.get("errcode"), quota.get("errmsg", ""))
        steps.append(("quota", ok, hint))
    except WechatApiError as e:
        code = e.payload.get("errcode", -1)
        steps.append(("stable_token", False, DOCTOR_HINTS.get(code, e.payload.get("errmsg", ""))))
    except WechatNetworkError as e:
        steps.append(("network", False, str(e)))
    return _report_doctor(steps)


def _guarded_call(endpoint_id, body=None, file=None, yes=False, extra_query=None):
    """按注册名调用; destructive 且缺 --yes 时打印 blocked JSON 并返回 (2, {})。"""
    ep = load_endpoints().get(endpoint_id)
    if ep.get("destructive") and not yes:
        print(json.dumps({"blocked": True, "endpoint": endpoint_id, "name": ep["name"],
                          "hint": "add --yes to confirm"}, ensure_ascii=False, indent=2))
        return 2, {}
    try:
        payload = api_call(ep["method"], ep["path"], body=body, file=file,
                           extra_query=extra_query)
    except WechatNetworkError as e:
        _emit({"errcode": -2, "errmsg": f"network error: {e}", "rid": None})
        return 2, {}
    _emit(payload)
    return (0 if payload.get("errcode", 0) == 0 else 1), payload


def cmd_draft(args):
    if args.action == "ls":
        return _guarded_call("draft_batchget", {"offset": args.offset, "count": args.count,
                                                "no_content": 1})[0]
    if args.action == "get":
        return _guarded_call("draft_get", {"media_id": args.media_id})[0]
    if args.action == "count":
        return _guarded_call("draft_count")[0]
    if args.action == "del":
        return _guarded_call("draft_delete", {"media_id": args.media_id}, yes=args.yes)[0]


def cmd_material(args):
    if args.action == "ls":
        if args.type not in ("image", "video", "voice", "news"):
            print("type must be image|video|voice|news", file=sys.stderr)
            return 2
        return _guarded_call("material_batchget",
                             {"type": args.type, "offset": args.offset,
                              "count": args.count, "no_content": 1})[0]
    if args.action == "upload":
        # material_add 非 destructive; yes=True 仅跳过 guard,无副作用
        return _guarded_call("material_add", {"description": args.name or ""},
                             file=_read_file(args.file), yes=True,
                             extra_query={"type": args.type})[0]
    if args.action == "del":
        return _guarded_call("material_del", {"media_id": args.media_id}, yes=args.yes)[0]


def cmd_comment(args):
    # 官方契约: 一律 msg_data_id(int) + index; 精选/取消/删除/回复另需 user_comment_id
    # (developers.weixin.qq.com 留言管理; comment/list count >=50 会被拒绝)
    if args.action in ("reply", "elect", "unelect", "delete") and args.comment_id is None:
        print(f"comment {args.action} requires --comment-id (user_comment_id)", file=sys.stderr)
        return 2
    article = int(args.article_id)
    m = {
        "ls": ("comment_list", {"msg_data_id": article, "index": args.index,
                                "begin": args.begin, "count": args.count,
                                "type": args.type}),
        "reply": ("comment_reply_add", {"msg_data_id": article, "index": args.index,
                                        "user_comment_id": args.comment_id,
                                        "content": args.content}),
        "elect": ("comment_markelect", {"msg_data_id": article, "index": args.index,
                                        "user_comment_id": args.comment_id}),
        "unelect": ("comment_unmarkelect", {"msg_data_id": article, "index": args.index,
                                            "user_comment_id": args.comment_id}),
        "delete": ("comment_delete", {"msg_data_id": article, "index": args.index,
                                      "user_comment_id": args.comment_id}),
        "open": ("comment_open", {"msg_data_id": article, "index": args.index}),
        "close": ("comment_close", {"msg_data_id": article, "index": args.index}),
    }
    endpoint_id, body = m[args.action]
    return _guarded_call(endpoint_id, body, yes=args.yes)[0]


def parse_markdown(md_text):
    """解析简单 frontmatter (--- 块)。返回 (meta dict, body)。"""
    meta = {}
    body = md_text
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = parts[2].lstrip("\n")
    return meta, body


def replace_local_images(body, basedir):
    """正文本地图片 ![](./x.png) → uploadimg 换微信 URL。返回 (新 body, 上传记录)。"""
    import re
    uploaded = []

    def repl(m):
        alt, path = m.group(1), m.group(2)
        if not re.match(r"^(https?://|/)", path):
            local = os.path.join(basedir, path)
            if os.path.isfile(local):
                up = api_call("POST", "/cgi-bin/media/uploadimg", file=_read_file(local))
                if up.get("errcode", 0) == 0:
                    uploaded.append({"local": path, "url": up["url"]})
                    return f"![{alt}]({up['url']})"
        return m.group(0)

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, body), uploaded


def _upload_cover(cover_path):
    payload = api_call("POST", "/cgi-bin/material/add_material",
                       extra_query={"type": "image"}, file=_read_file(cover_path))
    if payload.get("errcode", 0) != 0:
        _emit(payload)
        raise SystemExit(1)
    return payload["media_id"]


def cmd_publish(args):
    with open(args.file, encoding="utf-8") as f:
        raw = f.read()
    if args.file.endswith(".json"):
        payload = json.loads(raw)
        articles = payload.get("articles")
        if not articles:
            print("json must contain 'articles' array", file=sys.stderr)
            return 2
    else:
        meta, body = parse_markdown(raw)
        basedir = os.path.dirname(os.path.abspath(args.file))
        body, _imgs = replace_local_images(body, basedir)
        articles = [{
            "title": args.title or meta.get("title", ""),
            "content": body,
            "need_open_comment": 1, "only_fans_can_comment": 0}]
        if args.author or meta.get("author"):
            articles[0]["author"] = args.author or meta.get("author")
        if args.digest or meta.get("digest"):
            articles[0]["digest"] = args.digest or meta.get("digest")

    cover = args.cover
    if not cover:
        cand = os.path.join(os.path.dirname(os.path.abspath(args.file)), "imgs", "cover.png")
        if os.path.isfile(cand):
            cover = cand
    if not cover:
        print("cover image required: --cover or imgs/cover.png", file=sys.stderr)
        return 2
    thumb_media_id = _upload_cover(cover)
    # 封面统一覆盖: 每篇文章的 thumb_media_id 无条件替换为已上传封面
    for a in articles:
        a["thumb_media_id"] = thumb_media_id

    resp = api_call("POST", "/cgi-bin/draft/add", body={"articles": articles})
    if resp.get("errcode", 0) != 0:
        _emit(resp)
        return 1
    media_id = resp["media_id"]
    if not args.yes:
        print(json.dumps({"draft_media_id": media_id,
                          "hint": "draft created; run again with --yes to publish"},
                         ensure_ascii=False, indent=2))
        return 0

    sub = api_call("POST", "/cgi-bin/freepublish/submit", body={"media_id": media_id})
    if sub.get("errcode", 0) != 0:
        _emit(sub)
        return 1
    publish_id = sub["publish_id"]
    for _ in range(20):
        time.sleep(3)
        st = api_call("POST", "/cgi-bin/freepublish/get", body={"publish_id": publish_id})
        if st.get("errcode", 0) != 0:
            _emit(st)
            return 1
        state = st.get("publish_state")
        if state == 0:
            urls = [i["article_url"] for i in
                    st.get("article_detail", {}).get("item", []) if i.get("article_url")]
            _emit({"publish_id": publish_id, "state": "success", "article_urls": urls,
                   "draft_media_id": media_id})
            return 0
        if state in (2, 3):  # 原创失败/常规失败
            _emit({"publish_id": publish_id, "state": state, "fail_idx":
                   st.get("fail_idx", []), "raw": st})
            return 1
    _emit({"publish_id": publish_id, "state": "timeout",
           "hint": "still publishing; check later via 'raw POST /cgi-bin/freepublish/get'"})
    return 1


def build_parser():
    p = argparse.ArgumentParser(prog="wechat_mp.py", description="微信公众号全量 API CLI")
    sub = p.add_subparsers(dest="command", required=True)
    raw = sub.add_parser("raw", help="通用网关: 任意端点直达")
    raw.add_argument("method", choices=["GET", "POST"])
    raw.add_argument("path", help="API 路径,可带 ?query")
    raw.add_argument("--data", help="JSON body,@file 读文件")
    raw.add_argument("--file", help="上传文件路径(multipart)")
    raw.set_defaults(func=cmd_raw)
    ls = sub.add_parser("list", help="列出端点")
    ls.add_argument("--category")
    ls.add_argument("--search")
    ls.set_defaults(func=cmd_list)
    call = sub.add_parser("call", help="按注册名调用端点")
    call.add_argument("endpoint")
    call.add_argument("--data")
    call.add_argument("--file")
    call.add_argument("--yes", action="store_true", help="确认 destructive 操作")
    call.set_defaults(func=cmd_call)
    doc = sub.add_parser("doctor", help="环境自检: 凭证/token/quota")
    doc.set_defaults(func=cmd_doctor)
    dr = sub.add_parser("draft", help="草稿箱管理")
    dr.add_argument("action", choices=["ls", "get", "count", "del"])
    dr.add_argument("--media-id")
    dr.add_argument("--offset", type=int, default=0)
    dr.add_argument("--count", type=int, default=20)
    dr.add_argument("--yes", action="store_true")
    dr.set_defaults(func=cmd_draft)
    mt = sub.add_parser("material", help="永久素材管理")
    mt.add_argument("action", choices=["ls", "upload", "del"])
    mt.add_argument("--file")
    mt.add_argument("--type", default="image")
    mt.add_argument("--media-id")
    mt.add_argument("--name")
    mt.add_argument("--offset", type=int, default=0)
    mt.add_argument("--count", type=int, default=20)
    mt.add_argument("--yes", action="store_true")
    mt.set_defaults(func=cmd_material)
    cm = sub.add_parser("comment", help="留言管理")
    cm.add_argument("action", choices=["ls", "reply", "elect", "unelect", "delete",
                                       "open", "close"])
    cm.add_argument("--article-id", required=True,
                    help="群发返回的 msg_data_id (整数)")
    cm.add_argument("--comment-id", type=int,
                    help="user_comment_id (reply/elect/unelect/delete 必填)")
    cm.add_argument("--index", type=int, default=0, help="多图文时第几篇,从 0 开始")
    cm.add_argument("--content")
    cm.add_argument("--begin", type=int, default=0)
    cm.add_argument("--count", type=int, default=49, help="ls 单页条数,官方 count>=50 会被拒绝")
    cm.add_argument("--type", type=int, default=0)
    cm.add_argument("--yes", action="store_true")
    cm.set_defaults(func=cmd_comment)
    pb = sub.add_parser("publish", help="一键发文: 封面→草稿→发布→轮询")
    pb.add_argument("file", help=".md 或 .json (标准 articles 结构)")
    pb.add_argument("--cover")
    pb.add_argument("--title")
    pb.add_argument("--author")
    pb.add_argument("--digest")
    pb.add_argument("--yes", action="store_true")
    pb.set_defaults(func=cmd_publish)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except WechatApiError as e:
        _emit(e.payload)
        return 1
    except WechatNetworkError as e:
        _emit({"errcode": -2, "errmsg": f"network error: {e}", "rid": None})
        return 2
    except json.JSONDecodeError as e:
        print(f"invalid JSON: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"invalid file path: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
