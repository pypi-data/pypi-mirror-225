import os
import pytest
from commonbase.exceptions import CommonbaseApiException
from commonbase.completion import Completion


def test_provider_with_no_api_key():
    with pytest.raises(CommonbaseApiException):
        Completion.create(
            api_key=os.getenv("CB_API_KEY") or "",
            project_id=os.getenv("CB_PROJECT_ID") or "",
            provider="openai",
            prompt="",
        )


def test_provider_with_valid_api_key():
    result = Completion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        provider_api_key=os.getenv("CB_OPENAI_API_KEY") or "",
        provider="openai",
        prompt="Please return the string '123abc' to me without the quotes.",
        provider_model="text-davinci-002",
    )

    assert result.completed and result.best_choice.text.strip() == "123abc"
