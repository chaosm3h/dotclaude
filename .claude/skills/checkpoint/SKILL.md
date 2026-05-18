---
name: checkpoint
description: ワークフロー中のチェックポイントを作成・検証・一覧。git stash/commitと.claude/checkpoints.logに記録し、ファイル変更・テスト成功率・カバレッジ差分を比較。「チェックポイント」「checkpoint」「進捗スナップショット」をトリガとする。
---

# Checkpoint Skill

複雑なワークフロー中に状態を保存・比較できるチェックポイント機構。

## When to Activate

- 機能実装の節目で状態を残したい時
- リファクタリング前のロールバック地点を確保したい時
- 「ここまでの進捗を残して」と指示された時

## Sub-command Usage

### `create <name>`

1. `verification-loop` skill を `quick` モードで実行し、現状がクリーンであることを確認
2. git stash または commit を作成
3. `.claude/checkpoints.log` に記録:
   ```bash
   echo "$(date +%Y-%m-%d-%H:%M) | $CHECKPOINT_NAME | $(git rev-parse --short HEAD)" >> .claude/checkpoints.log
   ```
4. チェックポイント作成を報告

### `verify <name>`

1. `.claude/checkpoints.log` から該当チェックポイントを読む
2. 現在状態と比較:
   - 追加/変更ファイル
   - テスト成功率
   - カバレッジ
3. 報告:
   ```
   CHECKPOINT COMPARISON: <name>
   ============================
   Files changed: X
   Tests: +Y passed / -Z failed
   Coverage: +X% / -Y%
   Build: [PASS/FAIL]
   ```

### `list`

全チェックポイントを表示:
- 名前
- タイムスタンプ
- Git SHA
- ステータス (current/behind/ahead)

### `clear`

古いチェックポイントを削除 (最新5件保持)。

## Typical Workflow

```
[Start]    → checkpoint create "feature-start"
[Implement]→ checkpoint create "core-done"
[Test]     → checkpoint verify "core-done"
[Refactor] → checkpoint create "refactor-done"
[PR]       → checkpoint verify "feature-start"
```
