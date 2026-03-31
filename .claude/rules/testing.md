# Testing Requirements

## Minimum Test Coverage: 80%

テストタイプ（全て必須）:
1. **Unit Tests** - 個別の関数、ユーティリティ、コンポーネント
2. **Integration Tests** - APIエンドポイント、データベース操作
3. **E2E Tests** - 重要なユーザーフロー（Playwright）

## Test-Driven Development

必須のワークフロー:
1. テストを最初に書く（RED）
2. テストを実行 - 失敗するはず
3. 最小限の実装を書く（GREEN）
4. テストを実行 - 成功するはず
5. リファクタリング（IMPROVE）
6. カバレッジを確認（80%以上）

## Troubleshooting Test Failures

1. **tdd-guide**エージェントを使用
2. テストの独立性をチェック
3. モックが正しいことを確認
4. テストではなく実装を修正（テストが間違っている場合を除く）

## Agent Support

- **tdd-guide** - 新機能に積極的に使用、テストファーストを強制
- **e2e-runner** - Playwright E2Eテスト専門家
