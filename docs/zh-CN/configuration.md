# 配置

[English](../en/configuration.md) | [简体中文](../zh-CN/configuration.md)

## 查找顺序

配置不是运行前提。Skill 按以下顺序读取第一个存在的文件：

1. 用户在请求中明确提供的路径。
2. 当前项目的 `.open-paper-analysis.toml`。
3. `~/.config/open-paper-analysis/config.toml`。

可以从 `skills/analyze-paper/assets/config.example.toml` 开始配置。不要
提交填入了真实目标的本地配置。

## 配置 schema

```toml
version = 2

[defaults]
outputs = ["markdown"]
language = "auto"
depth = "deep"

[media]
mode = "markers"
max_items = 6
license_policy = "open-or-approved"

[markdown]
notes_directory = "paper-notes"
assets_directory = "assets"

[notion]
database_id = ""
data_source_id = ""
template_page_id = ""

[lark]
parent_token = ""
parent_position = ""
doc_format = "xml"
```

### 默认值

`outputs` 可包含一个或多个互不重复的 `markdown`、`notion`、
`lark`。`language = "auto"` 跟随用户语言。`depth = "deep"` 是完整
分析唯一的深度档，但实际长度始终受有效证据约束。

### 媒体

`mode` 支持：

- `markers`：保留准确 Figure/Table 编号与分析，不上传图片。
- `extract`：在 `max_items` 上限内精选并发布符合条件的媒体。
- `off`：省略独立媒体块，但仍在正文解释关键证据。

`open-or-approved` 表示只有开放许可、用户提供或得到明确授权的素材才
允许自动提取。

### Markdown

`notes_directory` 控制默认笔记目录，`assets_directory` 控制提取素材
使用的稳定相对路径。

### Notion

数据库或 data source 目标只写在本地配置中，模板可选。
`[notion.properties]` 把 canonical metadata 映射到实时数据库 schema；
`[notion.values]` 可配置固定 select 值。未映射的可选字段直接跳过。

实时 schema 同时提供对应属性时，将 `published` 映射为正式发表日期，
将 `preprint_date` 独立映射为预印本首次公开日期。

发布前必须读取实时 schema，不能假定另一个工作区的私有属性名。

### 飞书

`parent_token` 和 `parent_position` 指向目标文件夹、知识库节点或
library position；也可都留空，在请求中临时指定。若工具要求二者互斥，
必须遵守。文档默认采用 XML。

## Schema 校验

Skill 只支持包含 `version = 2` 的配置文件。版本缺失或版本号不同时，不进行
自动迁移，也不猜测旧键含义。Agent 会明确报告配置问题；若继续执行是安全的，
则只使用用户当次请求和内置 Markdown 默认值。论文分析不会自动改写用户的
配置文件。

## 凭据边界

配置可以保存目标位置和属性映射，但不得保存 API key、OAuth token、
cookie、client secret、上传 token、签名媒体 URL、用户身份或其他凭据。
认证应由已连接工具、MCP、CLI 凭据存储或宿主环境负责。

不要在 issue、PR、fixture、笔记正文或测试日志中粘贴填充后的本地配置。
