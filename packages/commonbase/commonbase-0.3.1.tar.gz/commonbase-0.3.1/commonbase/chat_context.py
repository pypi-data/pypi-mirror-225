from typing import Literal, Sequence
from dataclasses import dataclass, asdict


@dataclass
class ChatMessage:
    role: Literal["system", "user", "assistant"]
    content: str


@dataclass
class ChatContext:
    messages: Sequence[ChatMessage]

    def _as_json(self) -> dict:
        return asdict(self)
