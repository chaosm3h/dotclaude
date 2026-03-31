# Security Guidelines

## Mandatory Security Checks

全てのコミット前に:
- [ ] ハードコードされた秘密情報がないこと（APIキー、パスワード、トークン）
- [ ] 全てのユーザー入力がバリデーション済み
- [ ] SQLインジェクション防止（パラメータ化クエリ）
- [ ] XSS防止（サニタイズされたHTML）
- [ ] CSRF保護が有効
- [ ] 認証/認可が検証済み
- [ ] 全てのエンドポイントにレート制限
- [ ] エラーメッセージが機密データを漏洩しない

## Secret Management

```typescript
// NEVER: ハードコードされた秘密情報
const apiKey = "sk-proj-xxxxx"

// ALWAYS: 環境変数
const apiKey = process.env.OPENAI_API_KEY

if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

## Security Response Protocol

セキュリティ問題が見つかった場合:
1. 即座に停止
2. **security-reviewer**エージェントを使用
3. 続行前にCRITICAL問題を修正
4. 露出した秘密情報をローテーション
5. 類似の問題がないかコードベース全体をレビュー
