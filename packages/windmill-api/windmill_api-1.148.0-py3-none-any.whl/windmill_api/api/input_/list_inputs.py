from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.list_inputs_response_200_item import ListInputsResponse200Item
from ...models.list_inputs_runnable_type import ListInputsRunnableType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    client: Client,
    runnable_id: Union[Unset, None, str] = UNSET,
    runnable_type: Union[Unset, None, ListInputsRunnableType] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/inputs/list".format(client.base_url, workspace=workspace)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["runnable_id"] = runnable_id

    json_runnable_type: Union[Unset, None, str] = UNSET
    if not isinstance(runnable_type, Unset):
        json_runnable_type = runnable_type.value if runnable_type else None

    params["runnable_type"] = json_runnable_type

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[ListInputsResponse200Item]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListInputsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[ListInputsResponse200Item]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Client,
    runnable_id: Union[Unset, None, str] = UNSET,
    runnable_type: Union[Unset, None, ListInputsRunnableType] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Response[List[ListInputsResponse200Item]]:
    """List saved Inputs for a Runnable

    Args:
        workspace (str):
        runnable_id (Union[Unset, None, str]):
        runnable_type (Union[Unset, None, ListInputsRunnableType]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):

    Returns:
        Response[List[ListInputsResponse200Item]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        runnable_id=runnable_id,
        runnable_type=runnable_type,
        page=page,
        per_page=per_page,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    workspace: str,
    *,
    client: Client,
    runnable_id: Union[Unset, None, str] = UNSET,
    runnable_type: Union[Unset, None, ListInputsRunnableType] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Optional[List[ListInputsResponse200Item]]:
    """List saved Inputs for a Runnable

    Args:
        workspace (str):
        runnable_id (Union[Unset, None, str]):
        runnable_type (Union[Unset, None, ListInputsRunnableType]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):

    Returns:
        Response[List[ListInputsResponse200Item]]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        runnable_id=runnable_id,
        runnable_type=runnable_type,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Client,
    runnable_id: Union[Unset, None, str] = UNSET,
    runnable_type: Union[Unset, None, ListInputsRunnableType] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Response[List[ListInputsResponse200Item]]:
    """List saved Inputs for a Runnable

    Args:
        workspace (str):
        runnable_id (Union[Unset, None, str]):
        runnable_type (Union[Unset, None, ListInputsRunnableType]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):

    Returns:
        Response[List[ListInputsResponse200Item]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        runnable_id=runnable_id,
        runnable_type=runnable_type,
        page=page,
        per_page=per_page,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    workspace: str,
    *,
    client: Client,
    runnable_id: Union[Unset, None, str] = UNSET,
    runnable_type: Union[Unset, None, ListInputsRunnableType] = UNSET,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
) -> Optional[List[ListInputsResponse200Item]]:
    """List saved Inputs for a Runnable

    Args:
        workspace (str):
        runnable_id (Union[Unset, None, str]):
        runnable_type (Union[Unset, None, ListInputsRunnableType]):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):

    Returns:
        Response[List[ListInputsResponse200Item]]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            runnable_id=runnable_id,
            runnable_type=runnable_type,
            page=page,
            per_page=per_page,
        )
    ).parsed
