---
name: security-review
description: 認証の追加、ユーザー入力の処理、秘密情報の扱い、APIエンドポイントの作成、または決済・機密機能の実装時にこのスキルを使用します。包括的なセキュリティチェックリストとパターンを提供します。
---

# Security Review Skill

このスキルは、すべてのコードがセキュリティのベストプラクティスに従い、潜在的な脆弱性を特定することを保証します。

## When to Activate

- 認証または認可の実装
- ユーザー入力またはファイルアップロードの処理
- 新しいAPIエンドポイントの作成
- 秘密情報または認証情報の扱い
- 決済機能の実装
- 機密データの保存または送信
- サードパーティAPIの統合

## Security Checklist

### 1. Secrets Management

#### ❌ 絶対にやってはいけないこと
```typescript
const apiKey = "sk-proj-xxxxx"  // ハードコードされた秘密情報
const dbPassword = "password123" // ソースコード内
```

#### ✅ 必ずこうすること
```typescript
const apiKey = process.env.OPENAI_API_KEY
const dbUrl = process.env.DATABASE_URL

// 秘密情報が存在することを確認
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

#### Verification Steps
- [ ] ハードコードされたAPIキー、トークン、パスワードがないこと
- [ ] すべての秘密情報が環境変数にあること
- [ ] `.env.local`が.gitignoreに含まれていること
- [ ] git履歴に秘密情報がないこと
- [ ] 本番環境の秘密情報がホスティングプラットフォーム(Vercel、Railway)にあること

### 2. Input Validation

#### 常にユーザー入力を検証する
```typescript
import { z } from 'zod'

// 検証スキーマを定義
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
})

// 処理前に検証
export async function createUser(input: unknown) {
  try {
    const validated = CreateUserSchema.parse(input)
    return await db.users.create(validated)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.errors }
    }
    throw error
  }
}
```

#### File Upload Validation
```typescript
function validateFileUpload(file: File) {
  // サイズチェック (最大5MB)
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    throw new Error('File too large (max 5MB)')
  }

  // タイプチェック
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type')
  }

  // 拡張子チェック
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif']
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!extension || !allowedExtensions.includes(extension)) {
    throw new Error('Invalid file extension')
  }

  return true
}
```

#### Verification Steps
- [ ] すべてのユーザー入力がスキーマで検証されていること
- [ ] ファイルアップロードが制限されていること（サイズ、タイプ、拡張子）
- [ ] クエリでユーザー入力を直接使用していないこと
- [ ] ホワイトリスト検証（ブラックリストではない）
- [ ] エラーメッセージが機密情報を漏らさないこと

### 3. SQL Injection Prevention

#### ❌ 絶対にSQLを結合しないこと
```typescript
// 危険 - SQLインジェクションの脆弱性
const query = `SELECT * FROM users WHERE email = '${userEmail}'`
await db.query(query)
```

#### ✅ 必ずパラメータ化されたクエリを使用すること
```typescript
// 安全 - パラメータ化されたクエリ
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail)

// または生SQLで
await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
)
```

#### Verification Steps
- [ ] すべてのデータベースクエリがパラメータ化されたクエリを使用していること
- [ ] SQLで文字列連結を使用していないこと
- [ ] ORM/クエリビルダーが正しく使用されていること
- [ ] Supabaseクエリが適切にサニタイズされていること

### 4. Authentication & Authorization

#### JWT Token Handling
```typescript
// ❌ 間違い: localStorage (XSSに脆弱)
localStorage.setItem('token', token)

// ✅ 正しい: httpOnly cookies
res.setHeader('Set-Cookie',
  `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`)
```

#### Authorization Checks
```typescript
export async function deleteUser(userId: string, requesterId: string) {
  // 必ず最初に認可を確認
  const requester = await db.users.findUnique({
    where: { id: requesterId }
  })

  if (requester.role !== 'admin') {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 403 }
    )
  }

  // 削除を実行
  await db.users.delete({ where: { id: userId } })
}
```

#### Row Level Security (Supabase)
```sql
-- すべてのテーブルでRLSを有効化
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- ユーザーは自分のデータのみ閲覧可能
CREATE POLICY "Users view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- ユーザーは自分のデータのみ更新可能
CREATE POLICY "Users update own data"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

