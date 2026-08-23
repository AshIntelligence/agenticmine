"""Payment Provider Onboarding Simulator
Reusable provider contract + regional launch/readiness gate."""
import sys
REQUIRED={'tokenization','webhooks','idempotency','refunds','disputes'}
def assess(provider:dict, market:dict)->dict:
    caps=set(provider.get('capabilities',[])); missing=sorted(REQUIRED-caps)
    blockers=missing
    if market['country'] not in provider.get('countries',[]): blockers+=['country']
    if market['currency'] not in provider.get('currencies',[]): blockers+=['currency']
    if provider.get('chargeback_rate',1)>market.get('max_chargeback_rate',.01): blockers+=['chargeback-rate']
    if provider.get('uptime',0)<market.get('min_uptime',.999): blockers+=['uptime']
    return {'ready':not blockers,'blockers':blockers,'reusability_score':round(len(caps&REQUIRED)/len(REQUIRED),2)}
def self_test():
    p={'capabilities':list(REQUIRED),'countries':['US'],'currencies':['USD'],'chargeback_rate':.001,'uptime':1}; assert assess(p,{'country':'US','currency':'USD'})['ready']
    assert not assess({'capabilities':[],'countries':['US'],'currencies':['USD'],'chargeback_rate':0,'uptime':1},{'country':'US','currency':'USD'})['ready']
def demo():
    p={'capabilities':list(REQUIRED),'countries':['BR','MX'],'currencies':['BRL','MXN'],'chargeback_rate':.006,'uptime':.9995}; print(assess(p,{'country':'BR','currency':'BRL'}))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
