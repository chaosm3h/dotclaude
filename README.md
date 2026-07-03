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

エージェント・ルール・スキルは互いに依存するため(例: `tdd-guide`↔`tdd`、`planner`↔`plan`、`code-reviewer`↔`code-review`)、種別ではなく**関係するコンテキスト単位**でまとめています。`モジュール` 列がその項目の種別(エージェント / スキル / ルール)を示します。

### 計画・アーキテクチャ設計

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| エージェント | `planner` | 機能実装計画 | ECC |
| スキル | `plan` | 要件再記述・リスク評価・段階計画 (`planner` ラッパー) | ECC |
| エージェント | `architect` | システム設計・アーキテクチャ決定 | ECC |
| スキル | `improve-codebase-architecture` | アーキテクチャ改善分析・浅いモジュールの深化 | 独自 |
| スキル | `grilling` | 計画・設計をユーザーに徹底質問しストレステスト | mattpocock |
| スキル | `orchestrate` | feature/bugfix/refactor/security のマルチエージェントワークフロー | 独自 |

### コードレビュー・品質

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| エージェント | `code-reviewer` | 品質・セキュリティのコードレビュー | ECC |
| スキル | `code-review` | 品質+セキュリティの包括レビュー (`code-reviewer` ラッパー) | ECC |
| スキル | `ai-slop-review` | AI生成特有の低品質コード(スロップ)検出と根拠付き辛口ダメ出しレビュー | 独自 |
| スキル | `coding-standards` | TypeScript・JavaScript・React・Node.js のユニバーサルなコーディング規約 | ECC |
| ルール | `coding-style.md` | イミュータビリティ・ファイル構成・エラーハンドリング | ECC |
| ルール | `patterns.md` | APIレスポンス・リポジトリパターン | ECC |

### セキュリティ

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| エージェント | `security-reviewer` | セキュリティ脆弱性分析 | ECC |
| スキル | `security-review` | 認証・入力処理・APIエンドポイント等のセキュリティチェックリストとパターン | ECC |
| ルール | `security.md` | セキュリティチェック・秘密情報管理 | ECC |

### テスト・検証

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| エージェント | `tdd-guide` | テスト駆動開発 | ECC |
| スキル | `tdd` | テスト駆動開発（Red-Green-Refactor） | 独自 |
| ルール | `testing.md` | TDDワークフロー・80%カバレッジ要件 | ECC |
| エージェント | `e2e-runner` | Playwright E2Eテスト | ECC |
| スキル | `e2e` | Playwrightでend-to-endテスト生成・実行 (`e2e-runner` ラッパー) | ECC |
| スキル | `test-coverage` | カバレッジ分析と不足テスト自動生成 | 独自 |
| スキル | `eval` | eval駆動開発 (define/check/report/list/clean) | 独自 |
| スキル | `eval-harness` | Eval駆動開発(EDD)ハーネス。pass@k/pass^kで信頼性測定 | ECC |
| スキル | `verify` | コードベース状態の包括検証・PR準備可否判定 | 独自 |
| スキル | `verification-loop` | ビルド/型/Lint/テスト/秘密情報/console.log/Git diff を順次検証 | ECC |

### ビルド・型エラー

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| エージェント | `build-error-resolver` | ビルド・TypeScriptエラー解決 | ECC |
| スキル | `build-fix` | TypeScript/ビルドエラーを段階的修正 (`build-error-resolver` ラッパー) | ECC |

### リファクタリング

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| エージェント | `refactor-cleaner` | デッドコードのクリーンアップ | ECC |
| スキル | `refactor-clean` | テスト検証付きデッドコード安全削除 (`refactor-cleaner` ラッパー) | ECC |

### ドキュメント

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| エージェント | `doc-updater` | ドキュメント更新 | ECC |
| スキル | `update-docs` | CONTRIB.md/RUNBOOK.md 同期生成 (`doc-updater` ラッパー) | ECC |
| スキル | `update-codemaps` | architecture/backend/frontend/data コードマップ自動生成 | 独自 |
| スキル | `japanese-tech-writing` | 日本語の技術文書・書籍原稿の文章規範 | 独自 |
| スキル | `translate2ja` | マークダウンファイルの日本語翻訳 | 独自 |

### PRD・イシュー管理

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| スキル | `to-prd` | 会話内容をPRD化しイシュートラッカーへ公開(ヒアリングなし) | mattpocock |
| スキル | `to-issues` | 計画・仕様・PRDをトレーサーバレット垂直スライスでイシュー分割 | mattpocock |

### 言語・ツール別ガイド

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| スキル | `backend-patterns` | Node.js・Express・Next.js APIのバックエンドアーキテクチャパターン | ECC |
| スキル | `frontend-patterns` | React・Next.js・状態管理・パフォーマンスのフロントエンドパターン | ECC |
| スキル | `effective-go` | Goのベストプラクティス | 独自 |
| スキル | `goland-clean` | GoLandインスペクションアラートゼロのGoコード実装・自動検証 | 独自 |
| スキル | `clickhouse-io` | ClickHouseクエリ最適化・分析 | 独自 |
| スキル | `drawio` | draw.io図の作成 | 独自 |

### ワークフロー・環境設定

| モジュール | 名前 | 内容 | 由来 |
|---|---|---|---|
| ルール | `agents.md` | エージェントオーケストレーション | ECC |
| ルール | `git-workflow.md` | コミット形式・PRワークフロー | ECC |
| ルール | `hooks.md` | フックの種類と設定 | ECC |
| ルール | `performance.md` | モデル選択・コンテキスト管理 | ECC |
| スキル | `setup-pm` | npm/pnpm/yarn/bun 優先パッケージマネージャー設定 | 独自 |
| スキル | `slide-commit` | PDFビルド→ステージング→コミット一括実施 | 独自 |
| スキル | `checkpoint` | ワークフロー中のチェックポイント作成・検証・一覧 | 独自 |
| スキル | `continuous-learning` | セッションから再利用パターンを自動抽出し学習済みスキルとして保存 (Stop hook) | ECC |
| スキル | `strategic-compact` | 論理的境界での手動コンパクション提案 | ECC |
| スキル | `learn` | セッション中の手動パターン抽出 → `~/.claude/skills/learned/` 保存 | 独自 |
| スキル | `handoff` | 現在の会話を別エージェント向け引き継ぎドキュメントにまとめる | mattpocock |
| スキル | `teach` | ワークスペース内でユーザーに新しいスキル・概念を教える | mattpocock |
| スキル | `project-guidelines-example` | プロジェクトガイドライン例 | 独自 |

> **由来について**: `ECC` は [affaan-m/ECC](https://github.com/affaan-m/ECC) 由来、`mattpocock` は [mattpocock/skills](https://github.com/mattpocock/skills) 由来、`独自` はそれ以外(自作・他ソース)を指します。
> `モジュール` が `スキル` で `内容` に「(`○○` ラッパー)」とあるもの(`build-fix`, `code-review`, `e2e`, `plan`, `refactor-clean`, `update-docs`)は、スキルファイル自体はECCに存在しませんが、呼び出し先エージェントがすべてECC由来のため `ECC` に分類しています。
> エージェントとルールは現状すべてECC由来です。