#### Verification Steps
- [ ] トークンがhttpOnly cookieに保存されている（localStorageではない）こと
- [ ] 機密操作の前に認可チェックがあること
- [ ] SupabaseでRow Level Securityが有効化されていること
- [ ] ロールベースのアクセス制御が実装されていること
- [ ] セッション管理が安全であること

### 5. XSS Prevention

#### Sanitize HTML
```typescript
import DOMPurify from 'isomorphic-dompurify'

// 必ずユーザー提供のHTMLをサニタイズ
function renderUserContent(html: string) {
  const clean = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p'],
    ALLOWED_ATTR: []
  })
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

#### Content Security Policy
```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self';
      connect-src 'self' https://api.example.com;
    `.replace(/\s{2,}/g, ' ').trim()
  }
]
```

#### Verification Steps
- [ ] ユーザー提供のHTMLがサニタイズされていること
- [ ] CSPヘッダーが設定されていること
- [ ] 検証されていない動的コンテンツのレンダリングがないこと
- [ ] ReactのビルトインXSS保護が使用されていること

### 6. CSRF Protection

#### CSRF Tokens
```typescript
import { csrf } from '@/lib/csrf'

export async function POST(request: Request) {
  const token = request.headers.get('X-CSRF-Token')

  if (!csrf.verify(token)) {
    return NextResponse.json(
      { error: 'Invalid CSRF token' },
      { status: 403 }
    )
  }

  // リクエストを処理
}
```

#### SameSite Cookies
```typescript
res.setHeader('Set-Cookie',
  `session=${sessionId}; HttpOnly; Secure; SameSite=Strict`)
```

#### Verification Steps
- [ ] 状態変更操作にCSRFトークンがあること
- [ ] すべてのcookieにSameSite=Strictがあること
- [ ] ダブルサブミットcookieパターンが実装されていること

### 7. Rate Limiting

#### API Rate Limiting
```typescript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分
  max: 100, // ウィンドウあたり100リクエスト
  message: 'Too many requests'
})

// ルートに適用
app.use('/api/', limiter)
```

#### Expensive Operations
```typescript
// 検索に対する厳格なレート制限
const searchLimiter = rateLimit({
  windowMs: 60 * 1000, // 1分
  max: 10, // 1分あたり10リクエスト
  message: 'Too many search requests'
})

app.use('/api/search', searchLimiter)
```

#### Verification Steps
- [ ] すべてのAPIエンドポイントにレート制限があること
- [ ] 高コスト操作にはより厳格な制限があること
- [ ] IPベースのレート制限
- [ ] ユーザーベースのレート制限（認証済み）

### 8. Sensitive Data Exposure

#### Logging
```typescript
// ❌ 間違い: 機密データをログに記録
console.log('User login:', { email, password })
console.log('Payment:', { cardNumber, cvv })

// ✅ 正しい: 機密データを編集
console.log('User login:', { email, userId })
console.log('Payment:', { last4: card.last4, userId })
```

#### Error Messages
```typescript
// ❌ 間違い: 内部詳細を露出
catch (error) {
  return NextResponse.json(
    { error: error.message, stack: error.stack },
    { status: 500 }
  )
}

// ✅ 正しい: 一般的なエラーメッセージ
catch (error) {
  console.error('Internal error:', error)
  return NextResponse.json(
    { error: 'An error occurred. Please try again.' },
    { status: 500 }
  )
}
```

#### Verification Steps
- [ ] ログにパスワード、トークン、秘密情報がないこと
- [ ] ユーザー向けエラーメッセージは一般的であること
- [ ] 詳細なエラーはサーバーログのみにあること
- [ ] スタックトレースがユーザーに露出していないこと

### 9. Blockchain Security (Solana)

#### Wallet Verification
```typescript
import { verify } from '@solana/web3.js'

async function verifyWalletOwnership(
  publicKey: string,
  signature: string,
  message: string
) {
  try {
    const isValid = verify(
      Buffer.from(message),
      Buffer.from(signature, 'base64'),
      Buffer.from(publicKey, 'base64')
    )
    return isValid
  } catch (error) {
    return false
  }
}
```

