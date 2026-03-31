# Project Guidelines Skill (Example)

これはプロジェクト固有のスキルの例です。自分のプロジェクト用のテンプレートとして使用してください。

実際の本番アプリケーションに基づいています: [Zenith](https://zenith.chat) - AI駆動の顧客発見プラットフォーム。

---

## When to Use

このスキルが設計された特定のプロジェクトで作業する際に参照してください。プロジェクトスキルには以下が含まれます:
- アーキテクチャ概要
- ファイル構造
- コードパターン
- テスト要件
- デプロイワークフロー

---

## Architecture Overview

**Tech Stack:**
- **Frontend**: Next.js 15 (App Router), TypeScript, React
- **Backend**: FastAPI (Python), Pydantic models
- **Database**: Supabase (PostgreSQL)
- **AI**: Claude API with tool calling and structured output
- **Deployment**: Google Cloud Run
- **Testing**: Playwright (E2E), pytest (backend), React Testing Library

**Services:**
```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  Next.js 15 + TypeScript + TailwindCSS                     │
│  Deployed: Vercel / Cloud Run                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         Backend                             │
│  FastAPI + Python 3.11 + Pydantic                          │
│  Deployed: Cloud Run                                       │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Supabase │   │  Claude  │   │  Redis   │
        │ Database │   │   API    │   │  Cache   │
        └──────────┘   └──────────┘   └──────────┘
```

---

## File Structure

```
project/
├── frontend/
│   └── src/
│       ├── app/              # Next.jsのapp routerページ
│       │   ├── api/          # APIルート
│       │   ├── (auth)/       # 認証保護されたルート
│       │   └── workspace/    # メインアプリワークスペース
│       ├── components/       # Reactコンポーネント
│       │   ├── ui/           # ベースUIコンポーネント
│       │   ├── forms/        # フォームコンポーネント
│       │   └── layouts/      # レイアウトコンポーネント
│       ├── hooks/            # カスタムReact hooks
│       ├── lib/              # ユーティリティ
│       ├── types/            # TypeScript定義
│       └── config/           # 設定
│
├── backend/
│   ├── routers/              # FastAPIルートハンドラー
│   ├── models.py             # Pydanticモデル
│   ├── main.py               # FastAPIアプリエントリー
│   ├── auth_system.py        # 認証
│   ├── database.py           # データベース操作
│   ├── services/             # ビジネスロジック
│   └── tests/                # pytestテスト
│
├── deploy/                   # デプロイ設定
├── docs/                     # ドキュメント
└── scripts/                  # ユーティリティスクリプト
```

---

## Code Patterns

### API Response Format (FastAPI)

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def ok(cls, data: T) -> "ApiResponse[T]":
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> "ApiResponse[T]":
        return cls(success=False, error=error)
```

### Frontend API Calls (TypeScript)

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`/api${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      return { success: false, error: `HTTP ${response.status}` }
    }

    return await response.json()
  } catch (error) {
    return { success: false, error: String(error) }
  }
}
```

### Claude AI Integration (Structured Output)

```python
from anthropic import Anthropic
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    key_points: list[str]
    confidence: float

async def analyze_with_claude(content: str) -> AnalysisResult:
    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-5-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": content}],
        tools=[{
            "name": "provide_analysis",
            "description": "Provide structured analysis",
            "input_schema": AnalysisResult.model_json_schema()
        }],
        tool_choice={"type": "tool", "name": "provide_analysis"}
    )

    # tool useの結果を抽出
    tool_use = next(
        block for block in response.content
        if block.type == "tool_use"
    )

    return AnalysisResult(**tool_use.input)
```

### Custom Hooks (React)

```typescript
import { useState, useCallback } from 'react'

interface UseApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export function useApi<T>(
  fetchFn: () => Promise<ApiResponse<T>>
) {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  })

  const execute = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }))

    const result = await fetchFn()

    if (result.success) {
      setState({ data: result.data!, loading: false, error: null })
    } else {
      setState({ data: null, loading: false, error: result.error! })
    }
  }, [fetchFn])

  return { ...state, execute }
}
```

---

## Testing Requirements

### Backend (pytest)

```bash
# 全テストを実行
poetry run pytest tests/

# カバレッジ付きで実行
poetry run pytest tests/ --cov=. --cov-report=html

# 特定のテストファイルを実行
poetry run pytest tests/test_auth.py -v
```

**Test structure:**
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Frontend (React Testing Library)

```bash
# テストを実行
npm run test

# カバレッジ付きで実行
npm run test -- --coverage

# E2Eテストを実行
npm run test:e2e
```

**Test structure:**
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { WorkspacePanel } from './WorkspacePanel'

describe('WorkspacePanel', () => {
  it('renders workspace correctly', () => {
    render(<WorkspacePanel />)
    expect(screen.getByRole('main')).toBeInTheDocument()
  })

  it('handles session creation', async () => {
    render(<WorkspacePanel />)
    fireEvent.click(screen.getByText('New Session'))
    expect(await screen.findByText('Session created')).toBeInTheDocument()
  })
})
```

---

## Deployment Workflow

### Pre-Deployment Checklist

- [ ] 全テストがローカルで通過
- [ ] `npm run build`が成功 (frontend)
- [ ] `poetry run pytest`が通過 (backend)
- [ ] ハードコードされた秘密情報がない
- [ ] 環境変数がドキュメント化されている
- [ ] データベースマイグレーションの準備完了

### Deployment Commands

```bash
# Frontendをビルドしてデプロイ
cd frontend && npm run build
gcloud run deploy frontend --source .

# Backendをビルドしてデプロイ
cd backend
gcloud run deploy backend --source .
```

### Environment Variables

```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# Backend (.env)
DATABASE_URL=postgresql://...
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
```

---

## Critical Rules

1. **絵文字禁止** - コード、コメント、ドキュメントに絵文字を使用しない
2. **イミュータビリティ** - オブジェクトや配列を決してミューテートしない
3. **TDD** - 実装前にテストを書く
4. **80%カバレッジ** 最低ライン
5. **多数の小さなファイル** - 通常200-400行、最大800行
6. **console.log禁止** - 本番コードでは使用しない
7. **適切なエラーハンドリング** - try/catchを使用
8. **入力バリデーション** - PydanticまたはZodを使用

---

## Related Skills

- `coding-standards.md` - 一般的なコーディングベストプラクティス
- `backend-patterns.md` - APIとデータベースパターン
- `frontend-patterns.md` - ReactとNext.jsパターン
- `tdd-workflow/` - テスト駆動開発方法論
