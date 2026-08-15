# 开发

[English](../en/development.md) | [简体中文](../zh-CN/development.md)

## 仓库结构

```text
skills/analyze-paper/       唯一跨 Agent canonical Skill
  SKILL.md                  精简执行流程
  references/               内容、质量、媒体和后端契约
  assets/                   公开配置示例
  scripts/                  工件验证器
examples/deepseekmoe/       三端 golden example 与开放媒体
evals/cases.yaml            行为评测矩阵
scripts/                    安装器与仓库检查
docs/en, docs/zh-CN         镜像指南
```

仓库只维护一份 Skill。安装器将它复制到 Codex、Claude Code 或通用
Agent Skills 目录，不为不同宿主维护多份正文。

## 本地验证

```bash
npx --yes skills-ref@0.1.5 validate skills/analyze-paper
python /path/to/skill-creator/scripts/quick_validate.py skills/analyze-paper
python skills/analyze-paper/scripts/validate_note.py examples/deepseekmoe/markdown.md
python skills/analyze-paper/scripts/validate_note.py examples/deepseekmoe/notion.md
python skills/analyze-paper/scripts/validate_note.py examples/deepseekmoe/lark.xml
python scripts/validate_examples.py
python scripts/check_markdown_links.py
python scripts/check_docs_parity.py
bash scripts/test-install.sh
```

CI 还会解析配置、编译 Python 脚本、用 Gitleaks 扫描 Git 历史，并验证所有
安装目标。

## 评测矩阵

行为用例覆盖 model/method、benchmark、system、survey、标题解析、安全
更新、重复歧义、marker/extract 媒体、多目标部分失败、平台不可用和只读
输出。

Forward test 至少包含：

- 一篇 method 论文渲染到三个目标。
- 一篇 dataset/benchmark 论文，确认章节 `3-4` 不退化为模型报告。
- 一次部分失败，证明不可用后端不会回滚 Markdown。

## 真实冒烟测试

使用带明确测试标记的临时标题和非生产目标。Notion 与飞书都执行：

1. 写入属性/标题、正文、公式、链接和媒体。
2. 读回并核验章节、元数据和证据编号。
3. 只截取正文，不显示账号与工作区 chrome。
4. 将临时工件移入回收站。
5. PR 中只记录脱敏状态和数量。

不得提交测试 URL、page/document ID、私有 schema、账号名、签名媒体 URL
或本地配置。未安装 Claude Code 时，明确记录未执行 Claude runtime；
目录和 Skill 格式兼容检查仍然必须通过。

## 贡献

改动应遵守 content contract 和既有平台规范。只有在确实阻止三端漂移或
减少验证重复时才增加抽象。后端行为变化应同步更新 reference、golden
fixture、validator、评测用例、中英文文档和 PR 测试证据。
