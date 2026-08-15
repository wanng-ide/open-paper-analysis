# Open Paper Analysis 文档

[English](../en/README.md) | [简体中文](../zh-CN/README.md)

Open Paper Analysis 是一个可移植的单篇论文深度分析 Agent Skill。它先形成
一份有证据支撑的语义主稿，再把同一主稿渲染为 Markdown、Notion、飞书
文档，或一次输出其中任意组合。

建议先看完整的
[DeepSeekMoE 三端案例](../../examples/deepseekmoe/README.md)：可阅读成品、
canonical 后端工件、证据清单和截图规范都集中在同一个入口。

## 指南

- [快速开始](getting-started.md)：安装、调用和理解一次运行。
- [配置](configuration.md)：version 2 schema、目标选择和校验行为。
- [输出后端](outputs.md)：Markdown、Notion enhanced Markdown、飞书
  XML，以及部分失败时的行为。
- [质量、媒体与安全](quality-media-safety.md)：深度标准、证据锚点、素材
  权限、更新安全和隐私。
- [开发](development.md)：仓库结构、验证、评测、真实冒烟测试和贡献流程。
