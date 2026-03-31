# Git Workflow

## Commit Message Format

```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, perf, ci

Description: 日本語で記載。

Optional Body: 日本語で記載し、一文程度の箇条書き最大５点以内で重要なものを優先とする。

Note: Attribution disabled globally via ~/.claude/settings.json.

## Pull Request Workflow

PRを作成する際:
1. 完全なコミット履歴を分析（最新のコミットだけでなく）
2. `git diff [base-branch]...HEAD`を使用して全ての変更を確認
3. 包括的なPR概要を下書き
4. TODOを含むテストプランを含める
5. 新しいブランチの場合は`-u`フラグでプッシュ

## Feature Implementation Workflow

1. **Plan First**
   - **planner**エージェントを使用して実装計画を作成
   - 依存関係とリスクを特定
   - フェーズに分割

2. **TDD Approach**
   - **tdd-guide**エージェントを使用
   - テストを最初に書く（RED）
   - テストに合格する実装（GREEN）
   - リファクタリング（IMPROVE）
   - 80%以上のカバレッジを確認

3. **Code Review**
   - コードを書いた直後に**code-reviewer**エージェントを使用
   - CRITICALとHIGH問題に対処
   - 可能な場合はMEDIUM問題を修正

4. **Commit & Push**
   - 詳細なコミットメッセージ
   - conventional commitsフォーマットに従う
