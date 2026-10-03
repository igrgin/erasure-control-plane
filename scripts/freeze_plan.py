#!/usr/bin/env python3
"""Bind the current planning/governance files without altering accepted intent."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'planning/candidate.json'
previous = json.loads(path.read_text()) if path.exists() else {}
names = {'.gitignore', 'README.md', 'CONTEXT.md', 'AGENTS.md'}
names.update(str(p.relative_to(ROOT)) for base in ('docs', 'planning', 'scripts', '.github')
             for p in (ROOT / base).rglob('*') if p.is_file()
             and p.name != 'candidate.json' and '__pycache__' not in p.parts)
files = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sorted(names)}
digest = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
accepted = json.loads((ROOT / 'planning/accepted-plan.json').read_text())['digest']
candidate = {'version': 4, 'kind': 'planning-and-repository-preparation',
             'status': 'accepted product plan; repository preparation authorized in this conversation',
             'accepted_plan_digest': accepted,
             'supersedes': previous.get('supersedes') if previous.get('digest') == digest else previous.get('digest'),
             'digest': digest, 'files': files}
path.write_text(json.dumps(candidate, indent=2) + '\n')
print(f'Candidate: {digest}')
