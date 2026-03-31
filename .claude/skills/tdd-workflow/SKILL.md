---
name: tdd-workflow
description: 新機能の実装、バグ修正、コードのリファクタリングを行う際にこのスキルを使用します。ユニット、統合、E2Eテストを含む80%以上のカバレッジでテスト駆動開発を徹底します。
---

# Test-Driven Development Workflow

このスキルは、すべてのコード開発が包括的なテストカバレッジを伴ったTDD原則に従うことを保証します。

## When to Activate

- 新機能や機能性の実装
- バグや問題の修正
- 既存コードのリファクタリング
- APIエンドポイントの追加
- 新しいコンポーネントの作成

## Core Principles

### 1. Tests BEFORE Code
常にテストを最初に書き、その後にテストを通すコードを実装します。

### 2. Coverage Requirements
- 最低80%のカバレッジ（ユニット + 統合 + E2E）
- すべてのエッジケースをカバー
- エラーシナリオのテスト
- 境界条件の検証

### 3. Test Types

#### Unit Tests
- 個別の関数とユーティリティ
- コンポーネントロジック
- 純粋関数
- ヘルパーとユーティリティ

#### Integration Tests
- APIエンドポイント
- データベース操作
- サービス間の相互作用
- 外部API呼び出し

#### E2E Tests (Playwright)
- 重要なユーザーフロー
- 完全なワークフロー
- ブラウザ自動化
- UI操作

## TDD Workflow Steps

### Step 1: Write User Journeys
```
[役割]として、[行動]したい、[利益]のために

例:
ユーザーとして、マーケットをセマンティックに検索したい、
正確なキーワードがなくても関連するマーケットを見つけるために。
```

### Step 2: Generate Test Cases
各ユーザージャーニーに対して、包括的なテストケースを作成します:

```typescript
describe('Semantic Search', () => {
  it('returns relevant markets for query', async () => {
    // テスト実装
  })

  it('handles empty query gracefully', async () => {
    // エッジケースのテスト
  })

  it('falls back to substring search when Redis unavailable', async () => {
    // フォールバック動作のテスト
  })

  it('sorts results by similarity score', async () => {
    // ソートロジックのテスト
  })
})
```

### Step 3: Run Tests (They Should Fail)
```bash
npm test
# テストは失敗するはず - まだ実装していないため
```

### Step 4: Implement Code
テストを通すための最小限のコードを書きます:

```typescript
// テストに導かれた実装
export async function searchMarkets(query: string) {
  // ここに実装
}
```

### Step 5: Run Tests Again
```bash
npm test
# テストが通るはず
```

### Step 6: Refactor
テストをグリーンに保ちながらコード品質を改善します:
- 重複を除去
- 命名を改善
- パフォーマンスを最適化
- 可読性を向上

### Step 7: Verify Coverage
```bash
npm run test:coverage
# 80%以上のカバレッジを達成したか検証
```

## Testing Patterns

### Unit Test Pattern (Jest/Vitest)
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)

    fireEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### API Integration Test Pattern
```typescript
import { NextRequest } from 'next/server'
import { GET } from './route'

describe('GET /api/markets', () => {
  it('returns markets successfully', async () => {
    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('validates query parameters', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid')
    const response = await GET(request)

    expect(response.status).toBe(400)
  })

  it('handles database errors gracefully', async () => {
    // Mock database failure
    const request = new NextRequest('http://localhost/api/markets')
    // Test error handling
  })
})
```

