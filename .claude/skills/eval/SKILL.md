---
name: eval
description: eval駆動開発ワークフローを管理。define/check/report/listサブコマンドで.claude/evals/に評価定義を作成・実行・レポート生成。「eval define」「evalsを実行」「evalチェック」「機能の評価」をトリガとする。
---

# Eval Skill

eval駆動開発ワークフローを管理する。機能ごとにCapability/Regressionの評価定義を作成し、実行・レポート化する。

## Sub-command Usage

### `define <feature-name>`

新しいeval定義を作成する:

1. `.claude/evals/<feature-name>.md` をテンプレートで作成:

```markdown
## EVAL: <feature-name>
Created: <date>

### Capability Evals
- [ ] [機能1の説明]
- [ ] [機能2の説明]

### Regression Evals
- [ ] [既存の動作1がまだ機能する]
- [ ] [既存の動作2がまだ機能する]

### Success Criteria
- capability evalsのpass@3 > 90%
- regression evalsのpass^3 = 100%
```

2. ユーザーに具体的な基準を入力するよう促す。

### `check <feature-name>`

機能のevalsを実行する:

1. `.claude/evals/<feature-name>.md` からeval定義を読む
2. 各capability evalについて:
   - 基準を検証
   - PASS/FAILを記録
   - `.claude/evals/<feature-name>.log` に試行をログ
3. 各regression evalについて:
   - 関連テストを実行
   - ベースラインと比較
   - PASS/FAILを記録
4. 現在の状態を報告:

```
EVAL CHECK: <feature-name>
========================
Capability: X/Y passing
Regression: X/Y passing
Status: IN PROGRESS / READY
```

### `report <feature-name>`

包括的なevalレポートを生成する:

```
EVAL REPORT: <feature-name>
=========================
Generated: <date>

CAPABILITY EVALS
----------------
[eval-1]: PASS (pass@1)
[eval-2]: PASS (pass@2) - リトライが必要
[eval-3]: FAIL - ノートを参照

REGRESSION EVALS
----------------
[test-1]: PASS
[test-2]: PASS
[test-3]: PASS

METRICS
-------
Capability pass@1: 67%
Capability pass@3: 100%
Regression pass^3: 100%

NOTES
-----
[問題、エッジケース、または観察事項]

RECOMMENDATION
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

### `list`

全てのeval定義を表示する:

```
EVAL DEFINITIONS
================
feature-auth      [3/5 passing] IN PROGRESS
feature-search    [5/5 passing] READY
feature-export    [0/4 passing] NOT STARTED
```

### `clean`

古いevalログを削除する（最新10件を保持）。

## Typical Workflow

```
[Feature Start] → eval define <name>
[Implement]     → eval check <name>
[Iterate]       → eval check <name>
[Ready]         → eval report <name>
```

## Related

- 実装フローは `tdd` skill
- PR前の検証は `verify` skill
