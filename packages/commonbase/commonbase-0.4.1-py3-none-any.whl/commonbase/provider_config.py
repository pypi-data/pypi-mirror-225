from typing import Literal, Sequence, Union, NotRequired, TypedDict


class OpenAIParams(TypedDict):
    temperature: NotRequired[float]
    top_p: NotRequired[float]
    max_tokens: NotRequired[int]
    n: NotRequired[int]
    frequency_penalty: NotRequired[float]
    presence_penalty: NotRequired[float]
    stop: NotRequired[Union[str, Sequence[str]]]
    best_of: NotRequired[int]
    suffix: NotRequired[str]
    logprobs: NotRequired[int]


class AnthropicParams(TypedDict):
    max_tokens_to_sample: NotRequired[int]
    temperature: NotRequired[float]
    stop_sequences: NotRequired[Sequence[str]]
    top_k: NotRequired[float]
    top_p: NotRequired[float]


ProviderName = Literal["openai", "cb-openai-eu", "cb-openai-us", "anthropic"]
ProviderParams = OpenAIParams | AnthropicParams
