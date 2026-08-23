"""Agentic Product Control Plane
Mini control plane for agent registry, tool policy, eval gates, cost budgets and rollout state."""
from dataclasses import dataclass,field
import sys
@dataclass
class AgentSpec:
    name:str; tools:list[str]; max_cost:float; min_eval:float=.75; requires_approval:list[str]=field(default_factory=list); rollout:str='shadow'
def evaluate_rollout(spec:AgentSpec,eval_score:float,incident_rate:float,cost_p95:float)->dict:
    blockers=[]
    if eval_score<spec.min_eval: blockers.append('eval-below-gate')
    if incident_rate>.02: blockers.append('incident-rate')
    if cost_p95>spec.max_cost: blockers.append('cost-budget')
    state='HOLD' if blockers else 'CANARY' if spec.rollout=='shadow' else 'PRODUCTION'
    return {'agent':spec.name,'state':state,'blockers':blockers,'tools':spec.tools,'approval_tools':spec.requires_approval}
def self_test():
    assert evaluate_rollout(AgentSpec('a',[],1,min_eval=.9),.7,0,.1)['state']=='HOLD'; assert evaluate_rollout(AgentSpec('a',[],1,min_eval=.8,rollout='canary'),.9,0,.1)['state']=='PRODUCTION'
def demo():
    spec=AgentSpec('finance-agent',['search','draft','refund'],max_cost=.25,min_eval=.82,requires_approval=['refund'],rollout='canary'); print(evaluate_rollout(spec,.89,.005,.19))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
