from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any

from .config import settings


@dataclass
class LLMResult:
    text: str
    raw: Any | None = None
    model: str = "mock"


class ClaudeClient:
    """Tiny provider wrapper with deterministic mock mode."""

    def __init__(self) -> None:
        mode = os.getenv("AGENT_MODE", settings.mode).lower()
        self.live = mode == "live" and bool(os.getenv("ANTHROPIC_API_KEY"))
        self.model = os.getenv("ANTHROPIC_MODEL", settings.anthropic_model)
        self._client = None
        if self.live:
            try:
                from anthropic import Anthropic
            except ImportError as e:
                raise RuntimeError("Install the Anthropic SDK: pip install anthropic") from e
            self._client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def complete(self, *, system: str, prompt: str, max_tokens: int | None = None) -> LLMResult:
        if not self.live:
            return LLMResult(text=self._mock_completion(system, prompt), model="mock")
        assert self._client is not None
        message = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens or settings.max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        text_parts = [block.text for block in message.content if getattr(block, "type", None) == "text"]
        return LLMResult(text="\n".join(text_parts), raw=message, model=self.model)

    def json(self, *, system: str, prompt: str, fallback: dict[str, Any]) -> dict[str, Any]:
        if not self.live:
            return fallback
        result = self.complete(system=system + "\nReturn only valid JSON.", prompt=prompt)
        text = result.text.strip()
        fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.S)
        if fenced:
            text = fenced.group(1)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {**fallback, "_raw_model_output": result.text}

    def _mock_completion(self, system: str, prompt: str) -> str:
        head = prompt.strip().splitlines()[0][:120] if prompt.strip() else "request"
        return f"[MOCK MODE] Processed: {head}. Set AGENT_MODE=live and ANTHROPIC_API_KEY for a live Claude response."
