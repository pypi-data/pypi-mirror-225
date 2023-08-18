import os
from commonbase.completion import ChatCompletion


def test_functions_api():
    result = ChatCompletion.create(
        api_key=os.getenv("CB_API_KEY") or "",
        project_id=os.getenv("CB_PROJECT_ID") or "",
        messages=[
            {
                "role": "system",
                "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
            },
            {"role": "user", "content": "What's the weather like today?"},
            {
                "role": "assistant",
                "content": "Sure, can you please provide me with the location?",
            },
            {"role": "user", "content": "I am in Berlin, Germany"},
            {
                "role": "assistant",
                "content": None,
                "function_call": {
                    "name": "get_current_weather",
                    "arguments": '{\\n  "location": "Berlin, Germany",\\n  "format": "celsius"\\n}',
                },
            },
            {
                "role": "function",
                "name": "get_current_weather",
                "content": "sunny, 30°C, 5% changes of rain",
            },
            {
                "role": "user",
                "content": "Thanks, how is the weather in New York today?",
            },
        ],
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "format": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The temperature unit to use. Infer this from the users location.",
                        },
                    },
                    "required": ["location", "format"],
                },
            }
        ],
    )

    assert result.best_choice.function_call is not None
    assert result.best_choice.function_call.name == "get_current_weather"
    assert "location" in result.best_choice.function_call.arguments
    assert "format" in result.best_choice.function_call.arguments
