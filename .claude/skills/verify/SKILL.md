---
name: verify
description: コードベース状態の包括的な検証を実行。ビルド/型/Lint/テスト/カバレッジ/秘密情報/console.log/Git diffを順次チェックし、PR準備可否を判定。quick/full/pre-commit/pre-prモードあり。「verify」「検証して」「PR前チェック」「pre-commit check」をトリガとする。
---

# Verify Skill

`verification-loop` skillの検証ワークフローを実行する。

## When to Activate

- 機能または重要なコード変更の完了後
- PRを作成する前
- リファクタリング後
- 品質ゲートの通過を確認したい時

## Modes

引数で指定 (省略時は `full`):

- `quick` - ビルド + 型チェックのみ (高速)
- `full` - 全てのチェック (デフォルト)
- `pre-commit` - 型/Lint/秘密情報チェック
- `pre-pr` - 完全なチェック + セキュリティスキャン

## Verification Phases

### Phase 1: Build

```bash
npm run build 2>&1 | tail -20
# または
pnpm build 2>&1 | tail -20
```

ビルドが失敗した場合は停止して修正する。

### Phase 2: Type Check

```bash
npx tsc --noEmit 2>&1 | head -30
```

### Phase 3: Lint

```bash
npm run lint 2>&1 | head -30
```

### Phase 4: Test Suite

```bash
npm run test -- --coverage 2>&1 | tail -50
```

目標: 最低80%カバレッジ。

### Phase 5: Security Scan

```bash
grep -rn "sk-\|api_key\|password" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### Phase 6: Diff Review

```bash
git diff --stat
git diff HEAD~1 --name-only
```

## Output Format

```
VERIFICATION: [PASS/FAIL]

Build:    [OK/FAIL]
Types:    [OK/X errors]
Lint:     [OK/X issues]
Tests:    [X/Y passed, Z% coverage]
Secrets:  [OK/X found]
Logs:     [OK/X console.logs]

Ready for PR: [YES/NO]
```

重要な問題がある場合は修正提案と該当ファイル:行を添える。

## Related

- ビルドエラー修正は `build-fix` skill
- テストカバレッジ改善は `test-coverage` skill
- セキュリティ専門レビューは `security-review` skill
