# Verification Loop Skill

Claude Codeセッション用の包括的な検証システム。

## When to Use

このスキルを呼び出すタイミング:
- 機能または重要なコード変更の完了後
- PRを作成する前
- 品質ゲートの通過を確認したい場合
- リファクタリング後

## Verification Phases

### Phase 1: Build Verification
```bash
# プロジェクトがビルドできるかチェック
npm run build 2>&1 | tail -20
# または
pnpm build 2>&1 | tail -20
```

ビルドが失敗した場合、継続する前に停止して修正してください。

### Phase 2: Type Check
```bash
# TypeScriptプロジェクト
npx tsc --noEmit 2>&1 | head -30

# Pythonプロジェクト
pyright . 2>&1 | head -30
```

すべての型エラーを報告。継続する前に重要なものを修正してください。

### Phase 3: Lint Check
```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
```

### Phase 4: Test Suite
```bash
# カバレッジ付きでテストを実行
npm run test -- --coverage 2>&1 | tail -50

# カバレッジ閾値をチェック
# 目標: 最低80%
```

報告内容:
- 総テスト数: X
- 合格: X
- 失敗: X
- カバレッジ: X%

### Phase 5: Security Scan
```bash
# 秘密情報をチェック
grep -rn "sk-" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
grep -rn "api_key" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# console.logをチェック
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### Phase 6: Diff Review
```bash
# 何が変更されたかを表示
git diff --stat
git diff HEAD~1 --name-only
```

変更された各ファイルを以下の点でレビュー:
- 意図しない変更
- 欠落しているエラーハンドリング
- 潜在的なエッジケース

## Output Format

すべてのフェーズ実行後、検証レポートを作成:

```
VERIFICATION REPORT
==================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## Continuous Mode

長いセッションの場合、15分ごとまたは大きな変更後に検証を実行:

```markdown
メンタルチェックポイントを設定:
- 各関数を完了した後
- コンポーネントを完成させた後
- 次のタスクに移る前

実行: /verify
```

## Integration with Hooks

このスキルは PostToolUse hooks を補完しますが、より深い検証を提供します。
Hooksは問題を即座にキャッチし、このスキルは包括的なレビューを提供します。
