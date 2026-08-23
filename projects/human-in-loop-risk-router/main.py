"""Human-in-the-Loop Risk Router

Routes an AI/agent action to ALLOW, REVIEW or DENY using consequence, confidence, reversibility and data sensitivity.
"""
from dataclasses import dataclass
import sys
@dataclass(frozen=True)
class Route:
    action:str; risk:float; reasons:tuple

def decide(consequence:float,confidence:float,reversibility:float,sensitive:bool=False)->Route:
    risk=min(1,.48*consequence+.28*(1-confidence)+.18*(1-reversibility)+(.16 if sensitive else 0))
    action="DENY" if risk>=.78 else "REVIEW" if risk>=.43 else "ALLOW"
    return Route(action,round(risk,3),(f"consequence={consequence:.2f}",f"confidence={confidence:.2f}",f"reversible={reversibility:.2f}",f"sensitive={sensitive}"))

def self_test():
    assert decide(.8,.9,.1,True).action in {"REVIEW","DENY"}
    assert decide(.1,.95,1,False).action=="ALLOW"

def demo():
    for x in [("refund",.55,.94,.9,False),("delete-account",.95,.88,.1,True),("draft-email",.2,.8,1,False)]: print(x[0],decide(*x[1:]))
if __name__=="__main__": self_test() if "--test" in sys.argv else demo()
