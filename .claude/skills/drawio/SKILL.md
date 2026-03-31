---
name: drawio
description: ユーザーが図、フローチャート、アーキテクチャ図、ER図、シーケンス図、クラス図、ネットワーク図、状態遷移図、画面遷移図、モックアップ、ワイヤーフレーム、UIスケッチの作成、生成、描画、設計を依頼したとき、またはdraw.io、drawio、drawoi、.drawioファイル、PNG/SVG/PDFへの図のエクスポートについて言及したときに必ず使用してください。
---

# Draw.io 図作成スキル

draw.ioの図をネイティブの `.drawio` ファイルとして生成します。オプションで、図のXMLを埋め込んだ状態でPNG、SVG、またはPDFにエクスポートできます（エクスポートされたファイルはdraw.ioで編集可能なまま保持されます）。

## 図の作成方法

1. リクエストされた図に対して、mxGraphModel形式の **draw.io XMLを生成** します。
2. Writeツールを使用して、現在の作業ディレクトリにXMLを `.drawio` ファイルとして **書き込みます**。
3. **ユーザーがエクスポート形式（png, svg, pdf）をリクエストした場合**、draw.io CLI（以下を参照）を探し、`--embed-diagram` を指定してエクスポートし、元の `.drawio` ファイルを削除します。CLIが見つからない場合は、`.drawio` ファイルを保持し、エクスポートを有効にするためにdraw.ioデスクトップアプリをインストールするか、`.drawio` ファイルを直接開くことができる旨をユーザーに伝えます。
4. **結果を開きます** — エクスポートされた場合はそのファイルを、そうでない場合は `.drawio` ファイルを開きます。openコマンドが失敗した場合は、ユーザーが手動で開けるようにファイルパスを表示します。

## 出力形式の選択

ユーザーのリクエストから形式の好みを判断してください。例：

- `/drawio フローチャートを作成して` → `flowchart.drawio`
- `/drawio ログインフローをpngで作成` → `login-flow.drawio.png`
- `/drawio svg: ER図` → `er-diagram.drawio.svg`
- `/drawio pdf アーキテクチャ構成図` → `architecture-overview.drawio.pdf`

形式の指定がない場合は、`.drawio` ファイルを書き込んでdraw.ioで開くだけにします。ユーザーは後からエクスポートを依頼することもできます。

### サポートされているエクスポート形式

| 形式 | XMLの埋め込み | 備考 |
|--------|-----------|-------|
| `png` | はい (`-e`) | どこでも表示可能、draw.ioで編集可能 |
| `svg` | はい (`-e`) | スケーラブル、draw.ioで編集可能 |
| `pdf` | はい (`-e`) | 印刷可能、draw.ioで編集可能 |
| `jpg` | いいえ | 非可逆圧縮、埋め込みXML非対応 |

PNG、SVG、PDFはいずれも `--embed-diagram` をサポートしています。エクスポートされたファイルには完全な図のXMLが含まれているため、draw.ioで開くと編集可能な図が復元されます。

## draw.io CLI

draw.ioデスクトップアプリには、エクスポート用のコマンドラインインターフェースが含まれています。

### CLIの場所

まず環境を検出し、それに応じてCLIを特定します。

#### WSL2 (Windows Subsystem for Linux)

`/proc/version` に `microsoft` または `WSL` が含まれている場合にWSL2として検出されます。

```bash
grep -qi microsoft /proc/version 2>/dev/null && echo "WSL2"
```

WSL2では、`/mnt/c/...` 経由でWindows版のdraw.ioデスクトップ実行ファイルを使用します。

```bash
DRAWIO_CMD=`/mnt/c/Program Files/draw.io/draw.io.exe`
```

bashで `Program Files` のスペースを扱うために、バッククォートによるクォーティングが必要です。

draw.ioがデフォルト以外の場所にインストールされている場合は、一般的な代替パスを確認してください。

```bash
# デフォルトのインストールパス
`/mnt/c/Program Files/draw.io/draw.io.exe`

# ユーザーごとのインストール（上記が存在しない場合）
`/mnt/c/Users/$WIN_USER/AppData/Local/Programs/draw.io/draw.io.exe`
```

