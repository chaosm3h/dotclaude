---
name: update-codemaps
description: コードベース構造を解析してトークン効率の良いコードマップ(architecture/backend/frontend/data)を生成・更新。前バージョンとの差分を計算し30%超で承認要求。「コードマップ」「codemap」「アーキテクチャドキュメント自動生成」をトリガとする。
---

# Update Codemaps Skill

コードベース全体の構造をトークン効率良くドキュメント化する。

## When to Activate

- 大規模リファクタリング後
- 新メンバーオンボーディング前
- アーキテクチャドキュメントの陳腐化が疑われる時
- 「コードマップ更新」と指示された時

## Workflow

1. **全ソースファイルをスキャン**: インポート/エクスポート/依存関係を抽出。

2. **コードマップ生成** (トークン効率重視、実装詳細ではなく高レベル構造):
   - `codemaps/architecture.md` - 全体アーキテクチャ
   - `codemaps/backend.md` - バックエンド構造
   - `codemaps/frontend.md` - フロントエンド構造
   - `codemaps/data.md` - データモデル/スキーマ

3. **差分計算**: 前バージョンとのパーセンテージ差分を算出。

4. **承認ゲート**: 変更が **30%超** の場合は更新前にユーザー承認を要求。

5. **タイムスタンプ付与**: 各マップに最新性タイムスタンプ。

6. **レポート保存**: `.reports/codemap-diff.txt`

## Implementation Hints

- TypeScript / Node.js 解析が前提
- 実装の詳細ではなく **高レベル構造** に焦点
- import graph / module dependency graph 視点

## Related

- 大規模変更前は `architect` agent
- 文書同期は `update-docs` skill
