---
name: continuous-learning
description: Claude Codeセッションから再利用可能なパターンを自動的に抽出し、将来の使用のために学習済みスキルとして保存します。
---

# Continuous Learning Skill

Claude Codeセッションの終了時に自動的に評価し、学習済みスキルとして保存できる再利用可能なパターンを抽出します。

## How It Works

このスキルは各セッションの終了時に **Stop hook** として実行されます:

1. **セッション評価**: セッションに十分なメッセージがあるかチェック (デフォルト: 10以上)
2. **パターン検出**: セッションから抽出可能なパターンを識別
3. **スキル抽出**: 有用なパターンを `~/.claude/skills/learned/` に保存

## Configuration

`config.json` を編集してカスタマイズ:

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": "~/.claude/skills/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "workarounds",
    "debugging_techniques",
    "project_specific"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "external_api_issues"
  ]
}
```

## Pattern Types

| Pattern | Description |
|---------|-------------|
| `error_resolution` | 特定のエラーがどのように解決されたか |
| `user_corrections` | ユーザー修正からのパターン |
| `workarounds` | フレームワーク/ライブラリの癖への解決策 |
| `debugging_techniques` | 効果的なデバッグアプローチ |
| `project_specific` | プロジェクト固有の規約 |

## Hook Setup

`~/.claude/settings.json` に追加:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": ".claude/skills/continuous-learning/evaluate-session.sh"
      }]
    }]
  }
}
```

## Why Stop Hook?

- **軽量**: セッション終了時に一度だけ実行
- **ノンブロッキング**: すべてのメッセージにレイテンシを追加しない
- **完全なコンテキスト**: 完全なセッショントランスクリプトにアクセス可能

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - 継続学習のセクション
- `/learn` コマンド - セッション中の手動パターン抽出
