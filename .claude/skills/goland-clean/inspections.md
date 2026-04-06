# GoLand インスペクション一覧

JetBrains GoLand が検出する主要なインスペクションの詳細リファレンスです。

## カテゴリ 1: エラー処理

| インスペクション | 説明 | 修正方針 |
|------------|------|---------|
| Error return value not checked | 関数の `error` 戻り値を使用していない | 必ず `if err != nil` でチェックする |
| Ignored error in defer | `defer` 内の関数の `error` を無視 | `defer func() { if err := f.Close(); err != nil {...} }()` |
| Assignment to variable without using it | エラーを `_` で無視 | 適切にエラーを処理する |

## カテゴリ 2: 命名規約

| インスペクション | 説明 | 修正方針 |
|------------|------|---------|
| Exported function/type has no comment | エクスポート識別子にコメントなし | `// FuncName ...` 形式のコメントを追加 |
| Underscore in identifier | 識別子にアンダースコア | MixedCaps (`camelCase`/`PascalCase`) に変更 |
| Package name contains underscore | パッケージ名にアンダースコア | 小文字のみの1単語に変更 |
| ALL_CAPS identifier | 定数以外のALL_CAPS | MixedCaps に変更 |

## カテゴリ 3: コード品質

| インスペクション | 説明 | 修正方針 |
|------------|------|---------|
| Variable shadowing | 外側スコープの変数をシャドーイング | 変数名を変更するか `:=` を `=` に変更 |
| Defer in loop | ループ内の `defer` | ループ本体を別関数に切り出す |
| Unnecessary variable initialization | ゼロ値への明示的初期化 | `var x int = 0` → `var x int` |
| Redundant type conversion | 不要な型変換 | 変換を削除 |
| Unnecessary else after return | `return` 後の `else` | `else` ブロックを削除してフラットに |
| Unreachable code | 到達不能コード | 不要なコードを削除 |
| Boolean expression simplification | `if x == true` 等 | `if x` に簡略化 |
| Struct literal without field names | フィールド名なしの構造体リテラル | フィールド名を明示する |

## カテゴリ 4: go vet 検出項目

GoLand は `go vet` を統合しており、以下を検出します：

| インスペクション | 説明 | 修正方針 |
|------------|------|---------|
| Printf format mismatch | フォーマット文字列と引数の型不一致 | フォーマット指定子を修正 |
| Copying mutex by value | ロックを含む構造体の値コピー | ポインタで渡す |
| Loop variable captured by closure | ループ変数のクロージャキャプチャ | ループ内でローカル変数にコピー（Go 1.22以降は自動修正済み） |
| Range variable in goroutine | goroutine内でのrange変数参照 | ループ変数をコピーして渡す |
| Atomic value copied | `atomic.Value` の値コピー | ポインタで渡す |

## カテゴリ 5: コンテキスト

| インスペクション | 説明 | 修正方針 |
|------------|------|---------|
| context.Context is not the first argument | Context が第一引数でない | 引数の順序を変更 |
| cancel function not called | キャンセル関数が呼ばれない | `defer cancel()` を追加 |
| context.TODO() usage | `context.TODO()` の使用 | 適切な Context を受け取るか `context.Background()` を使用 |

## カテゴリ 6: HTTP / IO

| インスペクション | 説明 | 修正方針 |
|------------|------|---------|
| Response body not closed | `resp.Body` のクローズ忘れ | `defer resp.Body.Close()` を追加 |
| HTTP response not checked for nil | nil Body チェックなし | エラーと Body を両方チェック |

## カテゴリ 7: 並行処理

| インスペクション | 説明 | 修正方針 |
|------------|------|---------|
| Goroutine leak | goroutine が終了しない可能性 | Context キャンセルや done チャネルで制御 |
| Channel not closed | 送信側がチャネルをクローズしない | 送信側で `defer close(ch)` を使用 |
| WaitGroup reuse before wait | Wait 前に WaitGroup を再利用 | 各ゴルーチングループで新しい WaitGroup を作成 |

## カテゴリ 8: 型システム

| インスペクション | 説明 | 修正方針 |
|------------|------|---------|
| Interface type assertion without ok | 型アサーションで ok をチェックしない | `v, ok := x.(T)` 形式を使用 |
| Wrong number of arguments | 関数呼び出しの引数数ミスマッチ | 引数を修正 |
| Nil pointer dereference | nil の可能性があるポインタ参照 | nil チェックを追加 |

## GoLand のデフォルトインスペクション設定

GoLand では以下の重要度で分類されます：
- **Error**: コンパイルエラー、確実なバグ
- **Warning**: 潜在的なバグ、非推奨API
- **Weak Warning**: コードスタイル、改善提案
- **Information**: 情報的なヒント

`go vet` の警告はデフォルトで **Warning** として扱われます。
`golangci-lint` を統合している場合はその設定に準じます。

## プロジェクトへの golangci-lint 統合

GoLand と golangci-lint を連携するには `.golangci.yml` を配置します：

```yaml
linters:
  enable:
    - errcheck      # エラー未チェック
    - govet         # go vet
    - staticcheck   # 静的解析
    - revive        # Go スタイルチェック
    - gochecknoglobals  # グローバル変数チェック
    - godot         # コメント末尾ピリオド
    - misspell      # スペルチェック

linters-settings:
  errcheck:
    check-type-assertions: true
    check-blank: true
  govet:
    shadow: true
```