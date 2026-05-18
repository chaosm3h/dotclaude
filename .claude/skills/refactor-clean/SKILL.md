---
name: refactor-clean
description: デッドコードをテスト検証付きで安全に特定・削除。knip/depcheck/ts-pruneで分析し、SAFE/CAUTION/DANGER分類で段階削除。`refactor-cleaner` agentを呼び出す。「デッドコード」「未使用コード削除」「refactor cleanup」をトリガとする。
---

# Refactor Clean Skill

このskillは `refactor-cleaner` agent を呼び出すラッパーです。

## When to Activate

- 定期メンテナンス
- リファクタリング前の整理
- 「未使用コードを削除して」と指示された時

## How to Execute

1. **agent起動**: Task ツールで `refactor-cleaner` agent (`~/.claude/agents/refactor-cleaner.md`) を起動。
2. **agentに要求する手順**:
   1. デッドコード分析ツール実行:
      - `knip` - 未使用エクスポート/ファイル
      - `depcheck` - 未使用依存
      - `ts-prune` - 未使用TS エクスポート
   2. `.reports/dead-code-analysis.md` に包括レポート生成
   3. 発見を深刻度別に分類:
      - **SAFE**: テストファイル、未使用ユーティリティ
      - **CAUTION**: APIルート、コンポーネント
      - **DANGER**: 設定ファイル、メインエントリポイント
   4. **SAFE のみ** 削除を提案
   5. 各削除前に:
      - テストスイート実行
      - テスト成功確認
      - 変更適用
      - テスト再実行
      - **失敗時はロールバック**
3. **完了サマリ**: クリーンアップ済みアイテムを表示。

## Safety

**まずテストを実行せずにコードを削除しない**。 ロールバック手順を必ず確保する。
