"""PRFAQ Product Spec Agent
Turns a product brief into a structured PRFAQ skeleton with users, promise, metrics, risks and open questions."""
from dataclasses import dataclass,asdict
import json,sys
@dataclass
class PRFAQ:
    headline:str; customer:str; problem:str; promise:str; metrics:list[str]; risks:list[str]; questions:list[str]
def generate(name:str,customer:str,problem:str,outcome:str,constraints:list[str])->PRFAQ:
    metrics=['task completion','time-to-value','repeat adoption']
    if any('risk' in c.lower() or 'privacy' in c.lower() for c in constraints): metrics.append('safe-completion rate')
    return PRFAQ(f'{name}: {outcome}',customer,problem,outcome,metrics,[f'Constraint: {c}' for c in constraints],[
      'What user behavior proves this is better than the current workaround?',
      'What should remain deterministic or human-controlled?',
      'What is the narrowest useful launch?'])
def self_test():
    assert 'safe-completion rate' in generate('x','u','p','o',['privacy']).metrics; assert len(generate('x','u','p','o',[]).questions)>=3
def demo(): print(json.dumps(asdict(generate('Close Copilot','finance analyst','manual exception chasing','close exceptions resolved faster',['SOX controls','PII privacy'])),indent=2))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
