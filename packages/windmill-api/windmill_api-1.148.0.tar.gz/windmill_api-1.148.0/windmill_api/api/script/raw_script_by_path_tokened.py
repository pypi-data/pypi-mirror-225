from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    workspace: str,
    token: str,
    path: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/scripts_u/tokened_raw/{workspace}/{token}/{path}".format(
        client.base_url, workspace=workspace, token=token, path=path
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    token: str,
    path: str,
    *,
    client: Client,
) -> Response[Any]:
    """raw script by path with a token (mostly used by lsp to be used with import maps to resolve scripts)

    Args:
        workspace (str):
        token (str):
        path (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        token=token,
        path=path,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    workspace: str,
    token: str,
    path: str,
    *,
    client: Client,
) -> Response[Any]:
    """raw script by path with a token (mostly used by lsp to be used with import maps to resolve scripts)

    Args:
        workspace (str):
        token (str):
        path (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        token=token,
        path=path,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
