# API 目录

> 自动生成自 `scripts/endpoints.json`(由 `wechat_mp.py list` 输出),共 134 个端点 / 22 个分类。
> 改注册表后请重新生成,勿手改本文件。

按注册名调用: `python3 scripts/wechat_mp.py call <id> --data '<json>'`;destructive 端点需加 `--yes`。


## openApi管理 (5)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `quota_clear_all` | 重置API调用次数 | POST | `/cgi-bin/clear_quota` | ⚠️ yes |
| `quota_get` | 查询API调用额度 | POST | `/cgi-bin/openapi/quota/get` | - |
| `rid_get` | 查询rid信息 | POST | `/cgi-bin/openapi/rid/get` | - |
| `quota_clear_all_v2` | 用AppSecret重置API调用次数 | POST | `/cgi-bin/clear_quota/v2` | ⚠️ yes |
| `quota_clear` | 重置指定API调用次数 | POST | `/cgi-bin/openapi/quota/clear` | ⚠️ yes |

## 一次性订阅消息 (1)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `subscribe_send` | 发送一次性订阅消息 | POST | `/cgi-bin/message/template/subscribe` | - |

## 会话控制 (5)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `kfsession_create` | 创建会话 | POST | `/customservice/kfsession/create` | - |
| `kfsession_close` | 关闭会话 | POST | `/customservice/kfsession/close` | - |
| `kfsession_get` | 获取客户会话状态 | GET | `/customservice/kfsession/getsession` | - |
| `kfsession_list` | 获取客服会话列表 | GET | `/customservice/kfsession/getsessionlist` | - |
| `kfsession_waitcase` | 获取未接入会话列表 | GET | `/customservice/kfsession/getwaitcase` | - |

## 发布能力 (5)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `freepublish_submit` | 发布草稿 | POST | `/cgi-bin/freepublish/submit` | ⚠️ yes |
| `freepublish_get` | 发布状态查询 | POST | `/cgi-bin/freepublish/get` | - |
| `freepublish_delete` | 删除发布文章 | POST | `/cgi-bin/freepublish/delete` | ⚠️ yes |
| `freepublish_batchget` | 获取已发布的消息列表 | POST | `/cgi-bin/freepublish/batchget` | - |
| `freepublish_getarticle` | 获取已发布图文信息 | POST | `/cgi-bin/freepublish/getarticle` | - |

## 商品卡片 (1)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `product_card_info` | 获取商品卡片的DOM结构 | POST | `/channels/ec/service/product/getcardinfo` | - |

## 基础接口 (5)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `stable_token` | 获取稳定版接口调用凭据 | POST | `/cgi-bin/stable_token` | - |
| `token_get` | 获取接口调用凭据 | GET | `/cgi-bin/token` | - |
| `callback_check` | 网络通信检测 | POST | `/cgi-bin/callback/check` | - |
| `get_api_domain_ip` | 获取微信API服务器IP | GET | `/cgi-bin/get_api_domain_ip` | - |
| `getcallbackip` | 获取微信推送服务器IP | GET | `/cgi-bin/getcallbackip` | - |

## 客服消息 (3)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `kf_msg_send` | 发送客服消息 | POST | `/cgi-bin/message/custom/send` | - |
| `kf_typing` | 客服输入状态 | POST | `/cgi-bin/message/custom/typing` | - |
| `msg_record` | 获取聊天记录 | POST | `/customservice/msgrecord/getmsglist` | - |

## 客服管理 (7)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `kflist` | 获取所有客服账号 | GET | `/cgi-bin/customservice/getkflist` | - |
| `kfonlinelist` | 获取在线客服列表 | GET | `/cgi-bin/customservice/getonlinekflist` | - |
| `kfaccount_add` | 添加客服账号 | POST | `/customservice/kfaccount/add` | - |
| `kfaccount_update` | 修改客服账号 | POST | `/customservice/kfaccount/update` | - |
| `kfaccount_del` | 删除客服账号 | POST | `/customservice/kfaccount/del` | ⚠️ yes |
| `kfaccount_invite` | 邀请绑定客服账号 | POST | `/customservice/kfaccount/inviteworker` | - |
| `kf_uploadheadimg` | 设置客服头像 | POST | `/customservice/kfaccount/uploadheadimg` | - |

