# Hooks System

## Hook Types

- **PreToolUse**: ツール実行前（検証、パラメータ修正）
- **PostToolUse**: ツール実行後（自動フォーマット、チェック）
- **Stop**: セッション終了時（最終検証）

## Current Hooks (in ~/.claude/settings.json)

### PreToolUse
- **tmux reminder**: 長時間実行コマンド（npm、pnpm、yarn、cargo等）にtmuxを提案
- **git push review**: プッシュ前にZedでレビューを開く
- **doc blocker**: 不要な.md/.txtファイルの作成をブロック

### PostToolUse
- **PR creation**: PR URLとGitHub Actionsステータスをログ
- **Prettier**: 編集後にJS/TSファイルを自動フォーマット
- **TypeScript check**: .ts/.tsxファイル編集後にtscを実行
- **console.log warning**: 編集されたファイル内のconsole.logについて警告

### Stop
- **console.log audit**: セッション終了前に変更された全てのファイルでconsole.logをチェック

## Auto-Accept Permissions

注意して使用:
- 信頼できる、明確に定義された計画に対して有効化
- 探索的な作業には無効化
- dangerously-skip-permissionsフラグは決して使用しない
- 代わりに`~/.claude.json`で`allowedTools`を設定

## TodoWrite Best Practices

TodoWriteツールを使用して:
- マルチステップタスクの進捗を追跡
- 指示の理解を確認
- リアルタイムでの舵取りを可能に
- 詳細な実装ステップを表示

Todoリストが明らかにすること:
- 順序が間違っているステップ
- 欠けているアイテム
- 余分な不要なアイテム
- 粒度の誤り
- 誤解された要件
