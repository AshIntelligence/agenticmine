"""Agent Tool Permission Policy Engine
Evaluates an agent tool call against role, action type, sensitivity and approval state."""
import sys
READ_ONLY={'search','read','list'}; DESTRUCTIVE={'delete','transfer','publish','refund'}
def authorize(role:str,tool:str,action:str,sensitivity:str='internal',approved=False)->dict:
    risk=3 if action in DESTRUCTIVE else 1 if action not in READ_ONLY else 0
    risk+=3 if sensitivity=='restricted' else 2 if sensitivity=='confidential' else 0
    if role in {'viewer','guest'} and action not in READ_ONLY: return {'decision':'DENY','reason':'role cannot mutate'}
    if risk>=4 and not approved: return {'decision':'APPROVAL_REQUIRED','risk':risk}
    if risk>=6 and role!='admin': return {'decision':'DENY','risk':risk}
    return {'decision':'ALLOW','risk':risk,'audit':f'{role}:{tool}:{action}:{sensitivity}'}
def self_test():
    assert authorize('viewer','x','publish')['decision']=='DENY'; assert authorize('operator','x','refund','restricted')['decision']=='APPROVAL_REQUIRED'
def demo():
    for x in [('analyst','payments','read','confidential',False),('operator','payments','refund','restricted',False),('admin','payments','refund','restricted',True)]: print(x,authorize(*x))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
