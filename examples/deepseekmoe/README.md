# Worked Example: DeepSeekMoE

[English](#english) | [中文说明](#中文说明)

## English

This is the primary end-to-end example for Open Paper Analysis. It analyzes
*DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts
Language Models* once, then renders the same evidence-grounded Chinese
manuscript for Markdown, Notion, and Feishu/Lark.

This is a complete paper note rather than a shortened demo. Use it to inspect
analysis depth, cross-platform consistency, native rendering, source quality,
media provenance, and the boundary between reported evidence and research
judgment.

### Explore the Results

| Target | Overview | Full capture or result | Canonical artifact |
| --- | --- | --- | --- |
| Markdown | [Overview PNG](screenshots/markdown.png) | [Read the complete note](markdown.md) | [Portable Markdown](markdown.md) |
| Notion | [Overview JPG](screenshots/notion-overview.jpg) | [Full-length JPG](screenshots/notion-full.jpg) | [Enhanced Markdown body](notion.md) and [logical properties](notion-properties.json) |
| Feishu/Lark | [Overview JPG](screenshots/lark-overview.jpg) | [Full-length JPG](screenshots/lark-full.jpg) | [Native XML document](lark.xml) |
| Shared evidence | [Media preview and license data](media.yaml) | Six extracted visuals and two exact-label markers | [Media and license manifest](media.yaml) |

The Feishu/Lark and Notion images are real platform captures. The Markdown
image is a rendered overview, with the complete portable note linked beside
it. The Notion captures retain the visible recorder property and comment UI
with the owner's explicit approval; they show the page state at capture time.
The Notion body and logical properties remain the canonical verification
artifacts.

### Suggested Reading Path

| Question | Inspect |
| --- | --- |
| What does the paper contribute? | Chapter `0` for the compressed judgment, then chapters `1.2` and `6.1` for the supported contribution claims. |
| How does DeepSeekMoE work? | Chapter `3`, especially Figure 1, fine-grained expert segmentation, shared expert isolation, routing, and load balancing. |
| Which evidence is decisive? | Chapter `4`, including the controlled 2B comparison, ablations, expert-disable proxies, and the 16B compute comparison. |
| What should not be overclaimed? | Chapter `5` for author-confirmed and reproducibility limits, then chapter `7` for the agent's research judgment. |
| How do the paper versions differ? | Chapter `8.1`, which separates the first arXiv release from the formal ACL publication. |
| Can the figures be reused? | [`media.yaml`](media.yaml) for source location, formal label, caption, license, and extraction status. |

### What This Case Demonstrates

- One manuscript preserves paper identity, chapters `0-8`, evidence, metrics,
  limitations, and research judgment across all targets.
- Chapters `3` and `4` adapt to a model/method paper instead of following a
  generic summary template.
- The mechanism is explained through parameter and activation budgets, not
  only through the paper's headline description of expert specialization.
- The evidence section distinguishes controlled 2B experiments, 16B scaling,
  functional proxy tests, efficiency claims, and results that only appear in
  the first arXiv release.
- Six CC BY 4.0 figures and tables demonstrate eligible media extraction;
  Figure 4 and Figure 5 demonstrate exact-label marker fallback.
- Canonical metadata uses official institutions and separates the ACL
  publication month (`published: 2024-08`) from the first arXiv release
  (`preprint_date: 2024-01-11`).
- `contributions` remains compact with four property tags: `细粒专家`, `共享专家`,
  `消融验证`, and `规模扩展`; complete claims and evidence stay in the body.

### Cross-Target Contract

| Semantic element | Markdown | Notion | Feishu/Lark |
| --- | --- | --- | --- |
| Paper identity | YAML plus visible title | Logical database properties plus page title | Compact native information table plus document title |
| Navigation | Linked contents list | Native table of contents | Native heading outline |
| Sources | Portable links | Enhanced-Markdown links | Native link blocks |
| Chapters | Numbered `0-8` headings | Numbered `0-8` page headings | Numbered `0-8` document headings |
| Formulas and tables | Standard Markdown and math | Enhanced Markdown blocks | Native XML blocks |
| Visual evidence | Stable relative assets or markers | Platform uploads or markers | Platform images or markers |
| Verification | File read-back | Body and property read-back | XML/document read-back |

The wording and visual hierarchy may change for each platform, but the paper
identity, claim meaning, metrics, evidence labels, limitations, and research
judgment must not drift.

### Canonical Outputs and Privacy

The Markdown note, Notion body plus logical properties, Lark XML, and media
manifest are the verification source. Automated checks require them to agree
on metadata, sources, chapter order, subsections, and Figure/Table labels.

The Notion fixture is enhanced Markdown accompanied by portable logical
properties, not a workspace-specific API payload. The Lark fixture uses
documented native XML tags. Neither fixture contains a page ID, document token,
private schema, signed URL, account identity, credential, or local path.

Notion follows the
[official enhanced Markdown format](https://developers.notion.com/guides/data-apis/enhanced-markdown),
and Feishu/Lark follows the
[official document block model](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/guide).

Screenshots are presentation aids rather than the source of truth. By default,
published captures exclude account chrome, comments, avatars, personal
properties, workspace names, page or document IDs, and local paths. Visible
display metadata may remain only with explicit owner approval, as in the
Notion captures here; private identifiers, credentials, and authentication
data are never eligible for that exception. User-provided raw captures remain
in the gitignored `screenshots/source/` staging directory until reviewed.

## 中文说明

这是 Open Paper Analysis 的主要端到端案例。它针对
*DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts
Language Models* 只完成一次资料收集、证据整理和研究判断，然后把同一份中文
深度主稿分别渲染为 Markdown、Notion 和飞书文档。案例不是为了展示界面而
缩短的 demo，也不是三份互相独立的摘要，而是一份可以追溯来源、核对指标、
比较平台差异的完整论文笔记。

这个案例适合用来判断 Skill 是否真正完成了以下工作：有没有准确确认论文版本
和机构信息；有没有解释机制而不仅是复述摘要；有没有把实验设置、核心数字和
结论边界连接起来；有没有区分论文报告与 Agent 自己的研究判断；三端渲染后，
章节、图表编号、局限和结论是否仍然一致。

### 结果入口

| 输出目标 | Overview | Full 截图或完整结果 | Canonical 工件 |
| --- | --- | --- | --- |
| Markdown | [概览 PNG](screenshots/markdown.png) | [阅读完整笔记](markdown.md) | [可移植 Markdown](markdown.md) |
| Notion | [概览 JPG](screenshots/notion-overview.jpg) | [完整长图 JPG](screenshots/notion-full.jpg) | [Enhanced Markdown 正文](notion.md)与[逻辑属性](notion-properties.json) |
| 飞书文档 | [概览 JPG](screenshots/lark-overview.jpg) | [完整长图 JPG](screenshots/lark-full.jpg) | [原生 XML 文档](lark.xml) |
| 共享证据 | [媒体与许可概览](media.yaml) | 6 个提取图表与 2 个准确编号 marker | [媒体与许可清单](media.yaml) |

飞书和 Notion 的 Overview、Full 都是真实平台截图；Markdown 提供适合快速
浏览的渲染图，完整内容直接链接到可移植成品。Notion 截图保留了“记录者”属性
与评论界面，已经得到所有者明确同意；它记录的是截图时页面的实际状态。
Notion 正文与逻辑属性仍然是自动校验使用的 canonical 工件。

### 建议阅读顺序

| 想确认什么 | 建议查看 |
| --- | --- |
| 先判断这篇论文值不值得读 | 先看第 `0` 章的一句话判断，再看第 `1.3` 节主要结论。 |
| 理解真正的结构贡献 | 看第 `3` 章，结合 Figure 1 理解细粒度专家切分、共享专家隔离、路由预算和负载均衡。 |
| 核对最有说服力的实验 | 看第 `4.1` 节受控 2B 实验、第 `4.2-4.4` 节消融与功能代理、第 `4.5` 节 16B 扩展。 |
| 分辨“更省计算”和“所有任务更强” | 对照第 `4.5` 节的 FLOPs、总体结果与多项选择任务差异，再看第 `5.3` 节因果解释边界。 |
| 判断结论能否复现 | 看第 `5` 章的数据、训练、系统效率和发布边界。 |
| 了解分析者自己的判断 | 看第 `7` 章；这里与论文直接报告的事实明确分开。 |
| 核对版本差异 | 看第 `8.1` 节，区分 arXiv 首次版本中的 Chat/145B 结果与 ACL 正式发表范围。 |
| 核对图表来源和许可 | 查看 [`media.yaml`](media.yaml)，其中记录正式编号、caption、来源位置、许可与处理方式。 |

### 这份分析具体做了什么

**第一，确认论文身份与版本。** 元数据中的“机构”来自正式论文，不使用作者
姓名代替机构；`published: 2024-08` 表示 ACL 2024 正式发表月份，
`preprint_date: 2024-01-11` 表示 arXiv 首次公开日期。正文第 `8.1` 节进一步
解释两版范围不同，避免把 arXiv v1 的 Chat SFT 和 145B 初步实验当成 ACL
正式版本的同行评审结论。

**第二，解释机制而不是只列贡献点。** 第 `3` 章从 FFN 专家参数与 token
激活预算出发，说明 fine-grained expert segmentation 如何扩大专家组合空间，
shared expert isolation 如何固定承载通用知识，以及负载均衡损失和 expert
parallelism 如何影响真实实现。这样可以看出 DeepSeekMoE 改变的是同一计算
预算下的专家组织方式，而不是简单增加总参数。

**第三，把结论绑定到证据。** 第 `4` 章区分四种证据：同设置下的 2B 受控
比较、结构消融、屏蔽专家后的功能代理实验，以及 16B 模型与 7B dense
baseline 的能力和计算量对比。每个关键 Figure/Table 都紧邻解释，同时说明
它能支持什么、不能单独证明什么。

**第四，保留失败条件与边界。** 第 `5` 章记录未公开训练数据、缺少多随机
种子、真实吞吐和通信成本不足、145B 未完成训练等限制。第 `7` 章再给出研究
判断：论文充分证明了 FFN 专家参数利用率的改进，但没有证明稀疏 MoE 能无代价
替代 dense 模型的全部能力来源。

**第五，让元数据适合平台属性而不牺牲正文。** `topics` 与 `contributions`
各不超过 4 项，贡献属性只保留 `细粒专家`、`共享专家`、`消融验证`、`规模扩展`
四个短标签。完整贡献、数字和证据都留在第 `1`、`4`、`6` 章，不把长句塞进
Notion 或飞书的属性区。

### 三端如何保持一致

| 语义内容 | Markdown | Notion | 飞书文档 |
| --- | --- | --- | --- |
| 论文身份 | YAML 元数据与可见标题 | 数据库逻辑属性与页面标题 | 顶部紧凑信息表与文档标题 |
| 导航 | 可点击目录 | 原生目录块 | 原生标题大纲 |
| 来源 | 标准 Markdown 链接 | Enhanced Markdown 链接块 | 原生链接块 |
| 正文 | `0-8` 编号章节 | `0-8` 页面标题 | `0-8` 文档标题 |
| 公式与表格 | 标准 Markdown/数学公式 | Enhanced Markdown 原生块 | XML 原生块 |
| 图表 | 稳定相对资源或 marker | 平台上传图片或 marker | 平台图片或 marker |
| 核验 | 文件读回 | 正文与属性读回 | XML/文档读回 |

平台可以有不同的标题层级、目录、属性表和媒体块，但论文身份、核心数字、证据
含义、图表编号、局限和研究判断不能漂移。自动检查会同时读取
[`markdown.md`](markdown.md)、[`notion.md`](notion.md)、
[`notion-properties.json`](notion-properties.json)、[`lark.xml`](lark.xml) 和
[`media.yaml`](media.yaml)，核对元数据、来源、章节顺序、小节和 Figure/Table
标签。

### 截图、工件与隐私边界

Canonical 工件是验证源，截图只是展示平台原生排版的辅助材料。Notion fixture
使用 enhanced Markdown 正文和可移植逻辑属性，而不是某个工作区专属 API
payload；飞书 fixture 使用公开文档支持的 XML 标签。公开工件不包含页面 ID、
文档 token、私有 schema、签名 URL、账号身份、凭据或本地路径。

公开截图默认不显示账号栏、评论、头像、个人属性、工作区名称、页面或文档 ID，
并且不能让读者误以为截图就是 API fixture。得到所有者明确授权后，可以保留
可见展示信息，本案例的 Notion 截图即属于这种情况；私有 ID、凭据和认证数据
永远不在例外范围内。论文原始图表放在 [`assets/`](assets/)，平台截图放在
[`screenshots/`](screenshots/)，用户提供但尚未审核的原图放在被 Git 忽略的
`screenshots/source/`，三者不会混在一起。
