from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class TraceEvent:
    run_id: str
    agent: str
    step: str
    started_at: float
    elapsed_ms: int
    input: Any
    output: Any
    metadata: dict[str, Any]


class TraceLogger:
    def __init__(self, agent: str, trace_dir: str | Path = "traces") -> None:
        self.agent = agent
        self.run_id = uuid.uuid4().hex[:12]
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.trace_dir / f"{agent}-{self.run_id}.jsonl"

    def record(self, step: str, input_data: Any, output_data: Any, started_at: float, **metadata: Any) -> None:
        event = TraceEvent(self.run_id, self.agent, step, started_at, int((time.time() - started_at) * 1000), input_data, output_data, metadata)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), ensure_ascii=False, default=str) + "\n")


class traced_step:
    def __init__(self, logger: TraceLogger, step: str, input_data: Any, **metadata: Any) -> None:
        self.logger = logger
        self.step = step
        self.input_data = input_data
        self.metadata = metadata
        self.started_at = 0.0
        self.output_data: Any = None

    def __enter__(self):
        self.started_at = time.time()
        return self

    def set_output(self, output_data: Any) -> None:
        self.output_data = output_data

    def __exit__(self, exc_type, exc, tb):
        if exc is not None:
            self.logger.record(self.step, self.input_data, {"error": str(exc)}, self.started_at, **self.metadata)
            return False
        self.logger.record(self.step, self.input_data, self.output_data, self.started_at, **self.metadata)
        return False
