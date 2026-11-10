#!/bin/bash
# 本リポジトリで定義した Claude 設定を、指定したリポジトリの .claude/ にコピーする。
#
# 使い方: ./setup.sh <反映先ディレクトリ>
set -euo pipefail

usage() {
    echo "使い方: $0 <反映先ディレクトリ>" >&2
    echo "  反映先ディレクトリの .claude/ に、本リポジトリの設定をコピーします。" >&2
}

if [ "$#" -ne 1 ] || [ -z "$1" ]; then
    usage
    exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
    echo "エラー: rsync が見つかりません。" >&2
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "エラー: ディレクトリが存在しません: $1" >&2
    exit 1
fi

# スクリプトの場所を基準にする(実行時のカレントディレクトリに依存しない)
DOTFILES="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/.claude"
TARGET_ROOT="$(cd "$1" && pwd -P)"
TARGET="$TARGET_ROOT/.claude"

# 自分自身への上書きを防ぐ
if [ -d "$TARGET" ] && [ "$(cd "$TARGET" && pwd -P)" = "$DOTFILES" ]; then
    echo "エラー: 反映先が本リポジトリ自身です: $TARGET_ROOT" >&2
    exit 1
fi

mkdir -p "$TARGET"

# 反映対象
ITEMS=("agents" "hooks" "rules" "skills")

# 除外対象
#   シンボリックリンク : cmux 等が各マシンで張る絶対パスのリンクは、コピー先で壊れるため除外
#   settings.local.json : マシン固有のローカル設定
#   *-workspace/    : スキル評価用の作業ディレクトリ
#   skills/synced/  : 外部ツールが同期するスキルで、本リポジトリの定義ではない
LINK_EXCLUDES="$(mktemp)"
trap 'rm -f "$LINK_EXCLUDES"' EXIT
(cd "$DOTFILES" && find . -type l | sed 's#^\./#/#') > "$LINK_EXCLUDES"

RSYNC_OPTS=(
    -a
    --exclude-from "$LINK_EXCLUDES"
    --exclude "settings.local.json"
    --exclude "*-workspace/"
    --exclude "/skills/synced/"
    --exclude ".DS_Store"
)

# 既存ファイルは同名のものだけ上書きし、反映先に元からあるファイルは削除しない
for item in "${ITEMS[@]}"; do
    if [ ! -e "$DOTFILES/$item" ]; then
        echo "スキップ(存在しません): $item" >&2
        continue
    fi
    rsync "${RSYNC_OPTS[@]}" "$DOTFILES/$item" "$TARGET/"
    echo "コピー: $item -> $TARGET/$item"
done

# ユーザースコープ(~/.claude)へのシンボリックリンク配置
#   CLAUDE.md / settings.json / statusline.py は、コピーではなくリンクで配置する。
#   既に何かが存在する場合(通常ファイル・別のリンク・壊れたリンクを含む)は何もしない。
USER_CLAUDE="$HOME/.claude"
LINK_ITEMS=("CLAUDE.md" "settings.json" "statusline.py")

mkdir -p "$USER_CLAUDE"

for item in "${LINK_ITEMS[@]}"; do
    src="$DOTFILES/$item"
    dest="$USER_CLAUDE/$item"

    if [ ! -e "$src" ]; then
        echo "スキップ(存在しません): $item" >&2
    elif [ -e "$dest" ] || [ -L "$dest" ]; then
        echo "スキップ(既に存在します): $dest"
    else
        ln -s "$src" "$dest"
        echo "リンク: $dest -> $src"
    fi
done
