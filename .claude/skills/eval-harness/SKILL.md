# Eval Harness Skill

Claude Codeセッション用の正式な評価フレームワークで、eval駆動開発 (EDD) の原則を実装しています。

## Philosophy

Eval駆動開発はevalを「AI開発のユニットテスト」として扱います:
- 実装前に期待される動作を定義
- 開発中に継続的にevalを実行
- 各変更でリグレッションを追跡
- 信頼性測定にpass@kメトリクスを使用

## Eval Types

### Capability Evals
Claudeが以前はできなかったことができるかをテスト:
```markdown
[CAPABILITY EVAL: feature-name]
Task: Claudeが達成すべきことの説明
Success Criteria:
  - [ ] 基準 1
  - [ ] 基準 2
  - [ ] 基準 3
Expected Output: 期待される結果の説明
```

### Regression Evals
変更が既存の機能を壊さないことを確認:
```markdown
[REGRESSION EVAL: feature-name]
Baseline: SHAまたはチェックポイント名
Tests:
  - existing-test-1: PASS/FAIL
  - existing-test-2: PASS/FAIL
  - existing-test-3: PASS/FAIL
Result: X/Y passed (previously Y/Y)
```

## Grader Types

### 1. Code-Based Grader
コードを使用した決定論的チェック:
```bash
# ファイルに期待されるパターンが含まれているかチェック
grep -q "export function handleAuth" src/auth.ts && echo "PASS" || echo "FAIL"

# テストが合格するかチェック
npm test -- --testPathPattern="auth" && echo "PASS" || echo "FAIL"

# ビルドが成功するかチェック
npm run build && echo "PASS" || echo "FAIL"
```

### 2. Model-Based Grader
Claudeを使用してオープンエンドな出力を評価:
```markdown
[MODEL GRADER PROMPT]
以下のコード変更を評価してください:
1. 述べられた問題を解決していますか?
2. 適切に構造化されていますか?
3. エッジケースが処理されていますか?
4. エラーハンドリングは適切ですか?

Score: 1-5 (1=poor, 5=excellent)
Reasoning: [explanation]
```

### 3. Human Grader
手動レビューのためのフラグ:
```markdown
[HUMAN REVIEW REQUIRED]
Change: 何が変更されたかの説明
Reason: なぜ人間のレビューが必要か
Risk Level: LOW/MEDIUM/HIGH
```

## Metrics

### pass@k
「k回の試行で少なくとも1回成功」
- pass@1: 最初の試行での成功率
- pass@3: 3回の試行内での成功
- 典型的な目標: pass@3 > 90%

### pass^k
「k回の試行すべてが成功」
- 信頼性のためのより高い基準
- pass^3: 3回連続の成功
- クリティカルパスに使用

## Eval Workflow

### 1. Define (Before Coding)
```markdown
## EVAL DEFINITION: feature-xyz

### Capability Evals
1. 新しいユーザーアカウントを作成できる
2. メールフォーマットを検証できる
3. パスワードを安全にハッシュ化できる

### Regression Evals
1. 既存のログインが引き続き動作する
2. セッション管理が変更されていない
3. ログアウトフローが保持されている

### Success Metrics
- capability evalsでpass@3 > 90%
- regression evalsでpass^3 = 100%
```

### 2. Implement
定義されたevalに合格するコードを書く。

### 3. Evaluate
```bash
# capability evalsを実行
[各capability evalを実行し、PASS/FAILを記録]

# regression evalsを実行
npm test -- --testPathPattern="existing"

# レポートを生成
```

### 4. Report
```markdown
EVAL REPORT: feature-xyz
========================

Capability Evals:
  create-user:     PASS (pass@1)
  validate-email:  PASS (pass@2)
  hash-password:   PASS (pass@1)
  Overall:         3/3 passed

Regression Evals:
  login-flow:      PASS
  session-mgmt:    PASS
  logout-flow:     PASS
  Overall:         3/3 passed

Metrics:
  pass@1: 67% (2/3)
  pass@3: 100% (3/3)

Status: READY FOR REVIEW
```

## Integration Patterns

### Pre-Implementation
```
/eval define feature-name
```
`.claude/evals/feature-name.md` にeval定義ファイルを作成

### During Implementation
```
/eval check feature-name
```
現在のevalを実行してステータスをレポート

### Post-Implementation
```
/eval report feature-name
```
完全なevalレポートを生成

## Eval Storage

プロジェクト内にevalを保存:
```
.claude/
  evals/
    feature-xyz.md      # Eval定義
    feature-xyz.log     # Eval実行履歴
    baseline.json       # リグレッションベースライン
```

## Best Practices

1. **コーディング前にevalを定義** - 成功基準について明確に考えることを強制
2. **頻繁にevalを実行** - 早期にリグレッションをキャッチ
3. **pass@kを経時的に追跡** - 信頼性トレンドを監視
4. **可能な限りcode gradersを使用** - 決定論的 > 確率的
5. **セキュリティには人間のレビュー** - セキュリティチェックを完全に自動化しない
6. **evalを高速に保つ** - 遅いevalは実行されない
7. **コードと一緒にevalをバージョン管理** - Evalはファーストクラスの成果物

## Example: Adding Authentication

```markdown
## EVAL: add-authentication

### Phase 1: Define (10 min)
Capability Evals:
- [ ] ユーザーがメール/パスワードで登録できる
- [ ] ユーザーが有効な認証情報でログインできる
- [ ] 無効な認証情報が適切なエラーで拒否される
- [ ] セッションがページリロード後も保持される
- [ ] ログアウトでセッションがクリアされる

Regression Evals:
- [ ] パブリックルートが引き続きアクセス可能
- [ ] APIレスポンスが変更されていない
- [ ] データベーススキーマが互換性がある

### Phase 2: Implement (varies)
[コードを書く]

### Phase 3: Evaluate
実行: /eval check add-authentication

### Phase 4: Report
EVAL REPORT: add-authentication
==============================
Capability: 5/5 passed (pass@3: 100%)
Regression: 3/3 passed (pass^3: 100%)
Status: SHIP IT
```
