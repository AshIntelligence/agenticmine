from __future__ import annotations

import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from core.evaluation import citation_coverage
from core.io_utils import read_text_file
from core.llm import ClaudeClient
from core.retrieval import BM25Lite, Chunk, chunk_text
from core.tracing import TraceLogger, traced_step


@dataclass
class Evidence:
    chunk_id: str
    source: str
    score: float
    text: str


@dataclass
class DocumentAnswer:
    question: str
    answer: str
    evidence: list[Evidence]
    evals: list[dict]
    trace_path: str


class DocumentIntelligenceAgent:
    """Retrieval + evidence-grounded synthesis + contradiction detection."""

    def __init__(self, paths: Iterable[str | Path], trace_dir: str = "traces") -> None:
        self.paths = [Path(p) for p in paths]
        self.logger = TraceLogger("document-intelligence", trace_dir)
        self.llm = ClaudeClient()
        self.chunks: list[Chunk] = []
        self._index()

    def _index(self) -> None:
        with traced_step(self.logger, "ingest_and_chunk", [str(p) for p in self.paths]) as trace:
            for path in self.paths:
                text = read_text_file(path)
                self.chunks.extend(chunk_text(text, str(path)))
            self.retriever = BM25Lite(self.chunks)
            trace.set_output({"chunks": len(self.chunks), "sources": len(self.paths)})

    def retrieve(self, question: str, k: int = 6) -> list[Evidence]:
        with traced_step(self.logger, "retrieve", {"question": question, "k": k}) as trace:
            hits = [Evidence(c.chunk_id, c.source, round(score, 4), c.text) for c, score in self.retriever.search(question, k=k)]
            trace.set_output([asdict(h) for h in hits])
            return hits

    def answer(self, question: str, k: int = 6) -> DocumentAnswer:
        evidence = self.retrieve(question, k=k)
        if not evidence:
            text = "I could not find sufficient evidence in the indexed documents to answer that question."
            return DocumentAnswer(question, text, [], [], str(self.logger.path))

        context = "\n\n".join(f"[{e.chunk_id}] {e.text}" for e in evidence)
        with traced_step(self.logger, "grounded_synthesis", {"question": question, "evidence_ids": [e.chunk_id for e in evidence]}) as trace:
            if self.llm.live:
                prompt = f"""Question: {question}\n\nEvidence:\n{context}\n\nAnswer using only the evidence. Cite every material claim with the relevant [chunk_id]. If evidence conflicts, say so explicitly. If evidence is insufficient, say what is missing."""
                answer = self.llm.complete(
                    system="You are an evidence-grounded document intelligence agent. Never invent facts outside supplied evidence.",
                    prompt=prompt,
                ).text
            else:
                answer = self._mock_answer(question, evidence)
            trace.set_output(answer)

        markers = [f"[{e.chunk_id}]" for e in evidence[:3]]
        eval_result = citation_coverage(answer, markers).to_dict()
        self.logger.record("evaluate_citations", {"markers": markers}, eval_result, time.time())
        return DocumentAnswer(question, answer, evidence, [eval_result], str(self.logger.path))

    def compare(self, topic: str, k: int = 8) -> DocumentAnswer:
        question = f"Compare the documents on {topic}. Identify agreements, contradictions, and missing evidence."
        return self.answer(question, k=k)

    def _mock_answer(self, question: str, evidence: list[Evidence]) -> str:
        q_terms = {t.lower() for t in re.findall(r"[A-Za-z0-9]+", question) if len(t) > 3}
        ql = question.lower()
        if "postmortem" in ql or "post-mortem" in ql:
            q_terms.update({"post-incident", "review", "business", "days"})
        if "timing" in ql or "within" in ql:
            q_terms.update({"within", "minutes", "days"})
        if "availability" in ql:
            q_terms.update({"availability", "monthly", "99"})
        lines: list[str] = []
        for e in evidence[:3]:
            sentences = re.split(r"(?<=[.!?])\s+", e.text)
            best = max(sentences, key=lambda s: sum(1 for t in q_terms if t in s.lower()), default=e.text[:220])
            lines.append(f"- {best.strip()} [{e.chunk_id}]")
        return "Evidence-grounded findings:\n" + "\n".join(lines) + "\n\nMock mode intentionally returns extractive evidence; live mode adds Claude synthesis."
