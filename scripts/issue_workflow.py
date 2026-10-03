#!/usr/bin/env python3
"""Check prerequisites before starting an issue and preserve its dedicated branch."""
import argparse
from pathlib import Path
import subprocess
from github_policy import branch_name, readiness

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['check', 'branch'])
    parser.add_argument('number', type=int)
    args = parser.parse_args()
    try:
        issue = readiness(args.number)
    except ValueError as error:
        raise SystemExit(f'Blocked: {error}')
    branch = branch_name(args.number, issue['title'])
    print(f'Ready: #{args.number}; branch {branch}')
    if args.action == 'branch':
        if git('status', '--porcelain'):
            raise SystemExit('Commit or preserve current changes before switching issue branches.')
        git('fetch', 'origin')
        exists = subprocess.run(['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch}'], cwd=ROOT).returncode == 0
        remote = subprocess.run(['git', 'show-ref', '--verify', '--quiet', f'refs/remotes/origin/{branch}'], cwd=ROOT).returncode == 0
        if exists:
            git('switch', branch)
        elif remote:
            git('switch', '--track', f'origin/{branch}')
        else:
            git('switch', '-c', branch, 'origin/main')
        ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', 'origin/main', 'HEAD'], cwd=ROOT).returncode == 0
        if not ancestor:
            git('merge', '--ff-only', 'origin/main')
        print(f'Current branch: {git("branch", "--show-current")}')
