"""Intentional Discovery Study
Personal recommendation study using Instagram discovery as the surface. Unaffiliated with Instagram."""
import sys

def rank(items:list[dict], interests:set[str], seen_creators:set[str], minutes_left:int)->list[dict]:
    out=[]
    for x in items:
        tags=set(x.get('tags',[])); relevance=len(tags&interests)/max(1,len(interests)); novelty=.25 if x.get('creator') not in seen_creators else 0; diversity=.15 if x.get('creator') not in seen_creators else 0; rage=.25 if x.get('ragebait') else 0; long_penalty=.18 if x.get('minutes',1)>max(1,minutes_left) else 0
        score=.7*relevance+novelty+diversity-rage-long_penalty
        out.append(dict(x,score=round(score,3)))
    return sorted(out,key=lambda x:x['score'],reverse=True)

def self_test():
    xs=[{'id':'a','creator':'new','tags':['design'],'minutes':1},{'id':'b','creator':'old','tags':['other'],'ragebait':True,'minutes':1}]; assert rank(xs,{'design'},{'old'},5)[0]['id']=='a'
def demo():
    xs=[{'id':'quiet-design','creator':'c1','tags':['design','travel'],'minutes':2},{'id':'rage','creator':'c2','tags':['design'],'ragebait':True,'minutes':1},{'id':'long','creator':'c3','tags':['travel'],'minutes':12}]; print(rank(xs,{'design','travel'},set(),6))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
