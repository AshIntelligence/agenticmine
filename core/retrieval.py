from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TOKEN_RE = re.compile(r"[A-Za-z0-9_+-]+")


@dataclass
class Chunk:
    chunk_id: str
    source: str
    text: str


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def chunk_text(text: str, source: str, chunk_size: int = 850, overlap: int = 120) -> list[Chunk]:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return []
    chunks: list[Chunk] = []
    start = 0
    i = 0
    while start < len(clean):
        end = min(len(clean), start + chunk_size)
        if end < len(clean):
            boundary = clean.rfind(". ", start, end)
            if boundary > start + chunk_size // 2:
                end = boundary + 1
        segment = clean[start:end].strip()
        chunks.append(Chunk(chunk_id=f"{Path(source).name}#c{i}", source=source, text=segment))
        if end == len(clean):
            break
        start = max(start + 1, end - overlap)
        i += 1
    return chunks


class BM25Lite:
    def __init__(self, chunks: Iterable[Chunk]) -> None:
        self.chunks = list(chunks)
        self.tokens = [tokenize(c.text) for c in self.chunks]
        self.doc_freq: Counter[str] = Counter()
        for toks in self.tokens:
            self.doc_freq.update(set(toks))
        self.avg_len = sum(map(len, self.tokens)) / max(1, len(self.tokens))

    def score(self, query: str, idx: int) -> float:
        q = tokenize(query)
        tf = Counter(self.tokens[idx])
        dl = len(self.tokens[idx]) or 1
        k1, b = 1.5, 0.75
        total = 0.0
        n = max(1, len(self.chunks))
        for term in q:
            df = self.doc_freq.get(term, 0)
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            freq = tf.get(term, 0)
            denom = freq + k1 * (1 - b + b * dl / max(self.avg_len, 1))
            if denom:
                total += idf * (freq * (k1 + 1)) / denom
        return total

    def search(self, query: str, k: int = 5) -> list[tuple[Chunk, float]]:
        ranked = sorted(((self.chunks[i], self.score(query, i)) for i in range(len(self.chunks))), key=lambda x: x[1], reverse=True)
        return [(c, s) for c, s in ranked[:k] if s > 0]
