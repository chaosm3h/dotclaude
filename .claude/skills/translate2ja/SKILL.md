---
name: translate2ja
description: ディレクトリ内のすべての.mdをバッチ処理で日本語に翻訳し、元のファイルを上書きします。ユーザーがマークダウンファイルを日本語に翻訳したい場合、ドキュメントのローカライズ、英語コンテンツの日本語化、または「日本語に翻訳」「mdファイルを日本語に」「translate to Japanese」「日本語化」といったマークダウンファイルのローカライズ要求を口にした際にこのスキルを使用します。ユーザーがディレクトリを指し示し「これを日本語にして」と言った場合にもトリガーされます。.
---

# Translate Markdown Files to Japanese

Translate all `.md` files in the target directory to Japanese, overwriting each file in place.

## Usage

```
/translate2ja [directory]
```

If no directory is given, use the current working directory. The path can be absolute or relative.

## Workflow

### 1. Discover files

Use Glob to find all `*.md` files recursively under the target directory.

### 2. Translate each file

For every discovered file:

1. Read the full content with the Read tool
2. Apply the translation rules below
3. Overwrite the file with the translated content using the Write tool

Process files one at a time. Do not skip any file.

### 3. Report

After all files are done, report how many files were translated and flag any that were skipped or errored.

---

## Translation Rules

### What to translate

- Prose text: paragraphs, sentences, list item labels, description text
- Inline comments inside code blocks:
  - `// this comment` → `// このコメント`
  - `# this comment` (shell/Python) → `# このコメント`
  - `/* this */` → `/* このコメント */`
  - `<!-- this -->` → `<!-- このコメント -->`

### What NOT to translate

| Element | Example | Rule |
|---------|---------|------|
| YAML frontmatter | `---\nname: foo\n---` | Preserve exactly — do not change any key or value |
| Code block content | ` ```js\nconst x = 1\n``` ` | Preserve as-is, except translate comments within |
| Inline code | `` `variable_name` `` | Preserve exactly |
| Technical terms | Google Ads, Meta Ads, CTR, CPC, CPA, ROAS, EMQ, API, URL, HTML, CSS | Keep in English |
| URLs and file paths | `https://...`, `./path/to/file` | Keep as-is |
| Variable/function names | `getUserById`, `MAX_RETRIES` | Keep as-is |

Headings (`#`, `##`, etc.) can remain in English or be translated — use judgment based on whether the heading is a proper noun, command name, or descriptive label.

---

## Quality standards

- Write natural, fluent Japanese — avoid literal word-for-word translations
- Preserve all markdown formatting: `**bold**`, `*italic*`, `>` blockquotes, `---` rules
- For links `[text](url)`, translate the link text if it's descriptive prose; keep technical labels as-is
- Preserve table structure — translate only cell content that is prose
- Never alter code, variables, or file references
