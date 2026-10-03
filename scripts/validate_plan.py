#!/usr/bin/env python3
"""Validate epic/issue planning and candidate hashes without external calls."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assert_acyclic(graph):
    visiting, visited = set(), set()

    def visit(node):
        assert node in graph, f'unknown dependency: {node}'
        assert node not in visiting, f'dependency cycle at {node}'
        if node in visited:
            return
        visiting.add(node)
        for dep in graph[node]:
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def ready_issues(data, accepted_issues, accepted_epics):
    epics = {e['id']: e for e in data['epics']}
    result = set()
    for issue in data['issues']:
        epic = epics[issue['epic']]
        if (issue['id'] not in accepted_issues
                and set(epic['depends_on_epics']) <= accepted_epics
                and set(epic['entry_issue_dependencies']) <= accepted_issues
                and set(issue['depends_on']) <= accepted_issues):
            result.add(issue['id'])
    return result


def validate():
    data = json.loads((ROOT / 'planning/issues.json').read_text())
    issues, epics = data['issues'], data['epics']
    ids = [i['id'] for i in issues]
    epic_ids = [e['id'] for e in epics]
    assert data['version'] == 3, 'expected demo manifest version 3'
    assert len(ids) == len(set(ids)) == 42, 'expected 42 unique child issues'
    assert len(epic_ids) == len(set(epic_ids)) == 10, 'expected ten unique epics'
    byid = {i['id']: i for i in issues}
    byepic = {e['id']: e for e in epics}
    mapped = []
    for epic in epics:
        eid = epic['id']
        assert re.fullmatch(r'EPIC-\d{2}', eid), f'invalid epic ID {eid}'
        assert len(epic['issues']) >= 2, f'incomplete epic {eid}'
        body = (ROOT / epic['body_file']).read_text()
        assert body.startswith(f"# {eid}: {epic['title']}"), f'epic title mismatch {eid}'
        assert epic['labels'] == ['epic'], f'missing epic label {eid}'
        for section in ['## Application capability', '## Why these issues belong together', '## Start prerequisites and external blockers', '## Coupled child issues', '## Integration boundaries', '## Epic acceptance']:
            assert section in body, f'missing {section} in {eid}'
        for ident in epic['issues']:
            assert ident in byid and byid[ident]['epic'] == eid, f'child mismatch {eid}: {ident}'
            assert f'[{ident}: ' in body, f'child absent from epic body {ident}'
            mapped.append(ident)
        for dep in epic['depends_on_epics']:
            assert dep in byepic and dep != eid, f'invalid epic dependency {eid}: {dep}'
            assert f'[{dep}]({dep}.md)' in body, f'missing epic dependency link {eid}'
        for dep in epic['entry_issue_dependencies']:
            assert dep in byid and byid[dep]['epic'] != eid, f'invalid entry dependency {eid}: {dep}'
            assert f'[{dep}](../issues/{dep}.md)' in body, f'missing entry issue link {eid}'
        external = {dep for ident in epic['issues'] for dep in byid[ident]['depends_on'] if dep not in epic['issues']}
        assert set(epic['external_issue_dependencies']) == external, f'external dependency mismatch {eid}'
        for dep in external:
            assert f'[{dep}](../issues/{dep}.md)' in body, f'missing external issue link {eid}: {dep}'
    assert sorted(mapped) == sorted(ids), 'issues must belong to exactly one epic'
    assert_acyclic({e['id']: e['depends_on_epics'] for e in epics})
    requirements = {f'REQ-{n:02d}' for n in range(1, 16)}
    covered = set()
    for issue in issues:
        ident = issue['id']
        assert re.fullmatch(r'ERA-\d{3}', ident), f'invalid ID {ident}'
        path = ROOT / issue['body_file']
        assert path.is_relative_to(ROOT) and path.is_file(), f'missing issue {ident}'
        body = path.read_text()
        assert body.startswith(f"# {ident}: {issue['title']}"), f'title mismatch {ident}'
        assert f"Epic: [{issue['epic']}](../epics/{issue['epic']}.md)." in body, f'parent link missing {ident}'
        assert len(issue["labels"]) == 1 and issue["labels"][0] in {"bug", "spike", "implement"}, f"invalid issue type {ident}"
        for section in ['## Outcome', '## Requirements and dependencies', '## Intended implementation ownership', '## Acceptance criteria', '## Verification']:
            assert section in body, f'missing {section} in {ident}'
        assert body.count('- [ ] ') >= 3, f'insufficient acceptance criteria {ident}'
        assert issue['requirements'] and set(issue['requirements']) <= requirements, f'invalid requirements {ident}'
        covered.update(issue['requirements'])
        for req in issue['requirements']:
            assert req in body, f'requirement absent from body {ident}: {req}'
        for dep in issue['depends_on']:
            assert dep in byid and dep != ident, f'unknown/self dependency {ident}: {dep}'
            assert f'[{dep}]({dep}.md)' in body, f'dependency absent from body {ident}: {dep}'
    # Expand epic start gates into issue prerequisites to catch cross-level deadlocks.
    expanded = {}
    for issue in issues:
        epic = byepic[issue['epic']]
        prereqs = set(issue['depends_on']) | set(epic['entry_issue_dependencies'])
        for required_epic in epic['depends_on_epics']:
            prereqs.update(byepic[required_epic]['issues'])
        expanded[issue['id']] = prereqs
    assert_acyclic(expanded)
    # Verify the concurrent scheduling examples, without claiming actual owner acceptance.
    assert ready_issues(data, set(), set()) == {'ERA-037'}, 'demo blueprint must be the initial ready issue'
    assert ready_issues(data, {'ERA-037'}, set()) == {'ERA-001', 'ERA-038', 'ERA-041'}, 'demo setup/research and foundation must overlap'
    baseline = {f'ERA-{n:03d}' for n in range(1, 5)} | {'ERA-037'}
    accepted_epics = {'EPIC-01'}
    expected = {'ERA-005', 'ERA-017', 'ERA-021', 'ERA-025', 'ERA-029', 'ERA-038', 'ERA-041'}
    assert ready_issues(data, baseline, accepted_epics) == expected, 'foundation readiness example is stale'
    assert ready_issues(data, baseline, set()) == {'ERA-038', 'ERA-041'}, 'foundation acceptance gates must not block independent demo work'
    assert 'ERA-013' in ready_issues(data, baseline | {'ERA-005'}, accepted_epics), 'owner epic is unnecessarily blocked'
    assert 'ERA-009' in ready_issues(data, baseline | {'ERA-005', 'ERA-006'}, accepted_epics), 'request scoping is unnecessarily blocked'
    assert 'ERA-011' not in ready_issues(data, baseline | {'ERA-005', 'ERA-006'}, accepted_epics), 'MongoDB fixture prerequisite is missing'
    assert 'ERA-011' in ready_issues(data, baseline | {'ERA-005', 'ERA-006', 'ERA-038'}, accepted_epics), 'MongoDB adapter is unnecessarily blocked'
    assert 'ERA-033' in ready_issues(data, baseline | {'ERA-005', 'ERA-006', 'ERA-007'}, accepted_epics), 'scale preparation is unnecessarily blocked'
    assert 'ERA-032' not in ready_issues(data, baseline, accepted_epics), 'release integration barrier is missing'
    assert 'ERA-042' not in ready_issues(data, baseline, accepted_epics), 'public-launch integration barrier is missing'
    assert 'ERA-040' in byid['ERA-032']['depends_on'], 'three-source UAT barrier is missing'
    assert 'ERA-042' in byid['ERA-036']['depends_on'], 'public-demo handoff barrier is missing'
    assert covered == requirements, f'uncovered requirements {requirements - covered}'
    spec = (ROOT / 'docs/specification.md').read_text()
    for req in requirements:
        assert f'| {req} |' in spec, f'missing requirement definition {req}'
    markdown = [ROOT / 'README.md', ROOT / 'CONTEXT.md', ROOT / 'AGENTS.md', *sorted((ROOT / 'docs').rglob('*.md')), *sorted((ROOT / 'planning').rglob('*.md'))]
    for path in markdown:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            if target.startswith(('https://', 'http://', '#')):
                continue
            target = target.split('#', 1)[0]
            assert (path.parent / target).resolve().exists(), f'broken link {path}: {target}'
    candidate = json.loads((ROOT / 'planning/candidate.json').read_text())
    actual_files = {'.gitignore', 'README.md', 'CONTEXT.md', 'AGENTS.md'}
    actual_files.update(str(p.relative_to(ROOT)) for base in ('docs', 'planning', 'scripts', '.github') for p in (ROOT / base).rglob('*') if p.is_file() and p.name != 'candidate.json' and '__pycache__' not in p.parts)
    assert set(candidate['files']) == actual_files, 'candidate inventory omits or retains an artifact'
    for name, expected_hash in candidate['files'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected_hash, f'candidate file changed: {name}'
    encoded = json.dumps(candidate['files'], sort_keys=True, separators=(',', ':')).encode()
    assert hashlib.sha256(encoded).hexdigest() == candidate['digest'], 'candidate digest mismatch'
    print(f'PASS: {len(epics)} epics, {len(issues)} child issues, {len(covered)} requirements; graphs, readiness examples, links, and candidate hashes valid.')


if __name__ == '__main__':
    validate()
