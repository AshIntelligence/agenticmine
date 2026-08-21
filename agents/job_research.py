from __future__ import annotations

import json
import math
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from core.evaluation import keyword_coverage
from core.llm import ClaudeClient
from core.tracing import TraceLogger, traced_step
from core.tool_runtime import AnthropicToolRuntime, Tool


@dataclass
class JobCandidate:
    id: str
    title: str
    company: str
    location: str
    description: str


@dataclass
class JobMatch:
    job: JobCandidate
    score: float
    matched_terms: list[str]
    gaps: list[str]
    rationale: str


class JobResearchAgent:
    """Agentic job analysis over a supplied job corpus."""

    SIGNALS = [
        "infrastructure", "distributed systems", "reliability", "observability",
        "developer productivity", "developer platform", "api", "migration", "ai/ml",
        "incident response", "cloud", "security", "technical program", "cross-functional",
    ]

    def __init__(self, jobs_path: str | Path, resume_text: str, trace_dir: str = "traces") -> None:
        self.jobs_path = Path(jobs_path)
        self.resume_text = resume_text
        self.logger = TraceLogger("job-research", trace_dir)
        self.llm = ClaudeClient()
        self.jobs = self._load_jobs()

    def _load_jobs(self) -> list[JobCandidate]:
        with traced_step(self.logger, "load_job_corpus", str(self.jobs_path)) as trace:
            data = json.loads(self.jobs_path.read_text(encoding="utf-8"))
            jobs = [JobCandidate(**row) for row in data]
            trace.set_output({"jobs": len(jobs)})
            return jobs

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9/+.-]+", text)}

    def discover(self, query: str, top_k: int = 5) -> list[JobCandidate]:
        with traced_step(self.logger, "discover", {"query": query, "top_k": top_k}) as trace:
            q = self._tokens(query)
            scored = []
            for job in self.jobs:
                hay = self._tokens(f"{job.title} {job.company} {job.description}")
                score = len(q & hay) / max(1, len(q))
                scored.append((score, job))
            results = [j for _, j in sorted(scored, key=lambda x: x[0], reverse=True)[:top_k]]
            trace.set_output([asdict(j) for j in results])
            return results

    def analyze(self, job: JobCandidate) -> JobMatch:
        with traced_step(self.logger, "extract_resume_evidence", job.id) as trace:
            resume_lower = self.resume_text.lower()
            job_lower = job.description.lower()
            matched = [s for s in self.SIGNALS if s in resume_lower and s in job_lower]
            gaps = [s for s in self.SIGNALS if s in job_lower and s not in resume_lower]
            trace.set_output({"matched": matched, "gaps": gaps})

        coverage = len(matched) / max(1, len([s for s in self.SIGNALS if s in job_lower]))
        score = round(100 * coverage, 1)

        with traced_step(self.logger, "fit_rationale", {"job_id": job.id, "score": score}) as trace:
            if self.llm.live:
                rationale = self.llm.complete(
                    system="You are a rigorous job-fit analyst. Never claim experience not present in the supplied resume evidence.",
                    prompt=f"""Job:\n{job.title} at {job.company}\n{job.description}\n\nResume:\n{self.resume_text}\n\nMatched signals: {matched}\nGaps: {gaps}\nGive a concise fit rationale and distinguish evidence from gaps.""",
                ).text
            else:
                rationale = f"Matched {len(matched)} explicit signals: {', '.join(matched) or 'none'}. Gaps remain: {', '.join(gaps) or 'none in tracked signals'}."
            trace.set_output(rationale)

        return JobMatch(job=job, score=score, matched_terms=matched, gaps=gaps, rationale=rationale)

    def native_tool_demo(self, query: str) -> dict[str, Any]:
        def search_jobs(args: dict[str, Any]) -> Any:
            q = str(args.get("query", query))
            k = int(args.get("top_k", 4))
            return [asdict(j) for j in self.discover(q, top_k=k)]

        def analyze_job(args: dict[str, Any]) -> Any:
            job_id = str(args["job_id"])
            job = next((j for j in self.jobs if j.id == job_id), None)
            if job is None:
                return {"error": f"job_id not found: {job_id}"}
            return asdict(self.analyze(job))

        runtime = AnthropicToolRuntime(
            tools=[
                Tool(
                    name="search_jobs",
                    description="Search the local job corpus for candidates relevant to a user's role intent.",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "top_k": {"type": "integer", "minimum": 1, "maximum": 8}
                        },
                        "required": ["query"]
                    },
                    handler=search_jobs,
                ),
                Tool(
                    name="analyze_job",
                    description="Analyze one discovered job against explicit resume evidence and return matched signals and gaps.",
                    input_schema={
                        "type": "object",
                        "properties": {"job_id": {"type": "string"}},
                        "required": ["job_id"]
                    },
                    handler=analyze_job,
                ),
            ],
            system=(
                "You are a job-research agent. Use tools to discover candidates and inspect resume-grounded fit. "
                "Do not invent candidate or resume facts. Prefer the role that best matches the user's current intent, "
                "and explicitly preserve gaps."
            ),
        )
        with traced_step(self.logger, "native_claude_tool_loop", {"query": query}) as trace:
            result = runtime.run(
                f"Find and recommend the best role for this intent: {query}. Use the tools, inspect multiple candidates, and explain the final choice."
            )
            trace.set_output(result)
            return result

    def rank(self, query: str, top_k: int = 5) -> list[JobMatch]:
        discovered = self.discover(query, top_k=max(top_k, 8))
        q = self._tokens(query)
        matches = []
        for job in discovered:
            match = self.analyze(job)
            hay = self._tokens(f"{job.title} {job.description}")
            query_relevance = len(q & hay) / max(1, len(q))
            combined = round(0.5 * match.score + 50 * query_relevance, 1)
            match.score = combined
            match.rationale += f" Combined score includes {query_relevance:.0%} query-intent overlap."
            matches.append(match)
        ranked = sorted(matches, key=lambda x: x.score, reverse=True)[:top_k]
        eval_result = keyword_coverage(
            " ".join(m.rationale for m in ranked),
            ["matched", "gaps"], threshold=1.0,
        ).to_dict()
        self.logger.record("evaluate_rank_output", {"query": query}, eval_result, time.time())
        return ranked
