---
name: slide-commit
description: PDFビルド→ステージング→コミットを一括実施。slides/とoutput/pdf/のみをステージングし、md+pdfセットコミットルールを強制。「スライドをコミット」「slide commit」「slides/をコミット」をトリガとする。
---

# Slide Commit Skill

PDFビルド → ステージング → コミットを一括実施し、md+pdfセットコミットルールを強制する。

## Usage

```
/slide-commit [コミットメッセージ]
```

- `[コミットメッセージ]`: 省略時は変更内容から自動生成

## Workflow

### 1. 変更確認

`git status slides/` で `slides/` 配下に変更があるか確認する。変更がない場合は報告して終了する。

### 2. PDFビルド

```bash
npm run build:pdf
```

ビルドが失敗した場合はコミットを中断し、エラーを報告する。

### 3. PDF存在確認

変更された各 `.md` ファイルに対応する PDF が `output/pdf/` に生成されていることを確認する。

```bash
git diff --name-only HEAD -- slides/
```

各 `slides/<filename>.md` に対して `output/pdf/<filename>.pdf` が存在するかチェックする。PDFが存在しない場合は警告を出すがステージングは続行する。

### 4. ステージング

`slides/` と `output/pdf/` のみをステージングする:

```bash
git add slides/ output/pdf/
```

`output/pptx/` と `output/html/` は除外する。

### 5. コミットメッセージ生成

引数にメッセージが指定されている場合はそれを使用する。指定がない場合は変更ファイルから自動生成する:

- 新規ファイルのみ: `docs: <ファイル名>スライドを追加`
- 既存ファイルの変更のみ: `docs: <ファイル名>スライドを更新`
- 複数ファイル: `docs: スライドを更新 (<変更数>件)`
- 新規+変更混在: `docs: スライドを追加・更新 (<合計数>件)`

### 6. コミット実行

ステージング内容を `git diff --cached` で確認・表示してからコミットする:

```bash
git commit -m "<メッセージ>"
```

### 7. 完了報告

コミット完了後に `git log --stat -1` の出力と共に含まれるファイルを報告する:

```
コミット完了
コミットメッセージ: <メッセージ>
含まれるファイル:
  slides/<filename>.md
  output/pdf/<filename>.pdf
  ...
```

## Notes

- `npm run build:pdf` は `slides/` 配下の全 `.md` をビルド対象とする
- `output/pptx/` は `.gitignore` 対象のため自動的に除外される
