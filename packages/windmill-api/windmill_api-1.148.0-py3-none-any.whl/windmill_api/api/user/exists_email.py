from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    email: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/users/exists/{email}".format(client.base_url, email=email)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[bool]:
    if response.status_code == 200:
        response_200 = cast(bool, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[bool]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    email: str,
    *,
    client: Client,
) -> Response[bool]:
    """exists email

    Args:
        email (str):

    Returns:
        Response[bool]
    """

    kwargs = _get_kwargs(
        email=email,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    email: str,
    *,
    client: Client,
) -> Optional[bool]:
    """exists email

    Args:
        email (str):

    Returns:
        Response[bool]
    """

    return sync_detailed(
        email=email,
        client=client,
    ).parsed


async def asyncio_detailed(
    email: str,
    *,
    client: Client,
) -> Response[bool]:
    """exists email

    Args:
        email (str):

    Returns:
        Response[bool]
    """

    kwargs = _get_kwargs(
        email=email,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    email: str,
    *,
    client: Client,
) -> Optional[bool]:
    """exists email

    Args:
        email (str):

    Returns:
        Response[bool]
    """

    return (
        await asyncio_detailed(
            email=email,
            client=client,
        )
    ).parsed
