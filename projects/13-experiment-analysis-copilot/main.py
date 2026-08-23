"""Experiment Analysis Copilot
Computes conversion uplift, a two-proportion z-test and a product recommendation without external libraries."""
import math,sys
def analyze(control_success:int,control_n:int,treatment_success:int,treatment_n:int,alpha=.05)->dict:
    if min(control_n,treatment_n)<=0: raise ValueError('n must be positive')
    pc=control_success/control_n; pt=treatment_success/treatment_n; pooled=(control_success+treatment_success)/(control_n+treatment_n)
    se=math.sqrt(max(1e-12,pooled*(1-pooled)*(1/control_n+1/treatment_n))); z=(pt-pc)/se; p=math.erfc(abs(z)/math.sqrt(2)); uplift=(pt-pc)/pc if pc else float('inf')
    decision='SHIP' if p<alpha and pt>pc else 'STOP' if p<alpha and pt<pc else 'HOLD'
    return {'control_rate':round(pc,4),'treatment_rate':round(pt,4),'relative_uplift':round(uplift,4),'z':round(z,3),'p_value':round(p,5),'decision':decision}
def self_test(): assert analyze(100,1000,160,1000)['decision']=='SHIP'; assert analyze(100,1000,100,1000)['decision']=='HOLD'
def demo(): print(analyze(1200,10000,1320,10000))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
