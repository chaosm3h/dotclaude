# Agent Orchestration

## Available Agents

`~/.claude/agents/`に配置:

| Agent | 目的 | 使用タイミング |
|-------|---------|-------------|
| planner | 実装計画 | 複雑な機能、リファクタリング |
| architect | システム設計 | アーキテクチャ決定 |
| tdd-guide | テスト駆動開発 | 新機能、バグ修正 |
| code-reviewer | コードレビュー | コード作成後 |
| security-reviewer | セキュリティ分析 | コミット前 |
| build-error-resolver | ビルドエラー修正 | ビルド失敗時 |
| e2e-runner | E2Eテスト | 重要なユーザーフロー |
| refactor-cleaner | デッドコードクリーンアップ | コード保守 |
| doc-updater | ドキュメント | ドキュメント更新 |

## Immediate Agent Usage

ユーザープロンプト不要:
1. 複雑な機能要求 - **planner**エージェントを使用
2. コードを書いた/修正した直後 - **code-reviewer**エージェントを使用
3. バグ修正または新機能 - **tdd-guide**エージェントを使用
4. アーキテクチャ決定 - **architect**エージェントを使用

## Parallel Task Execution

独立した操作には常に並列Task実行を使用:

```markdown
# GOOD: 並列実行
3つのエージェントを並列で起動:
1. Agent 1: auth.tsのセキュリティ分析
2. Agent 2: キャッシュシステムのパフォーマンスレビュー
3. Agent 3: utils.tsの型チェック

# BAD: 不要な逐次実行
最初にagent 1、次にagent 2、次にagent 3
```

## Multi-Perspective Analysis

複雑な問題には、ロール分割サブエージェントを使用:
- 事実レビューアー
- シニアエンジニア
- セキュリティ専門家
- 一貫性レビューアー
- 冗長性チェッカー
