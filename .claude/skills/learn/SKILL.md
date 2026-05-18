---
name: learn
description: セッション中の非自明な問題解決から再利用可能なパターンを手動抽出し、~/.claude/skills/learned/に保存。「/learn」「学んだことを保存」「パターンを抽出して」「セッションから学習」をトリガとする。
---

# Learn Skill

現在のセッションを分析し、スキルとして保存する価値のあるパターンを手動抽出する。

## When to Activate

- 非自明な問題を解決した直後
- 再利用価値のあるパターン・回避策を発見した時
- ユーザーが「`/learn`」「学んだことを保存」と指示した時

## What to Extract

以下を探す:

| パターン種別 | 内容 |
|---|---|
| Error Resolution | エラー → 根本原因 → 修正 → 再利用可能性 |
| Debugging Techniques | 効果があったツールの組み合わせ、診断パターン |
| Workarounds | ライブラリの癖、API制限、バージョン固有の修正 |
| Project-Specific | コードベース慣習、アーキテクチャ決定、統合パターン |

**抽出しないもの**:
- 些細な修正 (タイプミス、単純な構文エラー)
- 一回限りの問題 (特定のAPI障害等)
- 将来の時間節約に寄与しないもの

## Output Format

`~/.claude/skills/learned/<pattern-name>.md` にスキルファイルを作成:

```markdown
# <説明的なパターン名>

**Extracted:** <日付>
**Context:** <これが適用される場合の簡単な説明>

## Problem
<これが解決する問題 - 具体的に>

## Solution
<パターン/テクニック/回避策>

## Example
<該当する場合はコード例>

## When to Use
<トリガー条件 - このスキルを有効化すべき状況>
```

## Process

1. セッションから抽出可能なパターンをレビュー
2. 最も価値があり再利用可能な洞察を特定
3. スキルファイルを下書き
4. **保存前にユーザーに確認を求める**
5. `~/.claude/skills/learned/` に保存

スキルは集中させる - スキル毎に1つのパターンのみ。

## Related

- 自動Stop hookによるセッション末尾の自動抽出は `continuous-learning` skill
