from commonbase.chat_context import ChatContext, ChatMessage
from commonbase.provider_config import ProviderConfig, OpenAIParams
from commonbase.completion import _format_body
from dataclasses import asdict


def test_chat_context_json_format():
    context = asdict(
        ChatContext(
            messages=[
                ChatMessage(role="system", content="system message"),
                ChatMessage(role="user", content="user message"),
            ]
        )
    )

    assert "messages" in context and len(context["messages"]) == 2

    systemMessage = context["messages"][0]
    userMessage = context["messages"][1]

    assert (
        isinstance(systemMessage, dict)
        and systemMessage["role"] == "system"
        and systemMessage["content"] == "system message"
    )
    assert (
        isinstance(userMessage, dict)
        and userMessage["role"] == "user"
        and userMessage["content"] == "user message"
    )


def test_request_body_format():
    body = _format_body(
        project_id="<project_id>",
        prompt="<prompt>",
        variables={"test1": "value"},
        chat_context=ChatContext([ChatMessage(role="system", content="<content>")]),
        user_id="<userId>",
        provider_config=ProviderConfig(
            provider="cb-openai-eu",
            params=OpenAIParams(type="chat", model="model_name"),
        ),
        stream=True,
    )

    assert body == {
        "projectId": "<project_id>",
        "prompt": "<prompt>",
        "variables": {"test1": "value"},
        "context": {"messages": [{"role": "system", "content": "<content>"}]},
        "userId": "<userId>",
        "providerConfig": {
            "provider": "cb-openai-eu",
            "params": {"type": "chat", "model": "model_name"},
        },
        "stream": True,
    }
