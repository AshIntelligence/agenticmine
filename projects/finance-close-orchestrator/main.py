"""Multi-Agent Finance Close Orchestrator

Dependency-aware synthetic close workflow across AP, AR, Treasury, reconciliation, GL and a human controller checkpoint.
"""
from dataclasses import dataclass
import sys
@dataclass
class Task:
    name:str; deps:tuple; owner:str; critical:bool=False
TASKS=[Task("ap-close",(),"APAgent"),Task("ar-close",(),"ARAgent"),Task("cash-position",(),"TreasuryAgent"),Task("reconcile",("ap-close","ar-close","cash-position"),"ReconcileAgent",True),Task("gl-close",("reconcile",),"GLAgent",True),Task("controller-approval",("gl-close",),"HumanController",True)]

def plan(completed:set,exceptions:dict|None=None)->list[dict]:
    exceptions=exceptions or {}; out=[]
    for t in TASKS:
        if t.name in completed: continue
        blocked=[d for d in t.deps if d not in completed]
        status="exception" if t.name in exceptions else "ready" if not blocked else "blocked"
        out.append({"task":t.name,"owner":t.owner,"status":status,"blocked_by":blocked,"critical":t.critical,"exception":exceptions.get(t.name)})
    return out

def self_test():
    assert plan({"ap-close","ar-close","cash-position"})[0]["status"]=="ready"
    assert any(x["task"]=="gl-close" and x["status"]=="blocked" for x in plan(set()))

def demo():
    for row in plan({"ap-close","ar-close","cash-position"},{"reconcile":"cash mismatch > tolerance"}): print(row)
if __name__=="__main__": self_test() if "--test" in sys.argv else demo()
