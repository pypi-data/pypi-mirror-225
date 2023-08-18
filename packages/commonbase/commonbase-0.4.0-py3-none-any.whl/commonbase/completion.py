import json
import requests
import sseclient  # type: ignore
from typing import Generator, Optional, Any, Literal
from importlib.metadata import version, PackageNotFoundError
from commonbase.completion_response import CompletionResponse
from commonbase.exceptions import CommonbaseApiException, CommonbaseException
from commonbase.chat_context import ChatMessage, FunctionCallConfig, ChatFunction
from commonbase.provider_config import ProviderName, ProviderParams

_API_BASE_URL = "https://api.commonbase.com"

_RequestType = Literal["text", "chat", "embeddings"]


def _get_sdk_version() -> str:
    try:
        return version("commonbase")
    except PackageNotFoundError:
        # This error is thrown during testing.
        return "0.0.0"


def _get_default_provider_model(provider: str, type: _RequestType, hasFunctions: bool):
    if "openai" in provider:
        if type == "text":
            return "text-davinci-003"
        if type == "chat":
            return "gpt-4" if hasFunctions else "gpt-3.5-turbo"
        if type == "embeddings":
            return "text-embedding-ada-002"
    if "anthropic" in provider:
        return "claude-v1"


def _format_body(
    project_id: str,
    type: _RequestType,
    prompt: Optional[str],
    messages: Optional[list[ChatMessage]],
    functions: Optional[list[ChatFunction]],
    function_call: Optional[FunctionCallConfig],
    variables: Optional[dict[str, str]],
    user_id: Optional[str],
    provider: Optional[ProviderName],
    provider_model: Optional[str],
    provider_params: Optional[ProviderParams],
    stream: bool = False,
) -> dict[str, Any]:
    providerName = (
        provider
        if provider is not None
        else ("cb-openai-us" if functions is not None else "cb-openai-eu")
    )
    providerModel = (
        provider_model
        if provider_model is not None
        else _get_default_provider_model(providerName, type, functions is not None)
    )
    providerParams = {
        **(provider_params if provider_params is not None else {}),
        "type": type,
        "model": providerModel,
    }

    data: dict[str, Any] = {
        "projectId": project_id,
        "prompt": prompt,
        "messages": messages,
        "functions": functions,
        "functionCall": function_call,
        "variables": variables,
        "userId": user_id,
        "providerConfig": {
            "provider": providerName,
            "params": providerParams,
        },
        "stream": stream,
    }
    return {k: v for k, v in data.items() if v is not None}


def _send_completion_request(
    api_key: str,
    project_id: str,
    type: _RequestType,
    prompt: Optional[str],
    messages: Optional[list[ChatMessage]],
    functions: Optional[list[ChatFunction]],
    function_call: Optional[FunctionCallConfig],
    variables: Optional[dict[str, str]],
    user_id: Optional[str],
    provider_api_key: Optional[str],
    provider: Optional[ProviderName],
    provider_model: Optional[str],
    provider_params: Optional[ProviderParams],
    stream: bool,
) -> requests.Response:
    if api_key is None:  # type: ignore
        raise CommonbaseException(
            "A Commonbase API key must be provided with every request."
        )

    data = _format_body(
        project_id=project_id,
        type=type,
        prompt=prompt,
        messages=messages,
        functions=functions,
        function_call=function_call,
        variables=variables,
        user_id=user_id,
        provider=provider,
        provider_model=provider_model,
        provider_params=provider_params,
        stream=stream,
    )

    headers = {
        "Authorization": api_key,
        "User-Agent": f"commonbase-python/{_get_sdk_version()}",
    }

    if stream:
        headers["Accept"] = "text/event-stream"

    if provider_api_key is not None:
        headers["Provider-API-Key"] = provider_api_key

    return requests.post(
        f"{_API_BASE_URL}/completions",
        stream=stream,
        json=data,
        headers=headers,
    )


