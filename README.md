# Open Paper Analysis

An open, portable Agent Skill for evidence-grounded analysis of a single
research paper.

Open Paper Analysis turns an arXiv page, PDF, DOI, title, project page, code
repository, or existing note into a structured Markdown paper note. It keeps
the analysis centered on primary sources, adapts the note to the paper type,
and verifies the finished artifact. Notion publishing is optional.

## Highlights

- Works with OpenAI Codex, Claude Code, and other Agent Skills-compatible tools.
- Handles model/method, dataset/benchmark, system/tool, survey/position, and
  technical-report papers.
- Produces portable Markdown by default.
- Uses an available isolated worker for single-paper analysis when the host
  supports one, while retaining an inline fallback.
- Can publish to Notion through a connected tool or the `ntn` CLI without
  making Notion a hard dependency.
- Keeps personal database IDs, property names, and credentials outside the
  public Skill.

## Install

Install for Codex:

```bash
./scripts/install.sh --target codex
```

Install for Claude Code:

```bash
./scripts/install.sh --target claude
```

Install into a project-level open Agent Skills directory:

```bash
./scripts/install.sh --target agents --dest /path/to/project/.agents/skills
```

Existing installations are protected. Pass `--force` to replace one, or
`--dry-run` to inspect the destination without writing.

## Use

Invoke the Skill explicitly or ask the agent to analyze a paper:

```text
Use $analyze-paper to analyze https://arxiv.org/abs/2607.01233.
```

Unless another destination is requested or configured, the Skill writes
`paper-notes/<paper-slug>.md`. Copy
`skills/analyze-paper/assets/config.example.toml` to
`.open-paper-analysis.toml` or
`~/.config/open-paper-analysis/config.toml` to change defaults or enable
Notion publishing.

## 中文

Open Paper Analysis 是一个开放、可移植的单篇论文深度分析 Skill。它支持
Codex、Claude Code 和其他兼容 Agent Skills 规范的工具，可以从 arXiv、
PDF、DOI、论文标题、项目主页、代码仓库或已有笔记出发，生成经过核验的
结构化 Markdown 论文笔记。

默认输出为 `paper-notes/<paper-slug>.md`，Notion 是可选发布后端，不是
运行前提。公开仓库不包含个人数据库 ID、属性名称或凭据。

安装到 Codex：

```bash
./scripts/install.sh --target codex
```

安装到 Claude Code：

```bash
./scripts/install.sh --target claude
```

安装到通用项目级目录：

```bash
./scripts/install.sh --target agents --dest /path/to/project/.agents/skills
```

## Development

Validate the Skill and repository:

```bash
npx --yes skills-ref@0.1.5 validate skills/analyze-paper
python /path/to/skill-creator/scripts/quick_validate.py skills/analyze-paper
python scripts/check_markdown_links.py
bash scripts/test-install.sh
```

Claude Code is not required to use or package the Skill. Runtime behavior
should still be smoke-tested in Claude Code when that client is available.

## License

Apache-2.0
