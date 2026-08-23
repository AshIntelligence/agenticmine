"""Grounded RAG Quality Gate

Evaluates evidence coverage, citation validity and contradictions before an answer can ship. Failing the gate routes to review instead of hallucinating harder.
"""
import re, sys
from dataclasses import dataclass
@dataclass(frozen=True)
class GateResult:
    coverage:float; citation_precision:float; contradiction_penalty:float; score:float; status:str

def tokens(text): return {x.lower() for x in re.findall(r"[a-zA-Z0-9]+",text) if len(x)>2}
def evaluate(question:str,answer:str,evidence:list[str],citations:list[int],contradictions:int=0)->GateResult:
    q=tokens(question); a=tokens(answer); ev=set().union(*(tokens(e) for e in evidence)) if evidence else set()
    coverage=len((q|a)&ev)/max(1,len(q|a)); valid=sum(1 for c in citations if 0<=c<len(evidence)); precision=valid/max(1,len(citations))
    penalty=min(.4,contradictions*.12); score=.65*coverage+.35*precision-penalty
    status="PASS" if score>=.68 and coverage>=.55 else "REVIEW"
    return GateResult(round(coverage,3),round(precision,3),penalty,round(score,3),status)

def self_test():
    assert evaluate("approval gate","approval gate",["approval gate"],[0]).status=="PASS"
    assert evaluate("x","unsupported claim",[],[]).status=="REVIEW"

def demo():
    q="What controls protect agent tool use?"; a="Tool calls use allowlists, human approval and audit traces."
    ev=["Agent tool use is constrained by allowlists and approval gates.","Audit traces record each tool call."]
    print(evaluate(q,a,ev,[0,1]))
if __name__=="__main__": self_test() if "--test" in sys.argv else demo()
