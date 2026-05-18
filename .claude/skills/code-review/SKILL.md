---
name: code-review
description: コミットされていない変更に対する品質+セキュリティの包括的レビュー。`code-reviewer` agentを呼び出してCRITICAL/HIGH/MEDIUM/LOWで分類しPR可否を判定。「review this before I merge」「is this code safe?」「コードレビュー」をトリガとする。
---

# Code Review Skill

このskillは `code-reviewer` agent を呼び出すラッパーです。手順や規約はagent定義側に集約し、skillはエントリポイントとして機能します。

## When to Activate

- コミット前/PR作成前
- 「コードレビューして」「review my changes」と指示された時
- セキュリティ/品質チェックを求められた時

## How to Execute

1. **対象を特定**: 既定では `git diff --name-only HEAD` で取得した未コミット変更。ユーザーが特定ファイルや PR を指定した場合はそれに従う。
2. **agent起動**: Task ツールで `code-reviewer` agent を起動 (`~/.claude/agents/code-reviewer.md`)。プロンプトには対象範囲と背景を含める。
3. **結果集約**: agent の返答を以下で整理して提示する:
   - CRITICAL: セキュリティ脆弱性 (ハードコード資格情報、SQLi、XSS、入力検証欠如、パストラバーサル)
   - HIGH: 品質問題 (>50行関数、>800行ファイル、>4階層ネスト、エラーハンドリング欠如、console.log)
   - MEDIUM: ベストプラクティス違反 (ミューテーション、絵文字、テスト不足、a11y)
   - LOW: マイナーな改善提案
4. **判定**: CRITICAL/HIGH があれば PR を **ブロック**。修正提案と該当ファイル:行を必ず添える。

## Related

- セキュリティ専門レビューは `security-review` skill / `security-reviewer` agent
- 並列レビューは `orchestrate` skill (`security` ワークフロー) を参照