#### macOS

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io
```

#### Linux (ネイティブ)

```bash
drawio   # 通常、snap/apt/flatpak経由でPATHに存在します
```

#### Windows (ネイティブ、非WSL2)

```
"C:\Program Files\draw.io\draw.io.exe"
```

プラットフォーム固有のパスにフォールバックする前に、`which drawio` (Windowsの場合は `where drawio`) を使用してPATH上に存在するか確認してください。

### エクスポートコマンド

```bash
drawio -x -f <format> -e -b 10 -o <output> <input.drawio>
```

**WSL2の例:**

```bash
`/mnt/c/Program Files/draw.io/draw.io.exe` -x -f png -e -b 10 -o diagram.drawio.png diagram.drawio
```

主なフラグ:
- `-x` / `--export`: エクスポートモード
- `-f` / `--format`: 出力形式 (png, svg, pdf, jpg)
- `-e` / `--embed-diagram`: 出力に図のXMLを埋め込む (PNG, SVG, PDFのみ)
- `-o` / `--output`: 出力ファイルパス
- `-b` / `--border`: 図の周囲の境界線の幅 (デフォルト: 0)
- `-t` / `--transparent`: 背景を透明にする (PNGのみ)
- `-s` / `--scale`: 図のサイズをスケールする
- `--width` / `--height`: 指定した寸法に収める (アスペクト比を維持)
- `-a` / `--all-pages`: すべてのページをエクスポートする (PDFのみ)
- `-p` / `--page-index`: 特定のページを選択する (1始まり)

### 結果を開く

| 環境 | コマンド |
|-------------|---------|
| macOS | `open <file>` |
| Linux (ネイティブ) | `xdg-open <file>` |
| WSL2 | `cmd.exe /c start "" "$(wslpath -w <file>)"` |
| Windows | `start <file>` |

**WSL2に関する注意:**
- `wslpath -w <file>` はWSL2のパス（例: `/home/user/diagram.drawio`）をWindowsのパス（例: `C:\Users\...`）に変換します。これは `cmd.exe` が `/mnt/c/...` 形式のパスを解決できないために必要です。
- `start` の後の空文字列 `""` は、`start` がファイル名をウィンドウタイトルとして解釈するのを防ぐために必要です。

**WSL2の例:**

```bash
cmd.exe /c start "" "$(wslpath -w diagram.drawio)"
```

## ファイルの命名

- 図の内容に基づいたわかりやすいファイル名を使用してください（例: `login-flow`, `database-schema`）。
- 複数の単語からなる名前には、小文字とハイフンを使用してください。
- エクスポートの場合は、2重の拡張子 `name.drawio.png`, `name.drawio.svg`, `name.drawio.pdf` を使用してください。これにより、ファイルに埋め込まれた図のXMLが含まれていることが示されます。
- エクスポートが成功したら、中間ファイルである `.drawio` ファイルを削除してください。エクスポートされたファイルに完全な図が含まれています。

## XML形式

`.drawio` ファイルはネイティブのmxGraphModel XMLです。常にXMLを直接生成してください。MermaidやCSV形式はサーバー側での変換が必要であり、ネイティブファイルとして保存できません。

### 基本構造

すべての図は以下の構造を持つ必要があります。

```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- 図のセルはここに parent="1" で配置します -->
  </root>
</mxGraphModel>
```

- セル `id="0"` はルートレイヤーです。
- セル `id="1"` はデフォルトの親レイヤーです。
- 複数のレイヤーを使用しない限り、すべての図の要素は `parent="1"` を使用します。

一般的なスタイル、スタイルプロパティ、エッジルーティングの詳細（ウェイポイントを含む）、コンテナ/グループの例については、`references/xml-reference.md` を参照してください。

## エッジルーティング

**重要: すべてのエッジ `mxCell` には、ウェイポイントがない場合でも、子要素として `<mxGeometry relative="1" as="geometry" />` を含める必要があります。** 自己終了型のエッジセル（例: `<mxCell ... edge="1" ... />`）は無効であり、正しくレンダリングされません。常に展開された形式を使用してください。
```xml
<mxCell id="e1" edge="1" parent="1" source="a" target="b" style="...">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

