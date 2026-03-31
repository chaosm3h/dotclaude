# dotclaude
クロスデバイス用ClaudeCodeユーザースコープ設定ファイル

## 状況の整理

まず現状を把握します。

**公式のクロスデバイス同期機能はまだ存在しません。** GitHubのIssueで複数回リクエストされていますが、Anthropic側からの公式回答はまだありません。

---

## 同期すべきファイル・しないファイル

ユーザースコープの設定は `~/.claude/` 配下に保存されています。

| ファイル/ディレクトリ | 内容 | 同期する？ |
|---|---|---|
| `~/.claude/settings.json` | ユーザー設定 | ✅ |
| `~/.claude/CLAUDE.md` | グローバル指示 | ✅ |
| `~/.claude/agents/` | カスタムエージェント | ✅ |
| `~/.claude/skills/` | スキル | ✅ |
| `~/.claude/rules/` | カスタムルール | ✅ |
| `~/.claude/commands/` | スラッシュコマンド | ✅ |
| `~/.claude/settings.local.json` | マシン固有の設定 | ❌ |
| `~/.claude.json` | OAuthセッション・MCP設定・プロジェクト状態 | ❌ |
| `~/.claude/projects/` | セッション履歴（パスベース）| ❌ |

---

## アプローチ比較

| 方法 | 難易度 | 安全性 | 向き不向き             |
|---|---|---|-------------------|
| **dotfiles Git repo + symlink** | 中 | ◎ | **メインのベストプラクティス** |
| Dropbox / iCloud + symlink | 低 | △ | 簡易に始めたい場合         |
| `claude-sync` CLI（OSS）| 低 | ○ | セッション履歴も同期したい場合   |
| chezmoi / stow | 中〜高 | ◎ | 既存dotfiles管理と統合したい場合 |

---

## 推奨: dotfiles Git repo + symlink　（本リポジトリ）

Gitリポジトリをコンフィグの単一ソースとして使い、インストールスクリプトで `~/.claude/` 配下にシンリンクを張る方法が実績あるプラクティスです。

```
~/dotclaude/
└── .claude/
    ├── settings.json      → symlink: ~/.claude/settings.json
    ├── CLAUDE.md          → symlink: ~/.claude/CLAUDE.md
    ├── agents/            → symlink: ~/.claude/agents/
    ├── skills/            → symlink: ~/.claude/skills/
    ├── hooks/            → symlink: ~/.claude/hooks/
    └── rules/             → symlink: ~/.claude/rules/
```

## 使い方

```zsh
cd dotclaude
./setup.sh
```