#### Transaction Verification
```typescript
async function verifyTransaction(transaction: Transaction) {
  // 受信者を確認
  if (transaction.to !== expectedRecipient) {
    throw new Error('Invalid recipient')
  }

  // 金額を確認
  if (transaction.amount > maxAmount) {
    throw new Error('Amount exceeds limit')
  }

  // ユーザーに十分な残高があることを確認
  const balance = await getBalance(transaction.from)
  if (balance < transaction.amount) {
    throw new Error('Insufficient balance')
  }

  return true
}
```

#### Verification Steps
- [ ] ウォレット署名が検証されていること
- [ ] トランザクション詳細が検証されていること
- [ ] トランザクション前に残高チェックがあること
- [ ] ブラインドトランザクション署名がないこと

### 10. Dependency Security

#### Regular Updates
```bash
# 脆弱性をチェック
npm audit

# 自動修正可能な問題を修正
npm audit fix

# 依存関係を更新
npm update

# 古いパッケージをチェック
npm outdated
```

#### Lock Files
```bash
# 必ずロックファイルをコミット
git add package-lock.json

# CI/CDで再現可能なビルドに使用
npm ci  # npm installの代わりに
```

#### Verification Steps
- [ ] 依存関係が最新であること
- [ ] 既知の脆弱性がないこと（npm audit clean）
- [ ] ロックファイルがコミットされていること
- [ ] GitHubでDependabotが有効化されていること
- [ ] 定期的なセキュリティアップデート

## Security Testing

### Automated Security Tests
```typescript
// 認証をテスト
test('requires authentication', async () => {
  const response = await fetch('/api/protected')
  expect(response.status).toBe(401)
})

// 認可をテスト
test('requires admin role', async () => {
  const response = await fetch('/api/admin', {
    headers: { Authorization: `Bearer ${userToken}` }
  })
  expect(response.status).toBe(403)
})

// 入力検証をテスト
test('rejects invalid input', async () => {
  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ email: 'not-an-email' })
  })
  expect(response.status).toBe(400)
})

// レート制限をテスト
test('enforces rate limits', async () => {
  const requests = Array(101).fill(null).map(() =>
    fetch('/api/endpoint')
  )

  const responses = await Promise.all(requests)
  const tooManyRequests = responses.filter(r => r.status === 429)

  expect(tooManyRequests.length).toBeGreaterThan(0)
})
```

## Pre-Deployment Security Checklist

本番環境デプロイ前に必須:

- [ ] **Secrets**: ハードコードされた秘密情報がない、すべて環境変数にある
- [ ] **Input Validation**: すべてのユーザー入力が検証されている
- [ ] **SQL Injection**: すべてのクエリがパラメータ化されている
- [ ] **XSS**: ユーザーコンテンツがサニタイズされている
- [ ] **CSRF**: 保護が有効化されている
- [ ] **Authentication**: 適切なトークン処理
- [ ] **Authorization**: ロールチェックが実装されている
- [ ] **Rate Limiting**: すべてのエンドポイントで有効化されている
- [ ] **HTTPS**: 本番環境で強制されている
- [ ] **Security Headers**: CSP、X-Frame-Optionsが設定されている
- [ ] **Error Handling**: エラーに機密データがない
- [ ] **Logging**: 機密データがログに記録されていない
- [ ] **Dependencies**: 最新で脆弱性がない
- [ ] **Row Level Security**: Supabaseで有効化されている
- [ ] **CORS**: 適切に設定されている
- [ ] **File Uploads**: 検証されている（サイズ、タイプ）
- [ ] **Wallet Signatures**: 検証されている（blockchainの場合）

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Next.js Security](https://nextjs.org/docs/security)
- [Supabase Security](https://supabase.com/docs/guides/auth)
- [Web Security Academy](https://portswigger.net/web-security)

---

**覚えておいてください**: セキュリティはオプションではありません。1つの脆弱性がプラットフォーム全体を危険にさらす可能性があります。不明な場合は、慎重な側に立つべきです。
