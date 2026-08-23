"""Agent vs Workflow Router

Chooses deterministic workflow, assisted agent, or autonomous agent from variability, consequence, tool count, state and ambiguity.
The point: agency is a product mechanism, not a default architecture choice.
"""
from dataclasses import dataclass
import sys
@dataclass(frozen=True)
class Decision:
    mechanism:str; score:float; reasons:tuple; controls:tuple

def route(variability:float, consequence:float, tool_count:int, statefulness:float, ambiguity:float)->Decision:
    vals=[variability,consequence,statefulness,ambiguity]
    if any(v<0 or v>1 for v in vals): raise ValueError("scores must be 0..1")
    agency=.30*variability+.25*ambiguity+.20*statefulness+.05*min(tool_count/8,1)-.35*consequence
    if consequence>=.80: mech="assisted-agent" if variability+.2*tool_count>1 else "deterministic-workflow"
    elif agency>=.42: mech="autonomous-agent"
    elif agency>=.15: mech="assisted-agent"
    else: mech="deterministic-workflow"
    controls=[]
    if consequence>.55: controls.append("human-approval")
    if tool_count>3: controls.append("tool-allowlist")
    if statefulness>.55: controls.append("state-checkpointing")
    return Decision(mech,round(agency,3),(f"consequence={consequence:.2f}",f"tools={tool_count}"),tuple(controls))

def self_test():
    assert route(.9,.95,5,.7,.8).mechanism!="autonomous-agent"
    assert route(.1,.3,1,.1,.1).mechanism=="deterministic-workflow"

def demo():
    cases={"invoice-refund":(.35,.92,2,.45,.30),"research-brief":(.92,.18,6,.60,.88),"data-export":(.10,.45,1,.10,.10)}
    for name,args in cases.items(): print(name,route(*args))
if __name__=="__main__": self_test() if "--test" in sys.argv else demo()