## 就医助手 (1)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `cityservice_send` | 发送就医助手消息 | POST | `/cityservice/sendchannelmsg` | - |

## 微信门店 (12)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `store_category` | 获取门店类目表 | POST | `/wxa/get_merchant_category` | - |
| `store_apply` | 申请开通门店功能 | POST | `/wxa/apply_merchant` | - |
| `store_audit_info` | 查询门店功能审核信息 | POST | `/wxa/get_merchant_audit_info` | - |
| `store_modify` | 修改门店基本信息 | POST | `/wxa/modify_merchant` | - |
| `district_get` | 获取省市区信息 | POST | `/wxa/get_district` | - |
| `map_poi_search` | 搜索地图POI | POST | `/wxa/search_map_poi` | - |
| `store_add` | 添加门店 | POST | `/wxa/add_store` | - |
| `store_info` | 获取门店信息 | POST | `/wxa/get_store_info` | - |
| `store_list` | 获取门店列表 | POST | `/wxa/get_store_list` | - |
| `store_del` | 删除门店 | POST | `/wxa/del_store` | ⚠️ yes |
| `store_update` | 更新门店信息 | POST | `/wxa/update_store` | - |
| `map_poi_create` | 在地图创建新的POI | POST | `/wxa/create_map_poi` | - |

## 数据统计 (21)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `getusersummary` | 获取用户增减数据 | POST | `/datacube/getusersummary` | - |
| `getusercumulate` | 获取累计用户数据 | POST | `/datacube/getusercumulate` | - |
| `getarticlesummary` | 获取图文群发每日数据 | POST | `/datacube/getarticlesummary` | - |
| `getarticletotal` | 获取图文群发总数据 | POST | `/datacube/getarticletotal` | - |
| `getuserread` | 获取图文统计数据 | POST | `/datacube/getuserread` | - |
| `getuserreadhour` | 获取图文统计分时数据 | POST | `/datacube/getuserreadhour` | - |
| `getusershare` | 获取图文分享转发数据 | POST | `/datacube/getusershare` | - |
| `getusersharehour` | 获取图文分享转发分时数据 | POST | `/datacube/getusersharehour` | - |
| `getupstreammsg` | 获取消息发送概况数据 | POST | `/datacube/getupstreammsg` | - |
| `getupstreammsghour` | 获取消息发送分时数据 | POST | `/datacube/getupstreammsghour` | - |
| `getupstreammsgweek` | 获取消息发送周数据 | POST | `/datacube/getupstreammsgweek` | - |
| `getupstreammsgmonth` | 获取消息发送月数据 | POST | `/datacube/getupstreammsgmonth` | - |
| `getupstreammsgdist` | 获取消息发送分布数据 | POST | `/datacube/getupstreammsgdist` | - |
| `getupstreammsgdistweek` | 获取消息发送分布周数据 | POST | `/datacube/getupstreammsgdistweek` | - |
| `getupstreammsgdistmonth` | 获取消息发送分布月数据 | POST | `/datacube/getupstreammsgdistmonth` | - |
| `getarticleread` | 获取图文阅读数据 | POST | `/datacube/getarticleread` | - |
| `getarticleshare` | 获取图文分享数据 | POST | `/datacube/getarticleshare` | - |
| `getbizsummary` | 获取公众号概况数据 | POST | `/datacube/getbizsummary` | - |
| `getarticletotaldetail` | 获取图文群发总数据明细 | POST | `/datacube/getarticletotaldetail` | - |
| `getinterfacesummary` | 获取接口分析数据 | POST | `/datacube/getinterfacesummary` | - |
| `getinterfacesummaryhour` | 获取接口分析分时数据 | POST | `/datacube/getinterfacesummaryhour` | - |

