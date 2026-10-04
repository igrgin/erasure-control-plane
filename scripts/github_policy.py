#!/usr/bin/env python3
"""Read live issue prerequisites and derive the dedicated issue branch name."""
import json
import os
import re
import subprocess
import unicodedata

TYPES = {'bug', 'spike', 'implement', 'epic'}


def api(path, data=None, method=None):
    args = ['gh', 'api', path, '-H', 'Accept: application/vnd.github+json']
    if method:
        args += ['--method', method]
    if data is not None:
        args += ['--input', '-']
    result = subprocess.run(args, input=json.dumps(data) if data is not None else None,
                            text=True, capture_output=True, check=True)
    return json.loads(result.stdout) if result.stdout.strip() else None


def api_pages(path):
    result = subprocess.run(['gh', 'api', path, '--paginate', '--slurp', '-H',
                             'Accept: application/vnd.github+json'],
                            text=True, capture_output=True, check=True)
    return [item for page in json.loads(result.stdout) for item in page]


def repo_name():
    return os.environ.get('GITHUB_REPOSITORY', 'igrgin/erasure-control-plane')


def branch_name(number, title):
    title = re.sub(r'^\[(?:ERA-\d+|EPIC-\d+)\]\s*', '', title)
    title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode().lower()
    slug = re.sub(r'[^a-z0-9]+', '-', title).strip('-')
    if not slug:
        raise ValueError('Issue title must produce a nonempty branch slug')
    return f'{number}-{slug}'


def completed(issue):
    return issue.get('state') == 'closed' and issue.get('state_reason') == 'completed'


def readiness(number, for_integration=True):
    repo = repo_name()
    issue = api(f'repos/{repo}/issues/{number}')
    if 'pull_request' in issue or issue['state'] != 'open':
        raise ValueError(f'#{number} must be an open issue')
    labels = {label['name'] for label in issue['labels']} & TYPES
    if len(labels) != 1:
        raise ValueError(f'#{number} must have exactly one of bug, spike, implement, epic')
    blockers = api_pages(f'repos/{repo}/issues/{number}/dependencies/blocked_by?per_page=100')
    pending = [f"#{b['number']}" for b in blockers if not completed(b)]
    if pending:
        raise ValueError(f"#{number} awaits completed prerequisites: {', '.join(pending)}")
    if labels == {'epic'} and for_integration:
        actual = api_pages(f'repos/{repo}/issues/{number}/sub_issues?per_page=100')
        pending = [f"#{c['number']}" for c in actual if not completed(c)]
        if pending:
            raise ValueError(f"Epic #{number} integration awaits children: {', '.join(pending)}")
    return issue
