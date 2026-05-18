---
name: test-coverage
description: テストカバレッジ分析と不足テスト自動生成。coverage/coverage-summary.jsonから80%閾値未満のファイルを特定し、Unit/Integration/E2Eテストを生成。「カバレッジ」「coverage」「不足テスト追加」をトリガとする。
---

# Test Coverage Skill

カバレッジ分析と不足箇所への自動テスト生成。

## When to Activate

- カバレッジが80%閾値を割った時
- 「カバレッジ上げて」「test coverage analysis」と指示された時
- PR前の品質ゲートチェック

## Workflow

1. **カバレッジ付きテスト実行**:
   ```bash
   npm test -- --coverage
   # または
   pnpm test --coverage
   ```

2. **レポート解析**: `coverage/coverage-summary.json` を読み、ファイル別カバレッジを取得。

3. **不足ファイル特定**: 80%閾値未満のファイルを列挙。

4. **各ファイルへのテスト生成**:
   - テストされていないコードパスを解析
   - **Unit Tests** - 関数レベル
   - **Integration Tests** - APIエンドポイント
   - **E2E Tests** - 重要フロー (連携: `e2e` skill)

5. **新テストの成功確認**: 実行 → green → 続行。

6. **メトリクス比較**:
   ```
   Before: X% (Y/Z lines)
   After:  X'% (Y'/Z lines)
   ```

7. **プロジェクト全体80%以上を確保**。

## Focus Areas

優先的にテストする:
- ハッピーパスシナリオ
- エラーハンドリング
- エッジケース (null / undefined / empty)
- 境界条件

## Coverage Targets

- **最低80%** 全体
- **100%必須**: 財務計算、認証、セキュリティ重要コード、コアビジネスロジック

## Related

- 実装フローは `tdd` skill
- 包括的検証は `verification-loop` skill
