# Native Claude tool calling

The deterministic ranking path is model-independent. The same agent also exposes `native_tool_demo()` for live tool use.

In live mode Claude receives two tools:

- `search_jobs(query, top_k)`
- `analyze_job(job_id)`

Claude can decide which records to inspect, call the local Python handlers, receive structured tool results, and continue until it produces a final recommendation.

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
   +--> tool_use: analyze_job --------> profile-grounded scorer
   |                                      |
   |<------------- tool_result -----------+
   |
   v
Final Claude recommendation
```

Set `AGENT_MODE=live`, `ANTHROPIC_API_KEY`, and optionally `ANTHROPIC_MODEL` first.
