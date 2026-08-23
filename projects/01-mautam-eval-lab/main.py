"""MAUTAM AI Product Evaluation Lab

Model & Response Quality · Adoption · User Workflow Success · Trust & Controls · Availability & Health · Measurable Business Impact.
A deterministic product-level eval harness that turns six lenses into SHIP / TUNE / SIMPLIFY / STOP.
"""
from dataclasses import dataclass, asdict
import json, sys

WEIGHTS={"model_quality":.18,"adoption":.15,"workflow_success":.20,"trust_controls":.18,"availability_health":.12,"business_impact":.17}
@dataclass(frozen=True)
class Result:
    score:float; decision:str; weakest_lens:str; lens_scores:dict; rationale:tuple

def evaluate(lenses:dict)->Result:
    missing=set(WEIGHTS)-set(lenses)
    if missing: raise ValueError(f"missing lenses: {sorted(missing)}")
    clean={k:max(0,min(1,float(lenses[k]))) for k in WEIGHTS}
    score=sum(clean[k]*WEIGHTS[k] for k in WEIGHTS); weakest=min(clean,key=clean.get)
    if clean["trust_controls"]<.60 or clean["availability_health"]<.55: decision="STOP"
    elif score>=.80 and min(clean.values())>=.65: decision="SHIP"
    elif score>=.62: decision="TUNE"
    else: decision="SIMPLIFY"
    return Result(round(score,3),decision,weakest,clean,(f"weighted score={score:.2f}",f"weakest={weakest}:{clean[weakest]:.2f}","trust + availability are hard gates"))

def self_test():
    assert evaluate({k:.9 for k in WEIGHTS}).decision=="SHIP"
    x={k:.9 for k in WEIGHTS}; x["trust_controls"]=.4; assert evaluate(x).decision=="STOP"

def demo():
    sample={"model_quality":.88,"adoption":.74,"workflow_success":.82,"trust_controls":.91,"availability_health":.79,"business_impact":.77}
    print(json.dumps(asdict(evaluate(sample)),indent=2))
if __name__=="__main__": self_test() if "--test" in sys.argv else demo()
