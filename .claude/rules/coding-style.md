# Coding Style

## Immutability (CRITICAL)

常に新しいオブジェクトを作成、決してミューテートしない:

```javascript
// WRONG: ミューテーション
function updateUser(user, name) {
  user.name = name  // MUTATION!
  return user
}

// CORRECT: イミュータビリティ
function updateUser(user, name) {
  return {
    ...user,
    name
  }
}
```

## File Organization

多数の小さいファイル > 少数の大きなファイル:
- 高凝集、低結合
- 標準200-400行、最大800行
- 大きなコンポーネントからユーティリティを抽出
- 型ではなく機能/ドメイン別に整理

## Error Handling

常にエラーを包括的に処理:

```typescript
try {
  const result = await riskyOperation()
  return result
} catch (error) {
  console.error('Operation failed:', error)
  throw new Error('Detailed user-friendly message')
}
```

## Input Validation

常にユーザー入力を検証:

```typescript
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

const validated = schema.parse(input)
```

## Code Quality Checklist

作業を完了とマークする前に:
- [ ] コードが読みやすく、適切に命名されている
- [ ] 関数が小さい（<50行）
- [ ] ファイルが集中している（<800行）
- [ ] 深いネストがない（>4レベル）
- [ ] 適切なエラー処理
- [ ] console.log文がない
- [ ] ハードコードされた値がない
- [ ] ミューテーションがない（イミュータブルパターンを使用）
