"""Run the local demo and self-check for each system in projects/."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
PROJECTS=sorted(p.parent for p in (ROOT/'projects').glob('*/main.py'))
failed=[]

for project in PROJECTS:
    print(f'\n=== {project.name} ===')
    for args in ([sys.executable,str(project/'main.py')],[sys.executable,str(project/'main.py'),'--test']):
        result=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
        if result.stdout.strip(): print(result.stdout.strip())
        if result.returncode:
            failed.append(project.name)
            if result.stderr.strip(): print(result.stderr.strip(),file=sys.stderr)
            break

if failed:
    print('\nFailed: '+', '.join(sorted(set(failed))))
    raise SystemExit(1)
print('\nLab checks passed')
