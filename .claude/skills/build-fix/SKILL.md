---
name: build-fix
description: TypeScript/ビルドエラーを段階的に修正。一度に1エラーずつ、修正後に再ビルドして検証。`build-error-resolver` agentを呼び出す。「build fails」「TypeScript error」「ビルドエラー」をトリガとする。
---

# Build Fix Skill

このskillは `build-error-resolver` agent を呼び出すラッパーです。

## When to Activate

- ビルド失敗時
- TypeScript型エラー多発時
- `npm run build` / `pnpm build` がfailする時

## How to Execute

1. **agent起動**: Task ツールで `build-error-resolver` agent (`~/.claude/agents/build-error-resolver.md`) を起動。
2. **agentに要求する手順**:
   1. ビルド実行 (`npm run build` または `pnpm build`)
   2. エラー出力の解析 (ファイル別グループ化、深刻度ソート)
   3. 各エラーについて:
      - エラーコンテキスト表示 (前後5行)
      - 問題説明
      - 修正提案
      - 修正適用
      - 再ビルド
      - 解決確認
3. **停止条件 (必須)**:
   - 修正が新しいエラーを導入した時
   - 3回試行で同じエラーが続く時
   - ユーザーが一時停止を要求した時
4. **完了サマリ**: 修正されたエラー / 残存エラー / 新規導入エラー を表示。

## Safety

**一度に1エラーずつ** 修正する。一括修正は副作用追跡不能になるため禁止。
