"""Fraud Signal Decision Engine
Explainable synthetic risk scoring with ALLOW / REVIEW / BLOCK states."""
import sys
WEIGHTS={'velocity':.22,'device_novelty':.15,'payment_mismatch':.20,'identity_risk':.24,'behavior_anomaly':.19}
def decide(signals:dict)->dict:
    score=sum(max(0,min(1,float(signals.get(k,0))))*w for k,w in WEIGHTS.items())
    action='BLOCK' if score>=.72 else 'REVIEW' if score>=.43 else 'ALLOW'
    top=sorted(((k,signals.get(k,0)*w) for k,w in WEIGHTS.items()),key=lambda x:x[1],reverse=True)[:3]
    return {'score':round(score,3),'action':action,'top_contributors':[k for k,_ in top]}
def self_test():
    assert decide({k:1 for k in WEIGHTS})['action']=='BLOCK'; assert decide({})['action']=='ALLOW'
def demo():
    for s in [{'velocity':.9,'identity_risk':.8,'payment_mismatch':.7},{'velocity':.1,'identity_risk':.1}]: print(decide(s))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
