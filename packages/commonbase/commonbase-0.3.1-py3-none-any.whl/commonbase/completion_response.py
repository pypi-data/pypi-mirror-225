from typing import Optional, Literal


class CompletionChoice:
    def __init__(self, json):
        self.json = json

    @property
    def text(self) -> str:
        return self.json["text"]

    @property
    def role(self) -> Optional[str]:
        return self.json["role"] if "role" in self.json else None

    @property
    def index(self) -> int:
        return self.json["index"]

    @property
    def finish_reason(self) -> Optional[str]:
        return self.json["finish_reason"] if "finish_reason" in self.json else None


class CompletionResponse:
    def __init__(self, json: dict):
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
    def best_result(self) -> str:
        return self.choices[0].text
