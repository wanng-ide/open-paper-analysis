# 快速开始

[English](../en/getting-started.md) | [简体中文](../zh-CN/getting-started.md)

## 运行条件

本仓库提供唯一 canonical Agent Skill，不是独立应用或 SDK。可直接使用
支持 Agent Skills 的宿主，也可以让其他 Agent 读取
`skills/analyze-paper/SKILL.md`。

远程发布都是可选能力：

- Markdown 只需要可写目录。
- Notion 需要已连接的 Notion 工具/MCP，或已认证的 `ntn` CLI。
- 飞书需要已连接的文档工具/MCP，或已认证的 `lark-cli`。

凭据始终留在宿主或 CLI 的凭据存储中。

## 安装

在仓库根目录运行：

```bash
./scripts/install.sh --target codex
./scripts/install.sh --target claude
./scripts/install.sh --target agents --dest /path/to/project/.agents/skills
```

安装器默认保护已有安装。使用 `--dry-run` 查看目标路径；只有明确使用
`--force` 时才替换现有 Skill。

## 第一次分析

普通自然语言请求即可触发：

```text
使用 $analyze-paper，用中文分析 https://arxiv.org/abs/2401.06066。
```

Markdown 是零配置默认。可写环境生成
`paper-notes/<paper-slug>.md`；只读环境直接在回复中返回完整 Markdown。

一次请求多个目标：

```text
用中文深度分析这篇论文，同时生成 Markdown，并把同一主稿发布到 Notion
和飞书。保留图表编号 marker，不提取图片。
```

当次请求中的目标、语言和媒体模式优先于配置。

## Agent 的执行过程

1. 确认唯一论文，并在每个目标中查重。
2. 收集一手来源，判断论文类型。
3. 建立 evidence map 和可选 media manifest。
4. 只写一份目标无关的深度语义稿。
5. 从这份主稿渲染所有选择的目标。
6. 逐个读回工件，并报告各目标自己的状态。

宿主支持隔离 worker 时，主 Agent 会把完整单篇流程交给一个全新 worker，
不会把章节拆给多个互不知情的写作者。没有 worker 时，同一契约在当前
Agent 内执行。

## 完成状态

每个目标单独返回：

- `success`：写入并读回成功。
- `partial`：分析完成，但远程发布或部分媒体失败；仍保留离线工件或
  Markdown 保底。
- `blocked`：该目标无法安全创建或更新，例如查重结果存在歧义。

一个目标失败不会删除或回滚其他成功工件。
