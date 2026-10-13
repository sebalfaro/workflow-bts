"""Verify every allowlisted public payload file; mismatch terminates with exit 1."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "MANIFIESTO-SHA256.json").read_text())
errors = []
for relative, expected in manifest.items():
    path = root / relative
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        errors.append(relative)
actual = {str(p.relative_to(root)) for p in root.rglob("*")
          if p.is_file() and not any(x in p.relative_to(root).parts
                                    for x in (".git", "__pycache__"))
          and p.name != "MANIFIESTO-SHA256.json"}
errors.extend(sorted(actual - set(manifest)))
if errors:
    print("HASH_MISMATCH / UNLISTED_FILE:", ", ".join(errors))
    sys.exit(1)
print(f"Verified {len(manifest)} files")
