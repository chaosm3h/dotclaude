---
name: setup-pm
description: 優先するパッケージマネージャー(npm/pnpm/yarn/bun)をプロジェクトまたはグローバルに設定。lockファイル/package.json/環境変数の優先順位で検出。「パッケージマネージャー設定」「npm/pnpm/yarn/bun切替」「setup package manager」をトリガとする。
---

# Package Manager Setup Skill

このプロジェクトまたはグローバルに優先するパッケージマネージャーを設定する。

## Usage

```bash
# 現在のパッケージマネージャーを検出
node scripts/setup-package-manager.js --detect

# グローバル設定
node scripts/setup-package-manager.js --global pnpm

# プロジェクト設定
node scripts/setup-package-manager.js --project bun

# 利用可能なパッケージマネージャー一覧
node scripts/setup-package-manager.js --list
```

## Detection Priority

| 順位 | ソース |
|---|---|
| 1 | 環境変数 `CLAUDE_PACKAGE_MANAGER` |
| 2 | プロジェクト設定 `.claude/package-manager.json` |
| 3 | `package.json` の `packageManager` フィールド |
| 4 | Lockファイル (package-lock.json / yarn.lock / pnpm-lock.yaml / bun.lockb) |
| 5 | グローバル設定 `~/.claude/package-manager.json` |
| 6 | フォールバック (pnpm > bun > yarn > npm) |

## Configuration Files

### Global

```json
// ~/.claude/package-manager.json
{ "packageManager": "pnpm" }
```

### Project

```json
// .claude/package-manager.json
{ "packageManager": "bun" }
```

### package.json

```json
{ "packageManager": "pnpm@8.6.0" }
```

## Environment Variable

全検出を上書きするには:

```bash
# macOS/Linux
export CLAUDE_PACKAGE_MANAGER=pnpm

# Windows (PowerShell)
$env:CLAUDE_PACKAGE_MANAGER = "pnpm"
```

## Detect Current

```bash
node scripts/setup-package-manager.js --detect
```
