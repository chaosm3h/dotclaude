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
| `~/.claude/hooks/` | フック | ✅ |
| `~/.claude/statusline.py` | ステータスライン | ✅ |
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
    ├── hooks/             → symlink: ~/.claude/hooks/
    ├── rules/             → symlink: ~/.claude/rules/
    └── statusline.py      → symlink: ~/.claude/statusline.py
```

## 使い方

```zsh
cd dotclaude
./setup.sh
```

---

## 含まれるコンテンツ

### エージェント (`agents/`)

| エージェント | 目的 |
|---|---|
| `architect` | システム設計・アーキテクチャ決定 |
| `build-error-resolver` | ビルド・TypeScriptエラー解決 |
| `code-reviewer` | 品質・セキュリティのコードレビュー |
| `doc-updater` | ドキュメント更新 |
| `e2e-runner` | Playwright E2Eテスト |
| `planner` | 機能実装計画 |
| `refactor-cleaner` | デッドコードのクリーンアップ |
| `security-reviewer` | セキュリティ脆弱性分析 |
| `tdd-guide` | テスト駆動開発 |

### ルール (`rules/`)

| ルールファイル | 内容 |
|---|---|
| `agents.md` | エージェントオーケストレーション |
| `coding-style.md` | イミュータビリティ・ファイル構成・エラーハンドリング |
| `git-workflow.md` | コミット形式・PRワークフロー |
| `hooks.md` | フックの種類と設定 |
| `patterns.md` | APIレスポンス・リポジトリパターン |
| `performance.md` | モデル選択・コンテキスト管理 |
| `security.md` | セキュリティチェック・秘密情報管理 |
| `testing.md` | TDDワークフロー・80%カバレッジ要件 |

### スキル (`skills/`)

| スキル | 内容 | 種別 |
|---|---|---|
| `backend-patterns` | Node.js・Express・Next.js APIパターン | ガイド |
| `build-fix` | TypeScript/ビルドエラーを段階的修正 (`build-error-resolver` ラッパー) | Agent委任 |
| `checkpoint` | ワークフロー中のチェックポイント作成・検証・一覧 | ツール |
| `clickhouse-io` | ClickHouseクエリ最適化・分析 | ガイド |
| `code-review` | 品質+セキュリティの包括レビュー (`code-reviewer` ラッパー) | Agent委任 |
| `coding-standards` | TypeScript・JavaScript・React規約 | ガイド |
| `continuous-learning` | 継続的学習 (Stop hook による自動パターン抽出) | hook |
| `drawio` | draw.io図の作成 | ガイド |
| `e2e` | Playwrightでend-to-endテスト生成・実行 (`e2e-runner` ラッパー) | Agent委任 |
| `effective-go` | Goのベストプラクティス | ガイド |
| `eval` | eval駆動開発 (define/check/report/list/clean) | ツール |
| `eval-harness` | Eval駆動開発ハーネス | ツール |
| `frontend-patterns` | フロントエンドアーキテクチャパターン | ガイド |
| `grill-me` | コードレビュー練習 | ガイド |
| `improve-codebase-architecture` | アーキテクチャ改善分析 | ガイド |
| `learn` | セッション中の手動パターン抽出 → `~/.claude/skills/learned/` 保存 | ツール |
| `orchestrate` | feature/bugfix/refactor/security のマルチエージェントワークフロー | オーケストレーション |
| `plan` | 要件再記述・リスク評価・段階計画 (`planner` ラッパー) | Agent委任 |
| `prd-to-issues` | PRDからGitHubイシュー生成 | ツール |
| `project-guidelines-example` | プロジェクトガイドライン例 | ガイド |
| `refactor-clean` | テスト検証付きデッドコード安全削除 (`refactor-cleaner` ラッパー) | Agent委任 |
| `security-review` | セキュリティレビュー | ガイド |
| `setup-pm` | npm/pnpm/yarn/bun 優先パッケージマネージャー設定 | ツール |
| `slide-commit` | PDFビルド→ステージング→コミット一括実施 | ツール |
| `strategic-compact` | 戦略的コンパクト | ツール |
| `tdd` | テスト駆動開発（Red-Green-Refactor） | ガイド |
| `test-coverage` | カバレッジ分析と不足テスト自動生成 | ツール |
| `translate2ja` | マークダウンファイルの日本語翻訳 | ツール |
| `update-codemaps` | architecture/backend/frontend/data コードマップ自動生成 | ツール |
| `update-docs` | CONTRIB.md/RUNBOOK.md 同期生成 (`doc-updater` ラッパー) | Agent委任 |
| `verification-loop` | ビルド/型/Lint/テスト/秘密情報検証ループ | ツール |
| `verify` | コードベース状態の包括検証・PR準備可否判定 | ツール |
| `write-a-prd` | PRD作成・GitHubイシュー提出 | ツール |
