from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.create_resource_json_body import CreateResourceJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    client: Client,
    json_body: CreateResourceJsonBody,
    update_if_exists: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/resources/create".format(client.base_url, workspace=workspace)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["update_if_exists"] = update_if_exists

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    workspace: str,
    *,
    client: Client,
    json_body: CreateResourceJsonBody,
    update_if_exists: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """create resource

    Args:
        workspace (str):
        update_if_exists (Union[Unset, None, bool]):
        json_body (CreateResourceJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        json_body=json_body,
        update_if_exists=update_if_exists,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    workspace: str,
    *,
    client: Client,
    json_body: CreateResourceJsonBody,
    update_if_exists: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """create resource

    Args:
        workspace (str):
        update_if_exists (Union[Unset, None, bool]):
        json_body (CreateResourceJsonBody):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        json_body=json_body,
        update_if_exists=update_if_exists,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
