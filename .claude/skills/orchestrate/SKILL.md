---
name: orchestrate
description: 複雑タスクの連続エージェントワークフロー。feature/bugfix/refactor/securityのワークフロー型でplanner→tdd-guide→code-reviewer等を直列/並列実行し、HANDOFFドキュメントで引き継ぎ。「マルチエージェント」「workflow」「フィーチャー実装一気通貫」をトリガとする。
---

# Orchestrate Skill

複数agentを連続/並列実行する高位ワークフロー。各agentの出力をHANDOFFドキュメントとして次に渡す。

## Workflow Types

| Type | チェーン |
|---|---|
| `feature` | planner → tdd-guide → code-reviewer → security-reviewer |
| `bugfix` | (explore) → tdd-guide → code-reviewer |
| `refactor` | architect → code-reviewer → tdd-guide |
| `security` | security-reviewer → code-reviewer → architect |
| `custom <agents>` | カンマ区切りで任意シーケンス |

## Execution Pattern

各agentについて:

1. **agent起動** - 前agentからのHANDOFFコンテキスト付き
2. **出力収集** - 構造化HANDOFFとして
3. **次agentへ渡す**
4. **集約** - 最終レポート

### HANDOFF Document Format

```markdown
## HANDOFF: <previous> -> <next>

### Context
<実施した内容のサマリ>

### Findings
<主要な発見/決定>

### Files Modified
<変更ファイル一覧>

### Open Questions
<次agentへの未解決事項>

### Recommendations
<推奨次ステップ>
```

## Parallel Phase

独立チェックは並列実行 (Task ツールで同一メッセージ内に複数起動):

```
並列:
- code-reviewer (品質)
- security-reviewer (セキュリティ)
- architect (設計)

結果マージ → 単一レポート
```

## Final Report Format

```
ORCHESTRATION REPORT
====================
Workflow: <type>
Task: <description>
Agents: <chain>

SUMMARY
-------
<1段落要約>

AGENT OUTPUTS
-------------
<各agent要約>

FILES CHANGED
-------------
<全変更ファイル>

TEST RESULTS
------------
<合格/不合格サマリ>

SECURITY STATUS
---------------
<セキュリティ調査結果>

RECOMMENDATION
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

## Tips

1. `planner` から始める (複雑フィーチャー)
2. `code-reviewer` をマージ前に必ず含める
3. 認証/決済/個人情報は `security-reviewer` を必須
4. HANDOFF は次agentが必要なものに絞る
5. agent間で必要なら `verification-loop` skill を挟む
