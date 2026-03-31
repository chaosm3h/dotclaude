---
name: effective-go
description: golang.org/doc/effective_go からの Go のベストプラクティス、イディオム、規約を適用します。Go コードの記述、レビュー、リファクタリング時に使用し、慣用的でクリーンかつ効率的な実装を保証します。
source: https://github.com/openshift/hypershift/tree/main/.claude/skills/effective-go
---

# Effective Go

公式の [Effective Go ガイド](https://go.dev/doc/effective_go) のベストプラクティスと規約を適用して、クリーンで慣用的な Go コードを記述します。

## 適用場面

以下の場合にこのスキルを自動的に使用します：
- 新しい Go コードの記述
- Go コードのレビュー
- 既存の Go 実装のリファクタリング

## 重要な注意点

https://go.dev/doc/effective_go に記載されている規約とパターンに従い、特に以下に注意してください：

- **フォーマット**: 常に `gofmt` を使用してください - これは必須です。
- **命名**: アンダースコアは使用せず、エクスポートされる名前には MixedCaps を、エクスポートされない名前には mixedCaps を使用してください。
- **エラー処理**: 常にエラーをチェックしてください。パニックを起こさず、エラーを返してください。
- **並行性**: 通信によってメモリを共有してください（チャネルを使用）。
- **インターフェース**: 小さく保ちます（1〜3つのメソッドが理想的）。インターフェースを受け取り、具体的な型を返します。
- **ドキュメント**: エクスポートされるすべてのシンボルをドキュメント化し、シンボル名から始めてください。

## 参考文献

- 公式ガイド: https://go.dev/doc/effective_go
- コードレビューのコメント: https://github.com/golang/go/wiki/CodeReviewComments
- 標準ライブラリ: 慣用的なパターンのリファレンスとして使用してください
