from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Callable

from .config import settings


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], Any]

    def spec(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description, "input_schema": self.input_schema}


class AnthropicToolRuntime:
    def __init__(self, tools: list[Tool], system: str, max_turns: int = 6) -> None:
        self.tools = {t.name: t for t in tools}
        self.system = system
        self.max_turns = max_turns
        self.model = os.getenv("ANTHROPIC_MODEL", settings.anthropic_model)
        self.live = os.getenv("AGENT_MODE", settings.mode).lower() == "live" and bool(os.getenv("ANTHROPIC_API_KEY"))
        self._client = None
        if self.live:
            try:
                from anthropic import Anthropic
            except ImportError as e:
                raise RuntimeError("Install anthropic to use live tool calling") from e
            self._client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def run(self, prompt: str) -> dict[str, Any]:
        if not self.live:
            return {"text": "[MOCK TOOL MODE] Native tool loop available in live mode.", "tool_events": [], "model": "mock"}
        assert self._client is not None
        messages: list[Any] = [{"role": "user", "content": prompt}]
        events: list[dict[str, Any]] = []
        for _ in range(self.max_turns):
            message = self._client.messages.create(model=self.model, max_tokens=settings.max_tokens, system=self.system, messages=messages, tools=[t.spec() for t in self.tools.values()])
            tool_blocks = [b for b in message.content if getattr(b, "type", None) == "tool_use"]
            text_blocks = [b.text for b in message.content if getattr(b, "type", None) == "text"]
            if not tool_blocks:
                return {"text": "\n".join(text_blocks), "tool_events": events, "model": self.model}
            messages.append({"role": "assistant", "content": message.content})
            results = []
            for block in tool_blocks:
                name = block.name
                args = block.input if isinstance(block.input, dict) else dict(block.input)
                if name not in self.tools:
                    value = {"error": f"Unknown tool: {name}"}
                else:
                    try:
                        value = self.tools[name].handler(args)
                    except Exception as exc:
                        value = {"error": str(exc)}
                events.append({"tool": name, "input": args, "output": value})
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(value, ensure_ascii=False, default=str)})
            messages.append({"role": "user", "content": results})
        return {"text": "Tool loop stopped at max_turns.", "tool_events": events, "model": self.model}
