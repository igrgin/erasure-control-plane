#!/usr/bin/env python3
"""Idempotent, explicitly invoked GitHub backlog publication and verification."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import time
from urllib.parse import quote
from github_policy import api, api_pages, branch_name

ROOT = Path(__file__).resolve().parents[1]
REPO = 'igrgin/erasure-control-plane'
PREFIX = f'repos/{REPO}'
MAP = ROOT / 'planning/github-map.json'


def write_api(path, data, method='POST'):
    result = api(path, data, method)
    time.sleep(1.1)
    return result


def save(mapping):
    temp = MAP.with_suffix('.json.tmp')
    temp.write_text(json.dumps(mapping, indent=2) + '\n')
    temp.replace(MAP)


def rendered_body(record, items):
    path = ROOT / record['body_file']
    body = path.read_text().replace('Status: proposed.', 'Status: open; implementation pending.')

    def replace_link(match):
        label, target = match.groups()
        ident = re.search(r'(ERA-\d+|EPIC-\d+)\.md$', target)
        if ident and ident.group(1) in items:
            return f"[{label}]({items[ident.group(1)]['url']})"
        if target.startswith(('https://', 'http://', '#')):
            return match.group(0)
        target_path = (path.parent / target).resolve().relative_to(ROOT)
        return f'[{label}](https://github.com/{REPO}/blob/main/{quote(str(target_path))})'

    body = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', replace_link, body)
    branch = items[record['id']]['branch']
    blockers = items[record['id']]['blockers']
    links = ', '.join(f"#{items[d]['number']}" for d in blockers) or 'None'
    body += f'\n## GitHub delivery\n\nPlan ID: `{record["id"]}`. Dedicated branch: `{branch}`.\n\nEffective start/implementation blockers: {links}. Prerequisites must close as completed; discarded work does not authorize dependent implementation.\n'
    if record['id'].startswith('ERA-'):
        body += f"\nParent epic: #{items[record['epic']]['number']}.\n"
    return body


def publish(data):
    existing = api_pages(f'{PREFIX}/issues?state=all&per_page=100')
    epics = {e['id']: e for e in data['epics']}
    records = data['epics'] + data['issues']
    mapping = json.loads(MAP.read_text()) if MAP.exists() else {'version': 1, 'repo': REPO, 'setup_issue': {'number': 1, 'url': f'https://github.com/{REPO}/issues/1'}, 'items': {}}
    if mapping['repo'] != REPO:
        raise ValueError('Repository mapping mismatch')
    # This is a newly created repository. Retain only the four user-requested type labels.
    definitions = {'bug': ('d73a4a', 'Incorrect behavior'), 'spike': ('d4c5f9', 'Bounded investigation and decision'), 'implement': ('0e8a16', 'Regular implementation work'), 'epic': ('5319e7', 'Coupled issues forming an application capability')}
    labels = {label['name'] for label in api_pages(f'{PREFIX}/labels?per_page=100')}
    for name, (color, description) in definitions.items():
        write_api(f'{PREFIX}/labels/{quote(name)}' if name in labels else f'{PREFIX}/labels', {'name': name, 'color': color, 'description': description}, 'PATCH' if name in labels else 'POST')
    for name in sorted(labels - definitions.keys()):
        write_api(f'{PREFIX}/labels/{quote(name, safe="")}', None, 'DELETE')
    milestones = api_pages(f'{PREFIX}/milestones?state=all&per_page=100')
    milestone = next((m for m in milestones if m['title'] == data['release']), None)
    if milestone is None:
        milestone = write_api(f'{PREFIX}/milestones', {'title': data['release'], 'description': 'Complete synthetic end-to-end architecture, deployment, scale evidence, and public demonstration.'})
    mapping['milestone'] = {'number': milestone['number'], 'url': milestone['html_url']}
    for n, record in enumerate(records, 1):
        ident = record['id']
        found = [i for i in existing if 'pull_request' not in i and i['title'].startswith(f'[{ident}] ')]
        if len(found) > 1:
            raise ValueError(f'Duplicate published plan ID: {ident}')
        issue = found[0] if found else write_api(f'{PREFIX}/issues', {'title': f"[{ident}] {record['title']}", 'body': (ROOT / record['body_file']).read_text(), 'labels': record['labels'], 'milestone': milestone['number']})
        blockers = set(record.get('depends_on', [])) | set(record.get('depends_on_epics', [])) | set(record.get('entry_issue_dependencies', []))
        if ident.startswith('ERA-'):
            epic = epics[record['epic']]
            blockers |= set(epic['depends_on_epics']) | set(epic['entry_issue_dependencies'])
        mapping['items'][ident] = {'number': issue['number'], 'id': issue['id'], 'node_id': issue['node_id'], 'url': issue['html_url'], 'branch': branch_name(issue['number'], issue['title']), 'blockers': sorted(blockers)}
        save(mapping)
        if n % 10 == 0 or n == len(records):
            print(f'Published records: {n}/{len(records)}', flush=True)
    for n, record in enumerate(records, 1):
        write_api(f"{PREFIX}/issues/{mapping['items'][record['id']]['number']}", {'body': rendered_body(record, mapping['items']), 'labels': record['labels'], 'milestone': milestone['number']}, 'PATCH')
        if n % 10 == 0 or n == len(records):
            print(f'Linked issue bodies: {n}/{len(records)}', flush=True)
    for n, record in enumerate(data['issues'], 1):
        child = mapping['items'][record['id']]
        parent = mapping['items'][record['epic']]
        current = api(f"{PREFIX}/issues/{parent['number']}/sub_issues?per_page=100")
        if child['id'] not in {c['id'] for c in current}:
            query = 'mutation($parent:ID!,$child:ID!){addSubIssue(input:{issueId:$parent,subIssueId:$child}){__typename}}'
            result = write_api('graphql', {'query': query, 'variables': {'parent': parent['node_id'], 'child': child['node_id']}})
            if result.get('errors'):
                raise ValueError(result['errors'])
        if n % 10 == 0 or n == len(data['issues']):
            print(f'Native child links: {n}/{len(data["issues"])}', flush=True)
    added = 0
    for record in records:
        item = mapping['items'][record['id']]
        current = api(f"{PREFIX}/issues/{item['number']}/dependencies/blocked_by?per_page=100")
        present = {d['id'] for d in current}
        for ident in item['blockers']:
            blocker = mapping['items'][ident]
            if blocker['id'] not in present:
                write_api(f"{PREFIX}/issues/{item['number']}/dependencies/blocked_by", {'issue_id': blocker['id']})
                added += 1
                if added % 20 == 0:
                    print(f'Native blocker links added: {added}', flush=True)
    mapping['publication_status'] = 'published with native sub-issues and issue dependencies'
    save(mapping)
    print(f'Publication complete: {len(records)} records; {added} new blockers', flush=True)


def verify(data):
    mapping = json.loads(MAP.read_text())
    records = data['epics'] + data['issues']
    remote = {i['number']: i for i in api_pages(f'{PREFIX}/issues?state=all&per_page=100') if 'pull_request' not in i}
    count = 0
    for record in records:
        item = mapping['items'][record['id']]
        actual = remote[item['number']]
        assert actual['title'] == f"[{record['id']}] {record['title']}", 'Title mismatch'
        assert {x['name'] for x in actual['labels']} == set(record['labels']), 'Label mismatch'
        assert actual['body'] == rendered_body(record, mapping['items']), 'Body mismatch'
        assert actual['milestone']['number'] == mapping['milestone']['number'], 'Milestone mismatch'
        blockers = api(f"{PREFIX}/issues/{item['number']}/dependencies/blocked_by?per_page=100")
        assert {b['id'] for b in blockers} == {mapping['items'][ident]['id'] for ident in item['blockers']}, 'Blocker mismatch'
        count += len(blockers)
    for epic in data['epics']:
        parent = mapping['items'][epic['id']]
        children = api(f"{PREFIX}/issues/{parent['number']}/sub_issues?per_page=100")
        assert {c['id'] for c in children} == {mapping['items'][ident]['id'] for ident in epic['issues']}, 'Parent mismatch'
    print(f'PASS: {len(data["epics"])} native epics, {len(data["issues"])} sub-issues, {count} blocker links; bodies, labels, and milestone verified.', flush=True)


def branches(data):
    mapping = json.loads(MAP.read_text())
    base = api(f'{PREFIX}/git/ref/heads/main')['object']['sha']
    existing = {b['name'] for b in api_pages(f'{PREFIX}/branches?per_page=100')}
    for n, record in enumerate(data['epics'] + data['issues'], 1):
        branch = mapping['items'][record['id']]['branch']
        if branch not in existing:
            write_api(f'{PREFIX}/git/refs', {'ref': f'refs/heads/{branch}', 'sha': base})
        if n % 10 == 0 or n == 52:
            print(f'Issue branches: {n}/52', flush=True)
    print(f'Branches created/reused from main {base}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['publish', 'verify', 'branches'])
    args = parser.parse_args()
    data = json.loads((ROOT / 'planning/issues.json').read_text())
    {'publish': publish, 'verify': verify, 'branches': branches}[args.action](data)
