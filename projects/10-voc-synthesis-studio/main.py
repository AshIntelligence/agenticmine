"""Voice of Customer Synthesis Studio
Combines qualitative comments with usage evidence so loud anecdotes do not automatically become roadmap priority."""
import re,sys
from collections import defaultdict
POS={'love','fast','easy','helpful','great','clear'}; NEG={'slow','hard','broken','confusing','hate','missing','manual'}
THEMES={'search':['search','find','discover'],'onboarding':['setup','onboarding','start'],'automation':['manual','automate','workflow'],'trust':['wrong','trust','accurate','confusing']}
def synthesize(comments:list[str],telemetry:dict[str,float])->list[dict]:
    agg=defaultdict(lambda:{'mentions':0,'sentiment':0})
    for c in comments:
        words=set(re.findall(r'[a-z]+',c.lower())); sent=len(words&POS)-len(words&NEG)
        for theme,keys in THEMES.items():
            if words&set(keys): agg[theme]['mentions']+=1; agg[theme]['sentiment']+=sent
    out=[]
    for theme,x in agg.items():
        usage=float(telemetry.get(theme,0)); pain=max(0,-x['sentiment']); score=.5*x['mentions']+.25*pain+.25*usage*10
        out.append({'theme':theme,'mentions':x['mentions'],'sentiment':x['sentiment'],'usage_signal':usage,'priority':round(score,2)})
    return sorted(out,key=lambda x:x['priority'],reverse=True)
def self_test(): assert synthesize(['search is confusing','manual workflow'],{'search':.9,'automation':.1})[0]['theme']=='search'
def demo(): print(synthesize(['Search is confusing and I cannot find the right report','Too much manual workflow setup','Search is fast when it works'],{'search':.8,'automation':.6}))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