## 智能接口 (12)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `voice_translate` | 提交语音翻译内容 | POST | `/cgi-bin/media/voice/translatecontent` | - |
| `voice_add` | 提交语音内容进语音识别 | POST | `/cgi-bin/media/voice/addvoicetorecofortext` | - |
| `voice_query` | 获取语音识别结果 | POST | `/cgi-bin/media/voice/queryrecoresultfortext` | - |
| `ocr_menu` | OCR菜单识别 | POST | `/cv/ocr/menu` | - |
| `ocr_comm` | OCR通用印刷体识别 | POST | `/cv/ocr/comm` | - |
| `ocr_driving` | OCR行驶证识别 | POST | `/cv/ocr/driving` | - |
| `ocr_bankcard` | OCR银行卡识别 | POST | `/cv/ocr/bankcard` | - |
| `ocr_bizlicense` | OCR营业执照识别 | POST | `/cv/ocr/bizlicense` | - |
| `ocr_drivinglicense` | OCR驾驶证识别 | POST | `/cv/ocr/drivinglicense` | - |
| `ocr_idcard` | OCR身份证识别 | POST | `/cv/ocr/idcard` | - |
| `img_aicrop` | 图片智能裁剪 | POST | `/cv/img/aicrop` | - |
| `img_qrcode` | 图片二维码识别 | POST | `/cv/img/qrcode` | - |

## 标签管理 (8)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `tags_get` | 获取标签 | GET | `/cgi-bin/tags/get` | - |
| `tags_create` | 创建标签 | POST | `/cgi-bin/tags/create` | - |
| `tags_update` | 编辑标签 | POST | `/cgi-bin/tags/update` | - |
| `tags_delete` | 删除标签 | POST | `/cgi-bin/tags/delete` | ⚠️ yes |
| `user_tag_get` | 获取标签下粉丝列表 | POST | `/cgi-bin/user/tag/get` | - |
| `batchtagging` | 批量为用户打标签 | POST | `/cgi-bin/tags/members/batchtagging` | - |
| `batchuntagging` | 批量为用户取消标签 | POST | `/cgi-bin/tags/members/batchuntagging` | - |
| `tag_getidlist` | 获取用户的标签列表 | POST | `/cgi-bin/tags/getidlist` | - |

## 用户信息 (7)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `user_info` | 获取用户基本信息 | GET | `/cgi-bin/user/info` | - |
| `user_info_batchget` | 批量获取用户基本信息 | POST | `/cgi-bin/user/info/batchget` | - |
| `user_get` | 获取关注用户列表 | GET | `/cgi-bin/user/get` | - |
| `blacklist_get` | 获取公众号的黑名单列表 | POST | `/cgi-bin/tags/members/getblacklist` | - |
| `blacklist_batch` | 拉黑用户 | POST | `/cgi-bin/tags/members/batchblacklist` | ⚠️ yes |
| `blacklist_batchun` | 取消拉黑用户 | POST | `/cgi-bin/tags/members/batchunblacklist` | - |
| `user_remark` | 设置用户备注名 | POST | `/cgi-bin/user/info/updateremark` | - |

## 用户管理 (1)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `changeopenid` | 转换openid | POST | `/cgi-bin/changeopenid` | - |

## 留言管理 (8)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `comment_open` | 打开已群发文章评论 | POST | `/cgi-bin/comment/open` | - |
| `comment_close` | 关闭已群发文章评论 | POST | `/cgi-bin/comment/close` | - |
| `comment_list` | 查看指定文章的评论数据 | POST | `/cgi-bin/comment/list` | - |
| `comment_markelect` | 评论标记精选 | POST | `/cgi-bin/comment/markelect` | ⚠️ yes |
| `comment_unmarkelect` | 评论取消精选 | POST | `/cgi-bin/comment/unmarkelect` | ⚠️ yes |
| `comment_delete` | 删除评论 | POST | `/cgi-bin/comment/delete` | ⚠️ yes |
| `comment_reply_add` | 回复评论 | POST | `/cgi-bin/comment/reply/add` | - |
| `comment_reply_delete` | 删除回复 | POST | `/cgi-bin/comment/reply/delete` | ⚠️ yes |

