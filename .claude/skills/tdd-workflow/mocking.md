# When to Mock

**システムの境界**のみをモック化する：

- 外部API（決済、メールなど）
- データベース（場合によっては。テスト用DBを優先）
- 時刻／ランダム性
- ファイルシステム（場合によっては）

モック化しないもの：

- 自身のクラス／モジュール
- 内部の連携先
- 自身が制御できるもの

## モック化を考慮した設計

システムの境界では、モック化しやすいインターフェースを設計します：

**1. 依存性注入を利用する**

外部依存関係を内部で作成するのではなく、外部から渡すようにします：

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 汎用的なフェッチャーよりもSDKスタイルのインターフェースを優先する**

条件分岐を含む1つの汎用関数を作るのではなく、外部操作ごとに専用の関数を作成します：

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDKアプローチの特徴は以下の通りです：
- 各モックは特定の形状を1つ返す
- テストセットアップに条件分岐ロジックがない
- テストがどのエンドポイントを呼び出しているかが分かりやすい
- エンドポイントごとの型安全性