class Completion:
    @classmethod
    def create(
        cls,
        api_key: str,
        project_id: str,
        prompt: str,
        variables: Optional[dict[str, str]] = None,
        user_id: Optional[str] = None,
        provider_api_key: Optional[str] = None,
        provider: Optional[ProviderName] = None,
        provider_model: Optional[str] = None,
        provider_params: Optional[ProviderParams] = None,
    ) -> CompletionResponse:
        """Creates a text completion for the given prompt.

        Parameters
        ----------
        api_key : str
            The Commonbase API key used to authenticate the request.
        project_id : str
            The ID of the Commonbase project.
        prompt : str
            The prompt for which a completion is generated.
        variables : dict[str, str], optional
            The list of variables to use with Commonbase managed prompts.
        user_id : str, optional
            The User ID that will be logged for the invocation.
        provider_api_key : str, optional
            The API Key used to authenticate with a provider.
        provider: str, optional
            The provider to use for the completion.
        provider_model: str, optional
            The provider model to use for the completion.
        provider_params: ProviderParams, optional
            The configuration parameters for the provider.

        Raises
        ------
        CommonbaseException
            If the request parameters are invalid.
        CommonbaseApiException
            If there is an API error.
        """

        response = _send_completion_request(
            api_key=api_key,
            project_id=project_id,
            type="text",
            prompt=prompt,
            messages=None,
            functions=None,
            function_call=None,
            variables=variables,
            user_id=user_id,
            provider_api_key=provider_api_key,
            provider=provider,
            provider_model=provider_model,
            provider_params=provider_params,
            stream=False,
        )

        json = response.json()

        if response.status_code >= 400 or "error" in json:
            raise CommonbaseApiException(json)

        return CompletionResponse(response.json())

    # @classmethod
    # def stream(
    #     cls,
    #     api_key: str,
    #     project_id: str,
    #     prompt: str,
    #     variables: Optional[dict[str, str]] = None,
    #     user_id: Optional[str] = None,
    #     provider_api_key: Optional[str] = None,
    #     provider: Optional[ProviderName] = None,
    #     provider_model: Optional[str] = None,
    #     provider_params: Optional[ProviderParams] = None,
    # ) -> Generator[CompletionResponse, None, None]:
    #     """Creates a completion stream for the given prompt.

    #     This method is identical to Completion.create(), except it returns
    #     a stream of completion responses.
    #     """
    #     response = _send_completion_request(
    #         api_key=api_key,
    #         project_id=project_id,
    #         type="text",
    #         prompt=prompt,
    #         messages=None,
    #         functions=None,
    #         function_call=None,
    #         variables=variables,
    #         user_id=user_id,
    #         provider_api_key=provider_api_key,
    #         provider=provider,
    #         provider_model=provider_model,
    #         provider_params=provider_params,
    #         stream=True,
    #     )

    #     if response.status_code >= 400:
    #         raise CommonbaseApiException(response.json())

    #     client = sseclient.SSEClient(response)
    #     for event in client.events():
    #         yield CompletionResponse(json.loads(event.data))


class ChatCompletion:
    @classmethod
    def create(
        cls,
        api_key: str,
        project_id: str,
        messages: list[ChatMessage],
        functions: Optional[list[ChatFunction]] = None,
        function_call: Optional[FunctionCallConfig] = None,
        user_id: Optional[str] = None,
        provider_api_key: Optional[str] = None,
        provider: Optional[ProviderName] = None,
        provider_model: Optional[str] = None,
        provider_params: Optional[ProviderParams] = None,
    ) -> CompletionResponse:
        """Creates a chat completion for the given messages.

        Parameters
        ----------
        api_key : str
            The Commonbase API key used to authenticate the request.
        project_id : str
            The ID of the Commonbase project.
        prompt : str
            The prompt for which a completion is generated.
        variables : dict[str, str], optional
            The list of variables to use with Commonbase managed prompts.
        messages : list[ChatMessage]
            The list of chat messages in a conversation
        functions: list[ChatFunction], optional
            The list of functions that the LLM can call.
        function_call: FunctionCallConfig, optional
            The function call configuration.
        user_id : str, optional
            The User ID that will be logged for the invocation.
        provider_api_key : str, optional
            The API Key used to authenticate with a provider.
        provider: str, optional
            The provider to use for the completion.
        provider_model: str, optional
            The provider model to use for the completion.
        provider_params: ProviderParams, optional
            The configuration parameters for the provider.

        Raises
        ------
        CommonbaseException
            If the request parameters are invalid.
        CommonbaseApiException
            If there is an API error.
        """

        response = _send_completion_request(
            api_key=api_key,
            project_id=project_id,
            type="chat",
            prompt=None,
            messages=messages,
            functions=functions,
            function_call=function_call,
            variables=None,
            user_id=user_id,
            provider_api_key=provider_api_key,
            provider=provider,
            provider_model=provider_model,
            provider_params=provider_params,
            stream=False,
        )

        json = response.json()

        if response.status_code >= 400 or "error" in json:
            raise CommonbaseApiException(json)

        return CompletionResponse(response.json())

    @classmethod
    def stream(
        cls,
        api_key: str,
        project_id: str,
        messages: list[ChatMessage],
        functions: Optional[list[ChatFunction]] = None,
        function_call: Optional[FunctionCallConfig] = None,
        user_id: Optional[str] = None,
        provider_api_key: Optional[str] = None,
        provider: Optional[ProviderName] = None,
        provider_model: Optional[str] = None,
        provider_params: Optional[ProviderParams] = None,
    ) -> Generator[CompletionResponse, None, None]:
        """Creates a chat completion stream for the given messages.

        This method is identical to Completion.create(), except it returns
        a stream of completion responses.
        """
        response = _send_completion_request(
            api_key=api_key,
            project_id=project_id,
            type="chat",
            prompt=None,
            messages=messages,
            functions=functions,
            function_call=function_call,
            variables=None,
            user_id=user_id,
            provider_api_key=provider_api_key,
            provider=provider,
            provider_model=provider_model,
            provider_params=provider_params,
            stream=True,
        )

        if response.status_code >= 400:
            raise CommonbaseApiException(response.json())

        client = sseclient.SSEClient(response)
        for event in client.events():
            yield CompletionResponse(json.loads(event.data))
