"""Career Discovery Ranking Study
Personal ranking study using LinkedIn career discovery as the surface. Unaffiliated with LinkedIn."""
import sys
def jaccard(a,b):
    a=set(x.lower() for x in a); b=set(x.lower() for x in b); return len(a&b)/max(1,len(a|b))
def rank(profile:dict,jobs:list[dict])->list[dict]:
    out=[]
    for j in jobs:
        fit=jaccard(profile['skills'],j['skills']); growth=jaccard(profile['learn_next'],j.get('skills',[])); fresh=max(0,1-j.get('days_old',0)/30); location=1 if j.get('location') in profile['locations'] else .35
        score=.48*fit+.20*growth+.18*fresh+.14*location
        out.append(dict(j,score=round(score,3),why={'skill_fit':round(fit,2),'growth':round(growth,2),'freshness':round(fresh,2),'location':location}))
    return sorted(out,key=lambda x:x['score'],reverse=True)
def self_test():
    p={'skills':['ai','platform'],'learn_next':['agents'],'locations':['Seattle']}; jobs=[{'title':'fit','skills':['ai','platform','agents'],'location':'Seattle','days_old':10},{'title':'fresh','skills':['sales'],'location':'Seattle','days_old':0}]; assert rank(p,jobs)[0]['title']=='fit'
def demo():
    p={'skills':['product','ai','platform','payments'],'learn_next':['agents','evals'],'locations':['Seattle','Bay Area']}; jobs=[{'title':'AI Platform PM','skills':['product','ai','platform','agents','evals'],'location':'Bay Area','days_old':3},{'title':'Growth PM','skills':['growth','ads'],'location':'Seattle','days_old':1}]; print(rank(p,jobs))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
