import os
import pytest
from commonbase.exceptions import CommonbaseApiException, CommonbaseException
from commonbase.completion import ChatCompletion


def test_create_no_api_key():
    with pytest.raises(CommonbaseException):
        ChatCompletion.create(
            api_key=None, project_id=os.getenv("CB_PROJECT_ID") or "", messages=[]  # type: ignore
        )


def test_create_no_project_id():
    with pytest.raises(CommonbaseApiException):
        ChatCompletion.create(
            api_key=os.getenv("CB_API_KEY") or "", project_id=None, messages=[]  # type: ignore
        )


def test_create_no_prompt():
    with pytest.raises(CommonbaseApiException):
        ChatCompletion.create(
            api_key=os.getenv("CB_API_KEY") or "",
            project_id=os.getenv("CB_PROJECT_ID") or "",
            messages=None,  # type: ignore
        )


def test_stream_no_api_key():
    with pytest.raises(CommonbaseException):
        for _ in ChatCompletion.stream(
            api_key=None, project_id=os.getenv("CB_PROJECT_ID") or "", messages=[]  # type: ignore
        ):
            pass


def test_stream_no_project_id():
    with pytest.raises(CommonbaseApiException):
        for _ in ChatCompletion.stream(
            api_key=os.getenv("CB_API_KEY") or "", project_id=None, messages=[]  # type: ignore
        ):
            pass


def test_stream_no_prompt():
    with pytest.raises(CommonbaseApiException):
        for _ in ChatCompletion.stream(
            api_key=os.getenv("CB_API_KEY") or "",
            project_id=os.getenv("CB_PROJECT_ID") or "",
            messages=None,  # type: ignore
        ):
            pass


def test_create_invalid_project_id():
    with pytest.raises(CommonbaseApiException):
        ChatCompletion.create(
            api_key=os.getenv("CB_API_KEY") or "",
            project_id="",
            messages=[{"role": "user", "content": "Hello"}],
        )


def test_stream_invalid_project_id():
    with pytest.raises(CommonbaseApiException):
        for _ in ChatCompletion.stream(
            api_key=os.getenv("CB_API_KEY") or "",
            project_id="",
            messages=[{"role": "user", "content": "Hello"}],
        ):
            pass


def test_chat_completion_prompt():
    result = ChatCompletion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        messages=[{"role": "user", "content": "Hello"}],
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


def test_chat_completion_response():
    result = ChatCompletion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        messages=[
            {
                "role": "user",
                "content": "Please return the string '123abc' to me without the quotes.",
            }
        ],
    )

    assert result.completed and result.best_choice.text.strip() == "123abc"


def test_chat_completion_stream():
    response_count = 0

    for response in ChatCompletion.stream(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        messages=[
            {"role": "user", "content": "Tell me about artificial intelligence."}
        ],
    ):
        assert len(response.choices) > 0 and response.best_choice.text is not None
        response_count += 1

    assert response_count > 0


def test_completion_chat():
    result = ChatCompletion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        messages=[
            {"role": "system", "content": "You help people with geography."},
            {"role": "user", "content": "Where is Berlin located?"},
            {"role": "assistant", "content": "In the EU."},
            {"role": "user", "content": "What country?"},
        ],
        provider="cb-openai-eu",
    )

    assert result.completed and "germany" in result.best_choice.text.lower()
