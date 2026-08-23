"""Customer Support Knowledge OS
Deterministic intent/retrieval confidence gate: answer with a source or escalate."""
import re,sys
def overlap(a,b):
    norm=lambda x:x[:-1] if len(x)>4 and x.endswith('s') else x
    ta={norm(x) for x in re.findall(r'[a-z]+',a.lower())}; tb={norm(x) for x in re.findall(r'[a-z]+',b.lower())}; return len(ta&tb)/max(1,len(ta|tb))
def answer(query:str,articles:list[dict],threshold=.18)->dict:
    ranked=sorted(((overlap(query,a['text']),a) for a in articles),key=lambda x:x[0],reverse=True); score,article=ranked[0] if ranked else (0,None)
    if not article or score<threshold: return {'status':'ESCALATE','confidence':round(score,3),'sources':[]}
    return {'status':'ANSWER','confidence':round(score,3),'answer':article['text'],'sources':[article['id']]}
def self_test():
    assert answer('refund days',[{'id':'x','text':'refund days are five'}])['status']=='ANSWER'; assert answer('orbital mechanics',[{'id':'x','text':'refund policy'}])['status']=='ESCALATE'
def demo():
    kb=[{'id':'refunds','text':'Approved refund arrives in five to seven business days.'},{'id':'password','text':'Use account recovery to reset a forgotten password.'}]; print('known:',answer('approved refund business days',kb)); print('unknown:',answer('How do I export orbital telemetry?',kb))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
