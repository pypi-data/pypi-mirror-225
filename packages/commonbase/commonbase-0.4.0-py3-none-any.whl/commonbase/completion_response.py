from typing import Optional, Literal, Any
import json
from commonbase.chat_context import FunctionCall, AssistantChatMessage


class FunctionCallResponse:
    def __init__(self, json: FunctionCall) -> None:
        self.json = json

    @property
    def name(self) -> str:
        return self.json["name"]

    @property
    def arguments(self) -> dict[str, Any]:
        try:
            return json.loads(
                self.json["arguments"] or "" if "arguments" in self.json else ""
            )
        except:
            return {}


class CompletionChoice:
    def __init__(self, json: dict[str, Any]):
        self.json = json

    @property
    def text(self) -> str:
        return self.json["text"] if "text" in self.json else ""

    @property
    def role(self) -> Optional[str]:
        return self.json["role"] if "role" in self.json else None

    @property
    def index(self) -> int:
        return self.json["index"]

    @property
    def finish_reason(self) -> Optional[str]:
        return self.json["finish_reason"] if "finish_reason" in self.json else None

    @property
    def function_call(self) -> Optional[FunctionCallResponse]:
        return (
            FunctionCallResponse(self.json["function_call"])
            if "function_call" in self.json
            else None
        )

    def to_assistant_chat_message(self) -> AssistantChatMessage:
        function_call = self.function_call
        if function_call is not None:
            return {
                "role": "assistant",
                "content": self.text,
                "function_call": function_call.json,
            }
        else:
            return {"role": "assistant", "content": self.text}


class CompletionResponse:
    def __init__(self, json: dict[str, Any]):
        self.json = json

    @property
    def completed(self) -> bool:
        return self.json["completed"]

    @property
    def invocation_id(self) -> str:
        return self.json["invocationId"]

    @property
    def project_id(self) -> str:
        return self.json["projectId"]

    @property
    def type(self) -> Literal["text", "chat"]:
        return self.json["type"]

    @property
    def model(self) -> str:
        return self.json["model"]

    @property
    def choices(self) -> list[CompletionChoice]:
        return [CompletionChoice(choice) for choice in self.json["choices"]]

    @property
    def best_choice(self) -> CompletionChoice:
        return CompletionChoice(self.json["choices"][0])