- 直角コネクタには `edgeStyle=orthogonalEdgeStyle` を使用してください（最も一般的）。
- **ノードの間隔を十分に空けてください** — 水平方向に200px、垂直方向に120pxの間隔を推奨します。
- **矢印の頭のためのスペースを確保してください** — ターゲットの前に少なくとも20pxの直線セグメントを設けます。
- エッジが重なる場合は、明示的な **ウェイポイント** を追加してください。
- すべてのノードをグリッド（10の倍数）に合わせます。
- **エッジラベル**: フォントサイズを小さくするためにエッジラベルをHTMLタグで囲まないでください。エッジラベルのデフォルトのフォントサイズはすでに11px（頂点は12px）であり、すでに小さくなっています。`value` 属性を直接設定してください。

完全なエッジルーティングとコンテナのガイダンスについては、`references/xml-reference.md` を参照してください。

## コンテナとグループ

入れ子になった要素には親子の包含関係 (`parent="containerId"`) を使用してください。単に形状を積み重ねるだけでは **いけません**。子要素はコンテナ内での **相対座標** を使用します。コンテナの種類、ルール、例については `references/xml-reference.md` を参照してください。

## ダークモードの色

draw.ioは自動ダークモードレンダリングをサポートしています。色の挙動はプロパティによって異なります。

- **`strokeColor`, `fillColor`, `fontColor`** はデフォルトで `"default"` になり、ライトテーマでは黒、ダークテーマでは白でレンダリングされます。明示的な色が設定されていない場合、色は自動的に適応します。
- **明示的な色** (例: `fillColor=#DAE8FC`) はライトモードの色を指定します。ダークモードの色は、RGB値を反転させ（93%で反転色にブレンド）、色相を180°回転させることで自動的に計算されます (`mxUtils.getInverseColor` 経由)。
- **`light-dark()` 関数** — 両方の色を明示的に指定するには、スタイル文字列で `light-dark(lightColor,darkColor)` を使用します（例: `fontColor=light-dark(#7EA6E0,#FF0000)`）。最初の引数はライトモードで使用され、2番目の引数はダークモードで使用されます。

ダークモードの色適応を有効にするには、`mxGraphModel` 要素に `adaptiveColors="auto"` を含める必要があります。

図を生成する際、通常はダークモードの色を指定する必要はありません。自動反転がほとんどのケースを処理します。自動反転色が不十分な場合にのみ `light-dark()` を使用してください。

## スタイルリファレンス

完全なdraw.ioスタイルリファレンスはこちら: https://www.drawio.com/doc/faq/drawio-style-reference.html

XMLスキーマ定義 (XSD) はこちら: https://www.drawio.com/assets/mxfile.xsd

## トラブルシューティング

| 問題 | 原因 | 解決策 |
|---------|-------|----------|
| draw.io CLIが見つからない | デスクトップアプリがインストールされていない、またはPATHにない | `.drawio` ファイルを保持し、ユーザーにdraw.ioデスクトップアプリのインストールを依頼するか、ファイルを手動で開くよう伝えます |
| エクスポートで空または破損したファイルが生成される | 無効なXML（例: コメント内の二重ハイフン、エスケープされていない特殊文字） | 書き込む前にXMLの整合性を検証します。以下のXML整合性のセクションを参照してください |
| 図は開くが空白に見える | ルートセル `id="0"` と `id="1"` が欠落している | 基本的なmxGraphModel構造が完全であることを確認します |
| エッジがレンダリングされない | エッジのmxCellが自己終了している（子要素のmxGeometryがない） | すべてのエッジに子要素として `<mxGeometry relative="1" as="geometry" />` が必要です |
| エクスポート後にファイルが開けない | ファイルパスが正しくない、またはファイルの関連付けがない | ユーザーが手動で開けるように絶対ファイルパスを表示します |

## 重要: XMLの整合性

- **XMLコメント内では絶対に二重ハイフン (`--`) を使用しないでください。** XML仕様により `<!-- -->` 内での `--` は禁止されており、パースエラーの原因となります。単一のハイフンを使用するか、言い換えてください。
- 属性値内の特殊文字をエスケープしてください: `&amp;`, `&lt;`, `&gt;`, `&quot;`
- 各 `mxCell` には常にユニークな `id` 値を使用してください。
