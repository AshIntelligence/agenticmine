"""Instagram Intentional Discovery Prototype
Independent product exercise: relevance + novelty + creator diversity + user-defined time budget. No Instagram affiliation."""
import sys
def rank(user:dict,posts:list[dict],limit=5)->list[dict]:
    seen=set(); out=[]
    for p in posts:
        rel=len(set(user['interests'])&set(p['topics']))/max(1,len(set(user['interests'])|set(p['topics']))); novelty=1-p.get('similarity_to_recent',.5); wellbeing=1-p.get('ragebait',0); creator_bonus=1 if p['creator'] not in seen else .2
        out.append(dict(p,score=round(.45*rel+.20*novelty+.20*wellbeing+.15*creator_bonus,3))); seen.add(p['creator'])
    return sorted(out,key=lambda x:x['score'],reverse=True)[:min(limit,user.get('session_budget_posts',limit))]
def self_test():
    assert len(rank({'interests':['x'],'session_budget_posts':1},[{'id':1,'creator':'a','topics':['x']},{'id':2,'creator':'b','topics':['x']}]))==1
    x=rank({'interests':['x']},[{'id':'good','creator':'a','topics':['x'],'ragebait':0},{'id':'bad','creator':'b','topics':['x'],'ragebait':1}]); assert x[0]['id']=='good'
def demo():
    u={'interests':['travel','food','design'],'session_budget_posts':3}; posts=[{'id':1,'creator':'a','topics':['travel','food'],'similarity_to_recent':.8,'ragebait':0},{'id':2,'creator':'b','topics':['design'],'similarity_to_recent':.2,'ragebait':0},{'id':3,'creator':'c','topics':['celebrity'],'similarity_to_recent':.1,'ragebait':.8}]; print(rank(u,posts))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
