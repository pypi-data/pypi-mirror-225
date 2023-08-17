# Commonbase Python SDK

[![PyPI version](https://badge.fury.io/py/commonbase.svg)](https://badge.fury.io/py/commonbase)

Commonbase allows developers to integrate with any popular LLM API provider
without needing to change any code. The SDK helps with collecting data and
feedback from the users and helps you fine-tune models for your specific use case.

## Installation

```
pip install commonbase
```

## Usage

A Project ID and API Key are required for all Commonbase requests. You can find your project ID and generate an API key in the [Commonbase Dashboard](https://commonbase.com/).

To create a completion, provide your Project ID, API Key, and prompt to `Completion.create`.

```py
import commonbase

result = commonbase.Completion.create(
    api_key="API_KEY",
    project_id="PROJECT_ID",
    prompt="Hello!"
)

print(result.best_result)
```

To stream a completion as it is generated, use `Completion.stream`.

For more examples, see [/examples](https://github.com/commonbaseapp/commonbase-python/tree/main/examples) or check out our [Docs](https://docs.commonbase.com/quickstart/python).
