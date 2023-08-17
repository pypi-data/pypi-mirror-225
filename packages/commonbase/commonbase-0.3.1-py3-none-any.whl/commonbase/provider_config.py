from typing import Literal, Optional, Sequence, Union
from dataclasses import dataclass, asdict


@dataclass
class OpenAIParams:
    type: Literal["chat", "text"]
    model: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    n: Optional[int] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stop: Optional[Union[str, Sequence[str]]] = None
    best_of: Optional[int] = None
    suffix: Optional[str] = None
    logprobs: Optional[int] = None


@dataclass
class AnthropicParams:
    type: Union[Literal["chat"], None] = None
    model: Optional[str] = None
    max_tokens_to_sample: Optional[int] = None
    temperature: Optional[float] = None
    stop_sequences: Optional[Sequence[str]] = None
    top_k: Optional[float] = None
    top_p: Optional[float] = None


@dataclass
class ProviderConfig:
    provider: Literal["openai", "cb-openai-eu", "anthropic"]
    params: Union[OpenAIParams, AnthropicParams]

    def _as_json(self) -> dict:
        return asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
