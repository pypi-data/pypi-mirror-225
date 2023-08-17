from typing import Generator, Optional
import json
import requests
import sseclient
from commonbase.completion_response import CompletionResponse
from commonbase.exceptions import CommonbaseApiException, CommonbaseException
from commonbase.chat_context import ChatContext
from commonbase.provider_config import ProviderConfig
from importlib.metadata import version, PackageNotFoundError


def _get_sdk_version() -> str:
    try:
        return version("commonbase")
    except PackageNotFoundError:
        # This error is thrown during testing.
        return "0.0.0"


def _format_body(
    project_id: str,
    prompt: str,
    variables: Optional[dict[str, str]] = None,
    chat_context: Optional[ChatContext] = None,
    user_id: Optional[str] = None,
    provider_config: Optional[ProviderConfig] = None,
    stream: bool = False,
):
    data = {
        "projectId": project_id,
        "prompt": prompt,
        "variables": variables,
        "context": chat_context._as_json() if chat_context is not None else None,
        "userId": user_id,
        "providerConfig": provider_config._as_json()
        if provider_config is not None
        else None,
        "stream": stream,
    }
    return {k: v for k, v in data.items() if v is not None}


def _send_completion_request(
    api_key: str,
    project_id: str,
    prompt: str,
    variables: Optional[dict[str, str]],
    chat_context: Optional[ChatContext],
    user_id: Optional[str],
    provider_api_key: Optional[str],
    provider_config: Optional[ProviderConfig],
    stream: bool,
) -> requests.Response:
    if api_key is None:
        raise CommonbaseException(
            "A Commonbase API key must be provided with every request."
        )

    data = _format_body(
        project_id=project_id,
        prompt=prompt,
        variables=variables,
        chat_context=chat_context,
        user_id=user_id,
        provider_config=provider_config,
        stream=stream,
    )

    headers = {
        "Authorization": api_key,
        "User-Agent": f"commonbase-python/{_get_sdk_version()}",
    }

    if stream:
        headers["Accept"] = "text/event-stream"

    print(provider_api_key)
    if provider_api_key is not None:
        headers["Provider-API-Key"] = provider_api_key

    return requests.post(
        "https://api.commonbase.com/completions",
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
        chat_context: Optional[ChatContext] = None,
        user_id: Optional[str] = None,
        provider_api_key: Optional[str] = None,
        provider_config: Optional[ProviderConfig] = None,
    ) -> CompletionResponse:
        """Creates a completion for the given prompt.

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
        chat_context : ChatContext, optional
            The list of chat messages in a conversation
        user_id : str, optional
            The User ID that will be logged for the invocation.
        provider_api_key : str, optional
            The API Key used to authenticate with a provider.
        provider_config : ProviderConfig, optional
            Configures the completion provider to use, currently OpenAI or Anthropic.

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
            prompt=prompt,
            variables=variables,
            chat_context=chat_context,
            user_id=user_id,
            provider_api_key=provider_api_key,
            provider_config=provider_config,
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
        prompt: str,
        variables: Optional[dict[str, str]] = None,
        chat_context: Optional[ChatContext] = None,
        user_id: Optional[str] = None,
        provider_api_key: Optional[str] = None,
        provider_config: Optional[ProviderConfig] = None,
    ) -> Generator[CompletionResponse, None, None]:
        """Creates a completion stream for the given prompt.

        This method is identical to Completion.create(), except it returns
        a stream of completion responses.
        """
        response = _send_completion_request(
            api_key=api_key,
            project_id=project_id,
            prompt=prompt,
            variables=variables,
            chat_context=chat_context,
            user_id=user_id,
            provider_api_key=provider_api_key,
            provider_config=provider_config,
            stream=True,
        )

        if response.status_code >= 400:
            raise CommonbaseApiException(response.json())

        client = sseclient.SSEClient(response)
        for event in client.events():
            yield CompletionResponse(json.loads(event.data))
