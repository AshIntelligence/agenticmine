from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    mode: str = os.getenv("AGENT_MODE", "mock").lower()
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")
    max_tokens: int = int(os.getenv("ANTHROPIC_MAX_TOKENS", "1800"))
    trace_dir: str = os.getenv("TRACE_DIR", "traces")

    @property
    def live(self) -> bool:
        return self.mode == "live" and bool(os.getenv("ANTHROPIC_API_KEY"))


settings = Settings()
