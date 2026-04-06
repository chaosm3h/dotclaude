# Interface Design for Testability

優れたインターフェースは、テストを自然な形で行えるようにします：

1. **依存関係を受け入れ、作り出さない**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **結果を返す。副作用を生じさせない**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **対象範囲が狭い**
    - 手法が少ない = 必要なテストが少なくなる
    - パラメータが少ない = テスト環境の構築が簡単になる