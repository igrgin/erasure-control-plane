#!/usr/bin/env python3
"""Check live issue readiness and publish PR policy statuses using trusted code."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
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


def expected_blockers(number):
    manifest = json.loads((ROOT / 'planning/issues.json').read_text())
    record = json.loads((ROOT / 'planning/github-map.json').read_text())
    if record['repo'] != repo_name():
        raise ValueError('Published mapping belongs to another repository')
    mapping = record['items']
    ident = next((key for key, val in mapping.items() if val['number'] == number), None)
    if ident is None:
        return set(), []
    epics = {e['id']: e for e in manifest['epics']}
    if ident in epics:
        epic = epics[ident]
        blockers = set(epic['depends_on_epics']) | set(epic['entry_issue_dependencies'])
        children = epic['issues']
    else:
        issue = next(i for i in manifest['issues'] if i['id'] == ident)
        epic = epics[issue['epic']]
        blockers = set(issue['depends_on']) | set(epic['depends_on_epics']) | set(epic['entry_issue_dependencies'])
        children = []
    return {mapping[key]['id'] for key in blockers}, [mapping[key]['id'] for key in children]


def readiness(number, for_integration=True):
    repo = repo_name()
    issue = api(f'repos/{repo}/issues/{number}')
    if 'pull_request' in issue or issue['state'] != 'open':
        raise ValueError(f'#{number} must be an open issue')
    labels = {label['name'] for label in issue['labels']} & TYPES
    if len(labels) != 1:
        raise ValueError(f'#{number} must have exactly one of bug, spike, implement, epic')
    blockers = api(f'repos/{repo}/issues/{number}/dependencies/blocked_by?per_page=100')
    expected, children = expected_blockers(number)
    if not expected <= {b['id'] for b in blockers}:
        raise ValueError(f'#{number} is missing planned native dependency links')
    pending = [f"#{b['number']}" for b in blockers if not completed(b)]
    if pending:
        raise ValueError(f"#{number} awaits completed prerequisites: {', '.join(pending)}")
    if labels == {'epic'} and for_integration:
        actual = api(f'repos/{repo}/issues/{number}/sub_issues?per_page=100')
        if not set(children) <= {c['id'] for c in actual}:
            raise ValueError(f'#{number} is missing planned sub-issues')
        pending = [f"#{c['number']}" for c in actual if not completed(c)]
        if pending:
            raise ValueError(f"Epic #{number} integration awaits children: {', '.join(pending)}")
    return issue


def check_pr(pr):
    repo = repo_name()
    refs = re.findall(r'\b(?:close[sd]?|fix(?:es|ed)?|resolve[sd]?)\s+(?:#|https://github\.com/'
                      + re.escape(repo) + r'/issues/)(\d+)\b', pr.get('body') or '', re.I)
    refs = {int(ref) for ref in refs}
    if len(refs) != 1:
        raise ValueError('PR must close exactly one same-repository issue, e.g. Closes #48')
    number = next(iter(refs))
    issue = readiness(number)
    expected = branch_name(number, issue['title'])
    if pr['head']['ref'] != expected:
        raise ValueError(f'Use the issue branch: {expected}')
    if pr['base']['ref'] != 'main':
        raise ValueError('Default PR base is main; explicit exceptions require a policy revision')
    return f'Issue #{number}, branch, type, and prerequisites are valid'


def refresh(pr_number=None):
    repo = repo_name()
    prs = [api(f'repos/{repo}/pulls/{pr_number}')] if pr_number else api_pages(f'repos/{repo}/pulls?state=open&per_page=100')
    failed = False
    for pr in prs:
        if pr['state'] != 'open':
            continue
        try:
            detail = check_pr(pr)
            state = 'success'
        except (ValueError, subprocess.CalledProcessError, KeyError) as error:
            detail = str(error)
            state = 'failure'
            failed = True
        api(f"repos/{repo}/statuses/{pr['head']['sha']}", {
            'state': state, 'context': 'issue-policy', 'description': detail[:140],
            'target_url': pr['html_url']})
        print(f"PR #{pr['number']}: {state}: {detail}", flush=True)
    return not failed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr', type=int)
    args = parser.parse_args()
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    event = json.loads(Path(event_path).read_text()) if event_path else {}
    pr_number = args.pr or (event.get('pull_request') or {}).get('number')
    raise SystemExit(0 if refresh(pr_number) else 1)
