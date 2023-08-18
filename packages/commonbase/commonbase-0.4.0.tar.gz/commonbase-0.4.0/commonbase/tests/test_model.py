from commonbase.completion import _format_body  # type: ignore


def test_request_body_format():
    body = _format_body(
        project_id="<project_id>",
        type="chat",
        prompt="<prompt>",
        variables={"test1": "value"},
        messages=[{"role": "user", "content": "test content"}],
        functions=[
            {
                "description": "test description",
                "name": "func_name",
                "parameters": {"test": "test"},
            }
        ],
        function_call="auto",
        user_id="<userId>",
        provider="cb-openai-eu",
        provider_model="model_name",
        provider_params={"max_tokens": 10},
        stream=True,
    )

    assert body == {
        "projectId": "<project_id>",
        "prompt": "<prompt>",
        "variables": {"test1": "value"},
        "messages": [{"role": "user", "content": "test content"}],
        "functions": [
            {
                "description": "test description",
                "name": "func_name",
                "parameters": {"test": "test"},
            }
        ],
        "functionCall": "auto",
        "userId": "<userId>",
        "providerConfig": {
            "provider": "cb-openai-eu",
            "params": {"type": "chat", "model": "model_name", "max_tokens": 10},
        },
        "stream": True,
    }
