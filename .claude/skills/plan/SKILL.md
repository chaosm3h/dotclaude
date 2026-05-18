---
name: plan
description: 要件再記述・リスク評価・段階的な実装計画作成。コードに触れる前にユーザー承認を待つ。`planner` agentを呼び出す。「実装計画」「plan this feature」「どう設計する?」をトリガとする。
---

# Plan Skill

このskillは `planner` agent を呼び出すラッパーです。

## When to Activate

- 新機能開始時
- 重要なアーキテクチャ変更
- 複雑なリファクタリング
- 複数ファイル/コンポーネント影響時
- 要件が曖昧な時

## How to Execute

1. **agent起動**: Task ツールで `planner` agent (`~/.claude/agents/planner.md`) を起動。
2. **agentに要求する成果物**:
   - Requirements Restatement (要件再記述)
   - Implementation Phases (フェーズ分割)
   - Dependencies
   - Risks (HIGH/MEDIUM/LOW)
   - Estimated Complexity (時間見積)
3. **明示的な確認待ち**: agentが計画を提示したら、ユーザーが "yes" / "proceed" / "modify: ..." と応答するまでコードを書かない。
4. **応答のハンドリング**:
   - `yes` / `proceed` → 後続skill (`tdd`, `code-review` 等) へ
   - `modify: <変更>` → 計画を修正して再提示
   - `different approach: <案>` → 代替計画を作成
   - `skip phase N` → 該当フェーズを除外

## Integration

- 計画後の実装は `tdd` skill 経由で `tdd-guide` agent へ
- ビルド失敗時は `build-fix` skill
- 完了レビューは `code-review` skill
- 連続ワークフローは `orchestrate` skill (`feature` モード)
