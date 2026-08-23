# Voice of Customer Synthesis

`Python · product discovery`

This combines qualitative comments and sentiment with quantitative usage evidence to rank recurring product pain.

I use both because qualitative volume alone rewards the loudest cohort, while telemetry alone misses unmet need, intent and the reason behind behavior.

## Run

```bash
python main.py
python main.py --test
```

The useful output is not a sentiment summary. It is a product question with evidence: who experiences the problem, how often, how severe it is, and whether observed behavior supports the story users are telling us.
