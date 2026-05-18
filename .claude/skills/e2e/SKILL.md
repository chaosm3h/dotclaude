---
name: e2e
description: Playwrightでend-to-endテストを生成・実行。Page Object Modelでテストジャーニーを作成し、複数ブラウザ実行、スクリーンショット/ビデオ/トレース取得、不安定テスト検出。「e2e」「Playwright」「end-to-endテスト」をトリガとする。
---

# E2E Skill

このskillは `e2e-runner` agent を呼び出すラッパーです。

## When to Activate

- 重要なユーザージャーニーのテスト (ログイン、取引、決済)
- 複数ステップフローのend-to-end検証
- UIインタラクション/ナビゲーションテスト
- フロント-バック統合検証
- 本番デプロイ準備

## How to Execute

1. **agent起動**: Task ツールで `e2e-runner` agent (`~/.claude/agents/e2e-runner.md`) を起動。
2. **agentに要求する作業**:
   - ユーザーフロー分析 → テストシナリオ特定
   - Playwrightテスト生成 (Page Object Model)
   - 複数ブラウザ実行 (Chromium / Firefox / WebKit)
   - 失敗時アーティファクト取得 (スクリーンショット/ビデオ/トレース)
   - HTMLレポート / JUnit XML 生成
   - 不安定テスト隔離・修正提案

## Best Practices

実施する:
- Page Object Model で保守性確保
- `data-testid` セレクタ
- APIレスポンス待ち (任意タイムアウト不可)
- mainマージ前のテスト実行

実施しない:
- 脆弱なセレクタ (CSSクラス)
- 実装詳細のテスト
- 本番環境への取引テスト (testnet/staging限定)
- 不安定テストの放置

## Safety Rules

- 実際のお金が関わるE2Eは testnet/staging のみ
- 本番環境向けの取引テストを実行しない
- 財務テストは `test.skip(process.env.NODE_ENV === 'production')`
- テストウォレットのみ使用 (少額)

## Integration

- 細粒度なユニット/統合テストは `tdd` skill
- CI/CD 統合は `verification-loop` skill のテストフェーズと連動
