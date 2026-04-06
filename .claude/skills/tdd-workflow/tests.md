# Good and Bad Tests

## Good Tests

**統合型**: 内部コンポーネントのモックではなく、実際のインターフェースを通じてテストを行う。

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特徴：

- ユーザーや呼び出し元が重視する動作をテストする
- 公開APIのみを使用する
- 内部のリファクタリングにも耐える
- 「何を」行うかを記述し、「どのように」行うかは記述しない
- 1つのテストにつき1つの論理的なアサーション

## Bad Tests

**実装詳細のテスト**：内部構造に依存している。

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

注意すべき点：

- 内部コラボレータのモック
- プライベートメソッドのテスト
- 呼び出し回数や順序に対するアサーション
- 動作に変更がないにもかかわらず、リファクタリングを行った際にテストが失敗する
- テスト名が「何を」ではなく「どのように」実行するかを記述している
- インターフェースではなく、外部の手段を通じて検証している

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```