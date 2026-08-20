#!/usr/bin/env python3
"""Pattern 5: Braille dots - dotted progress bar using braille characters"""
import json, os, subprocess, sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

data = json.load(sys.stdin)

BRAILLE = ' ⣀⣄⣤⣦⣶⣷⣿'
R = '\033[0m'
DIM = '\033[2m'

def gradient(pct):
    if pct < 50:
        r = int(pct * 5.1)
        return f'\033[38;2;{r};200;80m'
    else:
        g = int(200 - (pct - 50) * 4)
        return f'\033[38;2;255;{max(g, 0)};60m'

def braille_bar(pct, width=8):
    pct = min(max(pct, 0), 100)
    level = pct / 100
    bar = ''
    for i in range(width):
        seg_start = i / width
        seg_end = (i + 1) / width
        if level >= seg_end:
            bar += BRAILLE[7]
        elif level <= seg_start:
            bar += BRAILLE[0]
        else:
            frac = (level - seg_start) / (seg_end - seg_start)
            bar += BRAILLE[min(int(frac * 7), 7)]
    return bar

def fmt(label, pct):
    p = round(pct)
    return f'{DIM}{label}{R} {gradient(pct)}{braille_bar(pct)}{R} {p}%'

GIT_TIMEOUT = 1.0
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
CYAN = '\033[36m'
BLUE = '\033[34m'


def git_status(cwd):
    """git status を1回だけ呼び、ブランチと差分の要約を返す。git外や失敗時はNone。"""
    if not cwd:
        return None
    try:
        proc = subprocess.run(
            ['git', '--no-optional-locks', 'status', '--porcelain=v2', '--branch'],
            cwd=cwd, capture_output=True, text=True, timeout=GIT_TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None

    head, oid = '', ''
    ahead = behind = staged = dirty = untracked = conflict = 0
    for line in proc.stdout.splitlines():
        if line.startswith('# branch.head '):
            head = line[len('# branch.head '):]
        elif line.startswith('# branch.oid '):
            oid = line[len('# branch.oid '):]
        elif line.startswith('# branch.ab '):
            for tok in line[len('# branch.ab '):].split():
                if tok[1:].isdigit():
                    if tok[0] == '+':
                        ahead = int(tok[1:])
                    elif tok[0] == '-':
                        behind = int(tok[1:])
        elif line[:2] in ('1 ', '2 '):
            xy = line[2:4]
            if xy[0] != '.':
                staged += 1
            if xy[1] != '.':
                dirty += 1
        elif line.startswith('u '):
            conflict += 1
        elif line.startswith('? '):
            untracked += 1

    if head == '(detached)':
        name = oid[:7] if oid and oid != '(initial)' else 'detached'
    elif oid == '(initial)':
        name = f'{head} (no commits)'
    else:
        name = head or 'unknown'

    return {
        'name': name, 'ahead': ahead, 'behind': behind,
        'staged': staged, 'dirty': dirty,
        'untracked': untracked, 'conflict': conflict,
    }


def fmt_git(st):
    counters = (
        ('↑', st['ahead'], CYAN),
        ('↓', st['behind'], BLUE),
        ('+', st['staged'], GREEN),
        ('~', st['dirty'], YELLOW),
        ('?', st['untracked'], DIM),
        ('!', st['conflict'], RED),
    )
    marks = [f'{color}{sign}{n}{R}' for sign, n, color in counters if n]
    branch = f'{CYAN}{st["name"]}{R}'
    if not marks:
        return f'{DIM}git{R} {branch} {GREEN}✓{R}'
    return f'{DIM}git{R} {branch} ' + ' '.join(marks)


model = data.get('model', {}).get('display_name', 'Claude')
parts = [model]

effort_colors = {
    'low':    DIM,
    'medium': '\033[36m',
    'high':   '\033[33m',
    'xhigh':  '\033[38;2;255;165;0m',
    'max':    '\033[31m',
}

ctx = data.get('context_window', {}).get('used_percentage')
if ctx is not None:
    parts.append(fmt('ctx', ctx))

five = data.get('rate_limits', {}).get('five_hour', {}).get('used_percentage')
if five is not None:
    parts.append(fmt('5h', five))

week = data.get('rate_limits', {}).get('seven_day', {}).get('used_percentage')
if week is not None:
    parts.append(fmt('7d', week))

effort_level = (data.get('effort') or {}).get('level') or ''
if effort_level:
    ec = effort_colors.get(effort_level, DIM)
    parts.append(f'{DIM}eff{R} {ec}{effort_level}{R}')

cwd = data.get('workspace', {}).get('current_dir') or data.get('cwd') or ''
if cwd:
    home = os.path.expanduser('~')
    cwd_display = '~' + cwd[len(home):] if cwd.startswith(home) else cwd
    parts.append(f'{DIM}{cwd_display}{R}')

git_st = git_status(cwd)
if git_st:
    parts.append(fmt_git(git_st))

sid = data.get('session_id') or ''
if sid:
    seg = f'{DIM}sid{R} {sid[:8]}'
    sname = data.get('session_name') or ''
    if sname:
        seg += f'[{sname}] '
    parts.append(seg)

print(f' {DIM}│{R} '.join(parts), end='')
