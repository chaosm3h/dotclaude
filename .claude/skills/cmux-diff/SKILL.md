---
name: cmux-diff
description: cmuxのDiffビューアに差分を表示する。未ステージ、ステージ済み、ブランチ、直近のエージェントターンの4種のgit差分に加え、パッチファイルと標準入力のパッチを専用パネルへ開く。「差分を見たい」「diffを表示」「パッチを開く」をトリガとする。
---

# cmux Diff Viewer

`cmux diff` はunified diffまたはパッチをcmuxのブラウザ分割に描画する。
ターミナルに `git diff` を流す場合と違い、スクロールと検索が効くパネルとして残る。

## When to Activate

- 変更内容を目視で確認したいと指示された時
- レビュー対象のパッチやPRの差分を開く時
- エージェントが直前のターンで何を変更したかを見せる時

## Fast start

```bash
cmux diff --unstaged --cwd /path/to/repo    # 未ステージの変更
cmux diff --staged --cwd /path/to/repo      # ステージ済みの変更
cmux diff --branch --base main              # ブランチをmerge baseと比較
cmux diff --last-turn                       # 直近のエージェントターン以降
git diff | cmux diff -                      # 標準入力のパッチ
cmux diff changes.patch --title "PR #42"    # パッチファイル
```

## 差分ソース

- **unstaged**：作業ツリーとインデックスの差
- **staged**：インデックスとHEADの差
- **branch**：現在のブランチとmerge baseの差。`--base` を省略すると `origin/HEAD` を探し、無ければ `main` を使う
- **last-turn**：呼び出し元サーフェスのエージェントターン基準点以降の変更。`--session` で単一セッションに絞れる

## 落とし穴

### --cwdを省略しない

git系のソースは、`--cwd` を省略するとコマンドを実行したプロセスの作業ディレクトリを基準にする。
呼び出し元サーフェスのcwdにはフォールバックしない。
エージェントから実行する場合はシェルの作業ディレクトリが意図した場所とは限らないため、常に `--cwd` でリポジトリを明示する。

gitリポジトリでないパスを渡すと `cmux diff git sources require a git repository` で終了コード1になる。

### 新規ファイルは差分に出ない

`--unstaged` は `git diff` と同じ範囲を対象とする。
未追跡ファイルも見せたい場合は `git add -N <path>` でintent-to-addしてから開く。

### 終了コードがソースによって非対称

git系のソースは、差分が空でも終了コード0でパネルを開く。
パッチ入力は、空なら `diff input is empty`、ファイルが無ければ `Path does not exist` で終了コード1になる。
パイプで渡す時は結果を確認する。

## 表示の指定

既定のレイアウトは `--layout unified` で、`--layout split` にすると左右に分かれる。
既定値は `cmux.json` の `diffViewer.defaultLayout` で変えられる。
`--font-size` の既定は10ポイント。
`--title` でタブ名を付けておくと、複数の差分を開いた時に見分けられる。

`--focus true` を付けない限りフォーカスは移らない。
既定は `false` なので、確認用のパネルを開いても作業中のターミナルから注意が逸れない。

## パネル内のキー操作

| キー | 動作 |
|------|------|
| `j` / `k` | 下 / 上へスクロール |
| `gg` / `shift+g` | 先頭 / 末尾へ移動 |
| `/` | ファイル検索 |

パネルはGUI操作の `cmd+shift+ctrl+d` でも開く。
いずれのキーも `cmux.json` の `shortcuts.bindings` で変更できる。

## 開いたパネルの後始末

一時的な確認で開いたパネルは `cmux close-surface --surface <uuid>` で閉じる。
refは閉じるたびに振り直されるため、複数を閉じる時は `cmux list-pane-surfaces --id-format both` でUUIDを取ってから指定する。
