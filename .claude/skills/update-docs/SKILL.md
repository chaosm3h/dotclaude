---
name: update-docs
description: package.jsonとenv.exampleを信頼できる情報源としてdocs/CONTRIB.mdとdocs/RUNBOOK.mdを同期生成。古いドキュメント(90日以上)を検出。`doc-updater` agentを呼び出す。「ドキュメント更新」「README同期」「docs sync」をトリガとする。
---

# Update Docs Skill

このskillは `doc-updater` agent を呼び出すラッパーです。

## When to Activate

- スクリプト/環境変数を変更した後
- 新メンバー受け入れ前
- 「ドキュメント更新して」「README同期」と指示された時

## How to Execute

1. **agent起動**: Task ツールで `doc-updater` agent (`~/.claude/agents/doc-updater.md`) を起動。
2. **信頼できる情報源**:
   - `package.json` の scripts セクション
   - `.env.example`
3. **生成物**:
   - `docs/CONTRIB.md`:
     - 開発ワークフロー
     - 利用可能なスクリプト (説明テーブル)
     - 環境セットアップ (環境変数の目的とフォーマット)
     - テスト手順
   - `docs/RUNBOOK.md`:
     - デプロイ手順
     - モニタリング/アラート
     - 一般的な問題と修正
     - ロールバック手順
4. **古ドキュメント検出**: 90日以上変更されていない docs を一覧化、手動レビューに渡す。
5. **差分サマリ表示**。

## Constraint

**信頼できる唯一の情報源は package.json と .env.example**。 これらと矛盾する手書き記述は上書き対象。
