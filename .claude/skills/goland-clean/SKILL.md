---
name: goland-clean
description: JetBrains IDE (GoLand) のコード解析アラートが出ないGoコードを実装します。go vet、golangci-lintによる自動検証と、GoLand固有インスペクションチェックリストを組み合わせて、アラートゼロを保証します。Go実装完了後に必ず使用してください。
---

# GoLand クリーン実装スキル

JetBrains IDE のコード解析アラートを出さないGoコードを書き、実装後に自動検証を行います。
詳細なインスペクション一覧は `inspections.md` を参照してください。

## 適用場面

以下のタイミングで自動的に適用します：
- Goファイルを新規作成したとき
- 既存Goファイルを編集したとき
- Go実装タスクを完了したとき

## 実装時のチェックリスト

コードを書く際に以下を遵守します：

### エラー処理
- [ ] すべての `error` 戻り値をチェックしている
- [ ] `defer` 内の関数呼び出しでも `err` を無視していない
- [ ] `io.Closer` の `Close()` エラーを適切に処理している

### 命名規約
- [ ] エクスポートされるすべての関数・型・変数にコメントを付けている（`// FuncName ...` 形式）
- [ ] 識別子にアンダースコアを使用していない（定数の慣習を除く）
- [ ] パッケージ名は小文字のみ、アンダースコアなし

### コード品質
- [ ] 変数のシャドーイングがない（特に `:=` でのエラー変数）
- [ ] `defer` をループ内で使用していない
- [ ] 到達不能コードがない
- [ ] ゼロ値への不要な初期化がない（例: `var x int = 0` ではなく `var x int`）
- [ ] 不要な型変換がない

### コンテキスト
- [ ] `context.Context` を受け取る関数では第一引数にしている
- [ ] `context.WithCancel` / `context.WithTimeout` のキャンセル関数を `defer cancel()` している
- [ ] `context.Background()` をリクエストスコープで使用していない

### HTTP / IO
- [ ] `http.Response.Body` を `defer resp.Body.Close()` している
- [ ] `http.Get` 等のレスポンスでエラーと `nil` Body を両方チェックしている

### 並行処理
- [ ] `sync.Mutex` 等のロックを含む構造体を値でコピーしていない
- [ ] `goroutine` のリークがない（チャネルに受信者がいる、またはキャンセル可能）

### Printf フォーマット
- [ ] `fmt.Sprintf`、`fmt.Fprintf` 等のフォーマット文字列と引数の型が一致している

## 実装後の検証ステップ

Goコードを書いた後、必ず以下を実行します：

### ステップ 1: go vet
```bash
go vet ./...
```
出力がゼロであることを確認。警告があれば修正してから次へ進む。

### ステップ 2: golangci-lint（利用可能な場合）
```bash
golangci-lint run ./...
```
プロジェクトに `.golangci.yml` がある場合はその設定に従う。
golangci-lint がない場合は `staticcheck ./...` で代替する。

### ステップ 3: ビルド確認
```bash
go build ./...
```
コンパイルエラーがないことを確認。

## よくあるパターンと修正例

### エラー未チェック（BAD）
```go
os.Remove(tmpFile)
resp, _ := http.Get(url)
```

### エラー未チェック（GOOD）
```go
if err := os.Remove(tmpFile); err != nil {
    return fmt.Errorf("remove tmp file: %w", err)
}
resp, err := http.Get(url)
if err != nil {
    return fmt.Errorf("http get: %w", err)
}
defer resp.Body.Close()
```

### エクスポート関数のコメントなし（BAD）
```go
func ProcessData(data []byte) error {
```

### エクスポート関数のコメントあり（GOOD）
```go
// ProcessData validates and transforms the given byte slice.
func ProcessData(data []byte) error {
```

### defer in loop（BAD）
```go
for _, f := range files {
    file, _ := os.Open(f)
    defer file.Close() // ループ終了まで呼ばれない
}
```

### defer in loop（GOOD）
```go
for _, f := range files {
    if err := processFile(f); err != nil {
        return err
    }
}

func processFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close()
    // ...
}
```