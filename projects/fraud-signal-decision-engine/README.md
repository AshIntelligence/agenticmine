# Fraud Signal Decision Engine

`Python · risk decisioning`

This engine combines behavioral, payment and identity signals into explainable **ALLOW / REVIEW / BLOCK** states.

I am intentionally optimizing for the tradeoff, not maximum blocking. A fraud system can reduce loss and still be a bad product if false positives destroy good-user conversion or push too much volume into manual review.

## Run

```bash
python main.py
python main.py --test
```

The output keeps the contributing signals visible so a reviewer or downstream policy layer can understand why the action changed.
