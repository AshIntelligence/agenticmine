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
    def _terms(text: str) -> list[str]:
        """Normalize lexical intent without pretending unrelated phrases are semantic matches.

        Slash-separated terms such as AI/ML become two searchable terms. A light plural
        normalizer maps platforms→platform, systems→system, APIs→api, etc. We keep the
        representation intentionally transparent because this demo is about inspectable
        ranking behavior rather than opaque embedding similarity.
        """
        text = text.lower().replace("/", " ")
        raw = re.findall(r"[a-z][a-z0-9+.-]*", text)
        normalized: list[str] = []
        for token in raw:
            if len(token) > 4 and token.endswith("ies"):
                token = token[:-3] + "y"
            elif len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
                token = token[:-1]
            normalized.append(token)
        return normalized

    @classmethod
    def _tokens(cls, text: str) -> set[str]:
        return set(cls._terms(text))

    def _intent_relevance(self, query: str, job: JobCandidate) -> float:
        """Corpus-aware lexical relevance with extra weight for explicit title intent.

        IDF prevents generic words from dominating and title weighting distinguishes an
        explicitly requested "AI Infrastructure" role from a role that only happens to
        mention generic terms such as "systems" in its body.
        """
        q_terms = set(self._terms(query))
        if not q_terms:
            return 0.0

        corpus = [
            set(self._terms(f"{candidate.title} {candidate.description}"))
            for candidate in self.jobs
        ]
        n = len(corpus)
        idf = {
            term: math.log((n + 1) / (1 + sum(term in doc for doc in corpus))) + 1
            for term in q_terms
        }

        title_terms = set(self._terms(job.title))
        body_terms = set(self._terms(job.description))
        weighted_hits = sum(
            idf[term]
            * (2.5 * (term in title_terms) + 1.0 * (term in body_terms))
            for term in q_terms
        )
        max_weight = sum(idf[term] * 3.5 for term in q_terms)
        return weighted_hits / max(1e-9, max_weight)

    def discover(self, query: str, top_k: int = 5) -> list[JobCandidate]:
        with traced_step(self.logger, "discover", {"query": query, "top_k": top_k}) as trace:
            scored = [(self._intent_relevance(query, job), job) for job in self.jobs]
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
        matches = []
        for job in discovered:
            match = self.analyze(job)
            query_relevance = self._intent_relevance(query, job)
            combined = round(0.5 * match.score + 50 * query_relevance, 1)
            match.score = combined
            match.rationale += f" Combined score includes {query_relevance:.0%} corpus-aware query-intent relevance."
            matches.append(match)
        ranked = sorted(matches, key=lambda x: x.score, reverse=True)[:top_k]
        eval_result = keyword_coverage(
            " ".join(m.rationale for m in ranked),
            ["matched", "gaps"], threshold=1.0,
        ).to_dict()
        self.logger.record("evaluate_rank_output", {"query": query}, eval_result, time.time())
        return ranked
