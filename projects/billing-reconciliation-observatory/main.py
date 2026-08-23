"""Billing Reconciliation Observatory
End-to-end usage → rating → invoice reconciliation with exposure-aware severity."""
import sys
def reconcile(usage:list[dict],rated:list[dict],invoices:list[dict],tolerance=.01)->dict:
    u={x['id']:x for x in usage}; r={x['id']:x for x in rated}; i={x['id']:x for x in invoices}; issues=[]
    for k in sorted(set(u)|set(r)|set(i)):
        if k not in u or k not in r or k not in i: issues.append({'id':k,'type':'missing-stage','severity':'high'}); continue
        expected=round(u[k]['qty']*r[k]['unit_price'],2); actual=round(i[k]['amount'],2); delta=round(actual-expected,2)
        if abs(delta)>tolerance: issues.append({'id':k,'type':'amount-mismatch','delta':delta,'severity':'critical' if abs(delta)>1000 else 'medium'})
    return {'records':len(set(u)|set(r)|set(i)),'issues':issues,'healthy':not issues}
def self_test():
    assert reconcile([{'id':'a','qty':2}],[{'id':'a','unit_price':3}],[{'id':'a','amount':6}])['healthy']; assert reconcile([{'id':'a','qty':2}],[{'id':'a','unit_price':3}],[{'id':'a','amount':9}])['issues']
def demo(): print(reconcile([{'id':'m1','qty':100},{'id':'m2','qty':50}],[{'id':'m1','unit_price':2},{'id':'m2','unit_price':3}],[{'id':'m1','amount':200},{'id':'m2','amount':400}]))
if __name__=='__main__': self_test() if '--test' in sys.argv else demo()
