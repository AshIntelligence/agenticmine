"""Run demos + self-tests for every numbered showcase project."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
PROJECTS=sorted((ROOT/'projects').glob('[0-9][0-9]-*'))
failed=[]
for p in PROJECTS:
    print(f'\n=== {p.name} ===')
    demo=subprocess.run([sys.executable,str(p/'main.py')],capture_output=True,text=True)
    print(demo.stdout.strip())
    test=subprocess.run([sys.executable,str(p/'main.py'),'--test'],capture_output=True,text=True)
    status='PASS' if demo.returncode==0 and test.returncode==0 else 'FAIL'
    print(f'self-test: {status}')
    if status=='FAIL':
        if demo.stderr: print(demo.stderr)
        if test.stderr: print(test.stderr)
        failed.append(p.name)
print(f'\n{len(PROJECTS)-len(failed)}/{len(PROJECTS)} projects passed demo + self-test')
raise SystemExit(1 if failed else 0)
