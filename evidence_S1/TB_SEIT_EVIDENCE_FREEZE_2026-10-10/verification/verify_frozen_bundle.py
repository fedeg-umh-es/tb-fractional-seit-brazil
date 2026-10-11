"""Portable read-only freeze verifier. Standard library only; no scientific execution."""
from pathlib import Path
import csv
import hashlib
import json
import sys

root=Path(sys.argv[1]).resolve()
manifest=json.loads((root/'artifact_manifest.json').read_text())
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==set(manifest)|{'artifact_manifest.json'}, 'Incomplete or extra files'
for name,digest in manifest.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest, 'Hash discrepancy: '+name
rows=list(csv.DictReader((root/'phase2/rolling_origin_predictions.csv').open()))
assert len(rows)==780
models={'fractional','integer','persistence','seasonal_naive_12','SARIMA'}
assert {r['model'] for r in rows}==models
support={model:{(r['origin'],r['target_date'],r['horizon']) for r in rows if r['model']==model} for model in models}
assert all(len(s)==156 for s in support.values())
assert all(s==next(iter(support.values())) for s in support.values())
checks=list(csv.DictReader((root/'verification/freeze_checks.csv').open()))
assert all(r['status']=='PASS' for r in checks)
summary=json.loads((root/'FREEZE_SUMMARY.json').read_text())
assert len(checks)==summary['checks'] and summary['verdict']=='EVIDENCE_FREEZE_PASS'
claims=list(csv.DictReader((root/'CLAIM_EVIDENCE_MATRIX.csv').open()))
assert len(claims)==summary['claims']
for r in claims:
    for column in ['tables','calculation_sources','protocols']:
        assert all((root/p).is_file() for p in json.loads(r[column]))
assert summary['new_optimizations']==summary['new_solver_simulations']==summary['new_scientific_experiments']==0
print(json.dumps({'status':'PASS','payload_files':len(manifest),'predictions':780,'pairs_per_model':156,'claims':len(claims),'freeze_checks':len(checks),'scientific_executions':0},indent=2))