## 素材管理 (9)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `material_add` | 上传永久素材 | POST | `/cgi-bin/material/add_material` | - |
| `material_get` | 获取永久素材 | POST | `/cgi-bin/material/get_material` | - |
| `material_count` | 获取永久素材总数 | GET | `/cgi-bin/material/get_materialcount` | - |
| `material_batchget` | 获取永久素材列表 | POST | `/cgi-bin/material/batchget_material` | - |
| `material_del` | 删除永久素材 | POST | `/cgi-bin/material/del_material` | ⚠️ yes |
| `media_uploadimg` | 上传发表内容中的图片 | POST | `/cgi-bin/media/uploadimg` | - |
| `media_upload` | 新增临时素材 | POST | `/cgi-bin/media/upload` | - |
| `media_get` | 获取临时素材 | GET | `/cgi-bin/media/get` | - |
| `media_get_jssdk` | 获取高清语音素材 | GET | `/cgi-bin/media/get/jssdk` | - |

## 网页开发 (1)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `ticket_get` | 获取sdk临时票据 | GET | `/cgi-bin/ticket/getticket` | - |

## 群发消息 (7)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `mass_sendall` | 根据标签群发消息 | POST | `/cgi-bin/message/mass/sendall` | ⚠️ yes |
| `mass_delete` | 删除群发消息 | POST | `/cgi-bin/message/mass/delete` | ⚠️ yes |
| `mass_preview` | 预览消息 | POST | `/cgi-bin/message/mass/preview` | - |
| `mass_get` | 查询群发消息发送状态 | POST | `/cgi-bin/message/mass/get` | - |
| `mass_speed_get` | 获取群发速度 | POST | `/cgi-bin/message/mass/speed/get` | - |
| `mass_speed_set` | 设置群发速度 | POST | `/cgi-bin/message/mass/speed/set` | - |
| `uploadnews` | 上传图文消息素材(旧) | POST | `/cgi-bin/media/uploadnews` | - |

## 自动回复 (1)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `autoreply_info` | 获取自动回复规则 | GET | `/cgi-bin/get_current_autoreply_info` | - |

## 自定义菜单 (7)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `menu_create` | 创建自定义菜单 | POST | `/cgi-bin/menu/create` | ⚠️ yes |
| `selfmenu_info` | 查询自定义菜单信息 | GET | `/cgi-bin/get_current_selfmenu_info` | - |
| `menu_get` | 获取自定义菜单配置 | GET | `/cgi-bin/menu/get` | - |
| `menu_delete` | 删除自定义菜单 | POST | `/cgi-bin/menu/delete` | ⚠️ yes |
| `menu_addconditional` | 创建个性化菜单 | POST | `/cgi-bin/menu/addconditional` | ⚠️ yes |
| `menu_delconditional` | 删除个性化菜单 | POST | `/cgi-bin/menu/delconditional` | ⚠️ yes |
| `menu_trymatch` | 测试个性化菜单匹配结果 | POST | `/cgi-bin/menu/trymatch` | - |

## 草稿管理 (7)

| id | name | method | path | destructive |
|---|---|---|---|---|
| `draft_count` | 获取草稿的总数 | GET | `/cgi-bin/draft/count` | - |
| `draft_add` | 新增草稿 | POST | `/cgi-bin/draft/add` | - |
| `draft_delete` | 删除草稿 | POST | `/cgi-bin/draft/delete` | ⚠️ yes |
| `draft_switch` | 草稿箱开关设置 | POST | `/cgi-bin/draft/switch` | ⚠️ yes |
| `draft_get` | 获取草稿详情 | POST | `/cgi-bin/draft/get` | - |
| `draft_update` | 更新草稿 | POST | `/cgi-bin/draft/update` | - |
| `draft_batchget` | 获取草稿列表 | POST | `/cgi-bin/draft/batchget` | - |
