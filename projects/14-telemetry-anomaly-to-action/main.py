"""Telemetry Anomaly → Product Action
Detects rolling anomalies and translates them into product actions instead of stopping at a red dashboard."""
import statistics,sys
def detect(values:list[float],window=5,threshold=2.0)->list[dict]:
    out=[]
    for i,v in enumerate(values):
        if i<window: continue
        hist=values[i-window:i]; mean=statistics.mean(hist); sd=statistics.pstdev(hist) or 1e-9; z=(v-mean)/sd
        if abs(z)>=threshold: out.append({'index':i,'value':v,'z':round(z,2),'action':'investigate-regression' if z<0 else 'validate-growth-signal'})
    return out
def self_test(): assert detect([1,1,1,1,1,10]); assert detect([1,1,1,1,1,1])==[]
def demo(): print(detect([100,102,98,101,99,100,52,101,150]))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
