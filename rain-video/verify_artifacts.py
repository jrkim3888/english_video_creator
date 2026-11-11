"""Verify the committed example files using only the Python standard library."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'artifact-manifest.json').read_text(encoding='utf-8'))
errors = []
for entry in manifest['files']:
    path = root / entry['path']
    if not path.is_file():
        errors.append(f"Missing: {entry['path']}")
        continue
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    if path.stat().st_size != entry['bytes'] or digest.hexdigest() != entry['sha256']:
        errors.append(f"Changed: {entry['path']}")
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f"Verified {len(manifest['files'])} example files.")