### E2E Test Pattern (Playwright)
```typescript
import { test, expect } from '@playwright/test'

test('user can search and filter markets', async ({ page }) => {
  // マーケットページに移動
  await page.goto('/')
  await page.click('a[href="/markets"]')

  // ページが読み込まれたことを検証
  await expect(page.locator('h1')).toContainText('Markets')

  // マーケットを検索
  await page.fill('input[placeholder="Search markets"]', 'election')

  // debounceと結果を待機
  await page.waitForTimeout(600)

  // 検索結果が表示されたことを検証
  const results = page.locator('[data-testid="market-card"]')
  await expect(results).toHaveCount(5, { timeout: 5000 })

  // 結果に検索語が含まれることを検証
  const firstResult = results.first()
  await expect(firstResult).toContainText('election', { ignoreCase: true })

  // ステータスでフィルター
  await page.click('button:has-text("Active")')

  // フィルターされた結果を検証
  await expect(results).toHaveCount(3)
})

test('user can create a new market', async ({ page }) => {
  // まずログイン
  await page.goto('/creator-dashboard')

  // マーケット作成フォームに入力
  await page.fill('input[name="name"]', 'Test Market')
  await page.fill('textarea[name="description"]', 'Test description')
  await page.fill('input[name="endDate"]', '2025-12-31')

  // フォームを送信
  await page.click('button[type="submit"]')

  // 成功メッセージを検証
  await expect(page.locator('text=Market created successfully')).toBeVisible()

  // マーケットページへのリダイレクトを検証
  await expect(page).toHaveURL(/\/markets\/test-market/)
})
```

## Test File Organization

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx          # ユニットテスト
│   │   └── Button.stories.tsx       # Storybook
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.test.ts         # 統合テスト
└── e2e/
    ├── markets.spec.ts               # E2Eテスト
    ├── trading.spec.ts
    └── auth.spec.ts
```

## Mocking External Services

### Supabase Mock
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test Market' }],
          error: null
        }))
      }))
    }))
  }
}))
```

### Redis Mock
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}))
```

### OpenAI Mock
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // 1536次元埋め込みのモック
  ))
}))
```

## Test Coverage Verification

### Run Coverage Report
```bash
npm run test:coverage
```

### Coverage Thresholds
```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## Common Testing Mistakes to Avoid

### ❌ 間違い: 実装詳細のテスト
```typescript
// 内部状態をテストしない
expect(component.state.count).toBe(5)
```

### ✅ 正解: ユーザーに見える動作をテスト
```typescript
// ユーザーが見るものをテスト
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### ❌ 間違い: 脆いセレクター
```typescript
// 簡単に壊れる
await page.click('.css-class-xyz')
```

### ✅ 正解: セマンティックなセレクター
```typescript
// 変更に強い
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### ❌ 間違い: テストの独立性がない
```typescript
// テストが互いに依存している
test('creates user', () => { /* ... */ })
test('updates same user', () => { /* 前のテストに依存 */ })
```

### ✅ 正解: 独立したテスト
```typescript
// 各テストが独自のデータをセットアップ
test('creates user', () => {
  const user = createTestUser()
  // テストロジック
})

test('updates user', () => {
  const user = createTestUser()
  // 更新ロジック
})
```

## Continuous Testing

### Watch Mode During Development
```bash
npm test -- --watch
# ファイル変更時に自動的にテストが実行される
```

### Pre-Commit Hook
```bash
# コミットの前に毎回実行
npm test && npm run lint
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Run Tests
  run: npm test -- --coverage
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## Best Practices

1. **テストを最初に書く** - 常にTDD
2. **テストごとに1つのアサーション** - 単一の動作に焦点を当てる
3. **説明的なテスト名** - 何をテストするか説明する
4. **Arrange-Act-Assert** - 明確なテスト構造
5. **外部依存をモック** - ユニットテストを分離
6. **エッジケースをテスト** - null、undefined、空、大きな値
7. **エラーパスをテスト** - ハッピーパスだけでなく
8. **テストを高速に保つ** - ユニットテストは各50ms未満
9. **テスト後にクリーンアップ** - 副作用を残さない
10. **カバレッジレポートをレビュー** - ギャップを特定

## Success Metrics

- 80%以上のコードカバレッジを達成
- すべてのテストが通過（グリーン）
- スキップまたは無効化されたテストがない
- 高速なテスト実行（ユニットテストは30秒未満）
- E2Eテストが重要なユーザーフローをカバー
- テストが本番前にバグを検出

---

**覚えておいてください**: テストはオプションではありません。テストは自信を持ったリファクタリング、迅速な開発、本番環境の信頼性を可能にするセーフティネットです。
