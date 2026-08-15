# Worked Example: DeepSeekMoE

[中文说明](#中文说明)

This is the primary end-to-end example for Open Paper Analysis. It analyzes
*DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts
Language Models* once, then renders the same evidence-grounded Chinese
manuscript for all three supported backends.

Use this case to judge the actual depth and portability of the Skill. It is a
complete paper note rather than a quick-start excerpt or a visual mockup.

## Start Here

| Goal | Open |
| --- | --- |
| Read the finished analysis | [Portable Markdown note](markdown.md) |
| Inspect the Notion rendering | [Enhanced-Markdown body](notion.md) and [logical properties](notion-properties.json) |
| Inspect the Feishu/Lark rendering | [Native XML document](lark.xml) |
| Audit figures, sources, and reuse rights | [Media and license manifest](media.yaml) |

## What This Case Demonstrates

- One manuscript preserves paper identity, chapters `0-8`, evidence, metrics,
  limitations, and research judgment across all targets.
- Chapters `3` and `4` adapt to a model/method paper instead of following a
  generic summary template.
- Six CC BY 4.0 figures and tables demonstrate eligible media extraction;
  Figure 4 and Figure 5 demonstrate exact-label marker fallback.
- Canonical metadata uses official institutions and separates the ACL
  publication month (`published: 2024-08`) from the first arXiv release
  (`preprint_date: 2024-01-11`).
- `contributions` stays compact with four property tags: `细粒专家`, `共享专家`,
  `消融验证`, and `规模扩展`; full claims and evidence remain in chapters `1`
  and `6`.

## Canonical Outputs

The Markdown note, Notion body plus logical properties, Lark XML, and media
manifest are the verification source. Automated checks require them to agree
on metadata, sources, chapter order, subsections, and Figure/Table labels.

The Notion fixture is an enhanced-Markdown page body, accompanied by portable
logical properties rather than a workspace-specific API payload. The Lark
fixture uses documented native XML tags. Neither fixture contains a page ID,
document token, private schema, signed URL, account identity, credential, or
local path.

Notion follows the
[official enhanced Markdown format](https://developers.notion.com/guides/data-apis/enhanced-markdown),
and Feishu/Lark follows the
[official document block model](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/guide).

## Visual Captures

Screenshots are presentation aids, not canonical output. A compact overview is
intended for README display; a full-length capture is linked for readers who
want to inspect native layout over the complete document. Raw captures stay
outside the published gallery until they:

- match the canonical manuscript version;
- exclude account chrome, comments, avatars, personal properties, workspace
  names, page or document IDs, and local paths;
- remain legible without implying that a platform screenshot is an API
  fixture.

Paper figures belong in [`assets/`](assets/). Platform captures belong in
[`screenshots/`](screenshots/); keeping those roles separate prevents source
evidence from being confused with documentation imagery. User-provided source
captures are staged in the gitignored `screenshots/source/` directory. Publish
only reviewed exports named `<target>-overview` and `<target>-full`.

## 中文说明

这是 Open Paper Analysis 的主要端到端案例。Skill 只分析一次
*DeepSeekMoE*，再把同一份有证据支撑的中文深度稿渲染为 Markdown、Notion
和飞书三种输出。它不是缩短版演示，也不是为了截图拼出的视觉样稿。

### 建议阅读顺序

| 想看什么 | 对应工件 |
| --- | --- |
| 直接阅读完整分析 | [Markdown 成品](markdown.md) |
| 检查 Notion 渲染 | [Enhanced Markdown 正文](notion.md)与[逻辑属性](notion-properties.json) |
| 检查飞书渲染 | [原生 XML 文档](lark.xml) |
| 核对图表、来源和许可 | [媒体与许可清单](media.yaml) |

这个案例重点验证：三端共享论文身份和 `0-8` 章节；第 `3`、`4` 章随
model/method 类型动态组织；六张开放许可图表与两个 marker 可以混合使用；
正式发表和 arXiv 首次公开日期不会混淆；`contributions` 只保留四个短标签，
完整贡献与证据仍在正文展开。

Markdown、Notion fixture、飞书 XML 和媒体清单才是自动校验使用的 canonical
工件。截图只负责展示平台原生排版：README 使用便于浏览的概览图，完整长图
只提供链接。任何截图在公开前都必须与当前正文一致，并移除账号、评论、头像、
个人属性、工作区名称、页面 ID、文档 token 和本地路径。

论文图表统一放在 [`assets/`](assets/)，平台截图统一放在
[`screenshots/`](screenshots/)，避免把论文证据素材和项目展示图片混在一起。
用户提供的原始截图暂存在被 Git 忽略的 `screenshots/source/`；审核后只公开
命名为 `<target>-overview` 和 `<target>-full` 的导出版本。
