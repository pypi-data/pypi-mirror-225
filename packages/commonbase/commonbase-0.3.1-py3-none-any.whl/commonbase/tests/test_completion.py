import os
import pytest
from commonbase.exceptions import CommonbaseApiException, CommonbaseException
from commonbase.completion import Completion
from commonbase.chat_context import ChatContext, ChatMessage
from commonbase.provider_config import ProviderConfig, OpenAIParams


def test_create_no_api_key():
    with pytest.raises(CommonbaseException):
        Completion.create(
            api_key=None, project_id=os.getenv("CB_PROJECT_ID") or "", prompt=""
        )


def test_create_no_project_id():
    with pytest.raises(CommonbaseApiException):
        Completion.create(api_key=os.getenv("CB_API_KEY") or "", project_id=None, prompt="")  # type: ignore


def test_create_no_prompt():
    with pytest.raises(CommonbaseApiException):
        Completion.create(api_key=os.getenv("CB_API_KEY") or "", project_id=os.getenv("CB_PROJECT_ID") or "", prompt=None)  # type: ignore


def test_stream_no_api_key():
    with pytest.raises(CommonbaseException):
        for _ in Completion.stream(api_key=None, project_id=os.getenv("CB_PROJECT_ID") or "", prompt=""):  # type: ignore
            pass


def test_stream_no_project_id():
    with pytest.raises(CommonbaseApiException):
        for _ in Completion.stream(api_key=os.getenv("CB_API_KEY") or "", project_id=None, prompt=""):  # type: ignore
            pass


def test_stream_no_prompt():
    with pytest.raises(CommonbaseApiException):
        for _ in Completion.stream(api_key=os.getenv("CB_API_KEY") or "", project_id=os.getenv("CB_PROJECT_ID") or "", prompt=None):  # type: ignore
            pass


def test_create_invalid_project_id():
    with pytest.raises(CommonbaseApiException):
        Completion.create(
            api_key=os.getenv("CB_API_KEY") or "", project_id="", prompt="Hello"
        )


def test_stream_invalid_project_id():
    with pytest.raises(CommonbaseApiException):
        for _ in Completion.stream(
            api_key=os.getenv("CB_API_KEY") or "", project_id="", prompt="Hello"
        ):
            pass


def test_completion_prompt():
    result = Completion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        prompt="Hello",
    )

    assert result.completed
    assert result.invocation_id is not None
    assert result.project_id is not None
    assert result.type == "text" or result.type == "chat"
    assert result.model is not None
    assert len(result.choices) > 0

    choice = result.choices[0]

    assert choice.text is not None
    assert choice.index >= 0
    assert choice.finish_reason is not None


def test_completion_response():
    result = Completion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        prompt="Please return the string '123abc' to me without the quotes.",
    )

    assert result.completed and result.best_result.strip() == "123abc"


def test_completion_variables():
    result = Completion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        prompt="My name is {{user_name}} and my email is {{email}}",
        variables={"user_name": "USERNAME", "email": "USER@COMPANY.COM"},
    )

    assert result.completed and result.best_result is not None


def test_completion_stream():
    response_count = 0

    for response in Completion.stream(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        prompt="Tell me about artificial intelligence.",
    ):
        assert len(response.choices) > 0 and response.best_result is not None
        response_count += 1

    assert response_count > 0


def test_completion_context():
    context = ChatContext(
        [
            ChatMessage(role="user", content="Where is Berlin located?"),
            ChatMessage(role="assistant", content="In the EU."),
            ChatMessage(role="user", content="What country?"),
        ]
    )

    result = Completion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        prompt="You help people with geography.",
        chat_context=context,
        provider_config=ProviderConfig(
            provider="cb-openai-eu", params=OpenAIParams(type="chat")
        ),
    )

    assert result.completed and "germany" in result.best_result.lower()
