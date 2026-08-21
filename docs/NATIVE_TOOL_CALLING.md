# Native Claude tool calling

The deterministic job-ranking path is deliberately model-independent. For a deeper live demo, the same agent also exposes `native_tool_demo()`.

In live mode Claude receives two actual tools:

- `search_jobs(query, top_k)`
- `analyze_job(job_id)`

Claude can decide which candidates to inspect, call the local Python handlers, receive structured tool results, and continue the conversation until it produces a final recommendation.

```text
User intent
   |
   v
Claude Messages API
   |
   +--> tool_use: search_jobs --------> local job corpus
   |                                      |
   |<------------- tool_result -----------+
   |
   +--> tool_use: analyze_job --------> resume-grounded scorer
   |                                      |
   |<------------- tool_result -----------+
   |
   v
Final Claude recommendation
```

Set `AGENT_MODE=live`, `ANTHROPIC_API_KEY`, and optionally `ANTHROPIC_MODEL` first.
