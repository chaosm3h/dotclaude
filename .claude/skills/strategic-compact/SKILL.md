---
name: strategic-compact
description: 任意の自動コンパクションではなく、タスクフェーズ間でコンテキストを保持するために論理的な間隔で手動コンテキストコンパクションを提案します。
---

# Strategic Compact Skill

任意の自動コンパクションに頼るのではなく、ワークフローの戦略的なポイントで手動 `/compact` を提案します。

## Why Strategic Compaction?

自動コンパクションは任意のポイントでトリガーされます:
- タスクの途中で発動することが多く、重要なコンテキストが失われる
- 論理的なタスク境界を認識しない
- 複雑な複数ステップの操作を中断する可能性がある

論理的な境界での戦略的コンパクション:
- **探索後、実行前** - リサーチコンテキストをコンパクトし、実装計画を保持
- **マイルストーン完了後** - 次のフェーズのための新しいスタート
- **大きなコンテキストシフト前** - 異なるタスクの前に探索コンテキストをクリア

## How It Works

`suggest-compact.sh` スクリプトは PreToolUse (Edit/Write) で実行され:

1. **ツール呼び出しの追跡** - セッション内のツール呼び出しをカウント
2. **閾値検出** - 設定可能な閾値で提案 (デフォルト: 50回の呼び出し)
3. **定期的なリマインダー** - 閾値後25回の呼び出しごとにリマインド

## Hook Setup

`~/.claude/settings.json` に追加:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "tool == \"Edit\" || tool == \"Write\"",
      "hooks": [{
        "type": "command",
        "command": ".claude/skills/strategic-compact/suggest-compact.sh"
      }]
    }]
  }
}
```

## Configuration

環境変数:
- `COMPACT_THRESHOLD` - 最初の提案前のツール呼び出し数 (デフォルト: 50)

## Best Practices

1. **計画後にコンパクト** - 計画が確定したら、コンパクトして新しくスタート
2. **デバッグ後にコンパクト** - 継続する前にエラー解決コンテキストをクリア
3. **実装中はコンパクトしない** - 関連する変更のためにコンテキストを保持
4. **提案を読む** - hookは*いつ*を伝え、あなたが*するかどうか*を決定

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Token最適化セクション
- Memory persistence hooks - コンパクション後も残る状態のため
