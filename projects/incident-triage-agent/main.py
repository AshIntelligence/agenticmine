"""Incident Triage Agent
Deterministic first-pass severity, owner and next-action routing before any generative summary."""
import sys
KEYWORDS={'billing':'commerce','invoice':'commerce','latency':'platform','timeout':'platform','login':'identity','auth':'identity','fraud':'risk','chargeback':'risk'}
def triage(title:str,error_rate:float,affected_pct:float,revenue_path:bool=False)->dict:
    text=title.lower(); scores={}
    for k,owner in KEYWORDS.items():
        if k in text: scores[owner]=scores.get(owner,0)+1
    owner=max(scores,key=scores.get) if scores else 'platform'; s=.45*min(error_rate/.10,1)+.35*min(affected_pct/.50,1)+(.20 if revenue_path else 0)
    sev='SEV0' if s>=.85 else 'SEV1' if s>=.55 else 'SEV2'; action='freeze-deploys' if sev in {'SEV0','SEV1'} else 'collect-diagnostics'
    return {'severity':sev,'owner':owner,'next_action':action,'score':round(s,3),'matched_terms':[k for k in KEYWORDS if k in text]}
def self_test():
    assert triage('invoice failure',.01,.02)['owner']=='commerce'; assert triage('billing down',.1,.5,True)['severity'] in {'SEV0','SEV1'}
def demo(): print(triage('Invoice callback timeout spike',.08,.35,True))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
