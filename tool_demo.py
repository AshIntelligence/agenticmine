from pathlib import Path

from agents.job_research import JobResearchAgent

ROOT = Path(__file__).resolve().parent
profile = (ROOT / "demo_data/example_profile.txt").read_text(encoding="utf-8")
agent = JobResearchAgent(ROOT / "demo_data/jobs.json", profile, trace_dir=ROOT / "traces")
result = agent.native_tool_demo("AI infrastructure reliability distributed systems developer platform")
print(result["text"])
print("\nTool events:")
for event in result["tool_events"]:
    print(event)
print(f"\nTrace: {agent.logger.path}")
