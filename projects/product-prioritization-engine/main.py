"""Evidence-Weighted Product Prioritization Engine
Ranks bets using impact, evidence, leverage, effort, dependencies, control burden and opportunity cost."""
import sys
def score(item:dict)->float:
    pos=.30*item['impact']+.22*item['evidence']+.18*item['leverage']+.10*item.get('urgency',.5)
    neg=.08*item['effort']+.05*item['dependencies']+.04*item['control_burden']+.03*item['opportunity_cost']
    return round((pos-neg)*100,2)
def rank(items:list[dict])->list[dict]: return sorted([dict(x,priority_score=score(x)) for x in items],key=lambda x:x['priority_score'],reverse=True)
def self_test():
    items=[{'name':'a','impact':.6,'evidence':1,'leverage':.6,'effort':.2,'dependencies':.2,'control_burden':.2,'opportunity_cost':.2},{'name':'b','impact':.9,'evidence':.1,'leverage':.7,'effort':.8,'dependencies':.8,'control_burden':.8,'opportunity_cost':.8}]; assert rank(items)[0]['name']=='a'
def demo():
    items=[{'name':'agent-dashboard','impact':.7,'evidence':.95,'leverage':.8,'effort':.3,'dependencies':.2,'control_burden':.2,'opportunity_cost':.2},{'name':'autonomous-agent','impact':.85,'evidence':.35,'leverage':.9,'effort':.8,'dependencies':.8,'control_burden':.9,'opportunity_cost':.7}]
    for x in rank(items): print(x['name'],x['priority_score'])
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
