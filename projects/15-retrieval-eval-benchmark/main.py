"""Retrieval Evaluation Benchmark
Computes Precision@K, Recall@K, MRR and nDCG for retrieval experiments."""
import math,sys
def metrics(ranked:list[str],relevant:set[str],k=5)->dict:
    top=ranked[:k]; hits=[1 if x in relevant else 0 for x in top]
    precision=sum(hits)/max(1,k); recall=sum(hits)/max(1,len(relevant)); rr=next((1/(i+1) for i,x in enumerate(ranked) if x in relevant),0)
    dcg=sum(h/math.log2(i+2) for i,h in enumerate(hits)); ideal=[1]*min(k,len(relevant))+[0]*max(0,k-len(relevant)); idcg=sum(h/math.log2(i+2) for i,h in enumerate(ideal))
    return {'precision_at_k':round(precision,3),'recall_at_k':round(recall,3),'mrr':round(rr,3),'ndcg_at_k':round(dcg/idcg if idcg else 0,3)}
def self_test():
    x=metrics(['a','b'],{'a','b'},2); assert x['precision_at_k']==1 and x['recall_at_k']==1; assert metrics(['x','a'],{'a'},2)['mrr']==.5
def demo(): print(metrics(['d3','d1','d9','d2','d7'],{'d1','d2','d5'},5))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
