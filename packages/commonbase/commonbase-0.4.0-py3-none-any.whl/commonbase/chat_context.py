from typing import Literal, NotRequired, TypedDict, Optional


class FunctionCall(TypedDict):
    name: str
    arguments: Optional[str]


class RegularChatMessage(TypedDict):
    role: Literal["system", "user"]
    content: str


class AssistantChatMessage(TypedDict):
    role: Literal["assistant"]
    content: str | None
    function_call: NotRequired[FunctionCall]


class FunctionChatMessage(TypedDict):
    role: Literal["function"]
    name: str
    content: str


class FunctionCallConfigName(TypedDict):
    name: str


class ChatFunction(TypedDict):
    name: str
    description: str
    parameters: object


ChatMessage = RegularChatMessage | AssistantChatMessage | FunctionChatMessage
FunctionCallConfig = Literal["none", "auto"] | FunctionCallConfigName
