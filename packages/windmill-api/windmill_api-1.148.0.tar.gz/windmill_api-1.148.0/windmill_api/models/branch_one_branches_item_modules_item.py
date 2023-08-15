from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.branch_one_branches_item_modules_item_mock import BranchOneBranchesItemModulesItemMock
from ..models.branch_one_branches_item_modules_item_retry import BranchOneBranchesItemModulesItemRetry
from ..models.branch_one_branches_item_modules_item_sleep_type_0 import BranchOneBranchesItemModulesItemSleepType0
from ..models.branch_one_branches_item_modules_item_sleep_type_1 import BranchOneBranchesItemModulesItemSleepType1
from ..models.branch_one_branches_item_modules_item_stop_after_if import BranchOneBranchesItemModulesItemStopAfterIf
from ..models.branch_one_branches_item_modules_item_suspend import BranchOneBranchesItemModulesItemSuspend
from ..types import UNSET, Unset

T = TypeVar("T", bound="BranchOneBranchesItemModulesItem")


@attr.s(auto_attribs=True)
class BranchOneBranchesItemModulesItem:
    """
    Attributes:
        id (str):
        value (Any):
        stop_after_if (Union[Unset, BranchOneBranchesItemModulesItemStopAfterIf]):
        sleep (Union[BranchOneBranchesItemModulesItemSleepType0, BranchOneBranchesItemModulesItemSleepType1, Unset]):
        cache_ttl (Union[Unset, float]):
        timeout (Union[Unset, float]):
        summary (Union[Unset, str]):
        mock (Union[Unset, BranchOneBranchesItemModulesItemMock]):
        suspend (Union[Unset, BranchOneBranchesItemModulesItemSuspend]):
        retry (Union[Unset, BranchOneBranchesItemModulesItemRetry]):
    """

    id: str
    value: Any
    stop_after_if: Union[Unset, BranchOneBranchesItemModulesItemStopAfterIf] = UNSET
    sleep: Union[BranchOneBranchesItemModulesItemSleepType0, BranchOneBranchesItemModulesItemSleepType1, Unset] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    timeout: Union[Unset, float] = UNSET
    summary: Union[Unset, str] = UNSET
    mock: Union[Unset, BranchOneBranchesItemModulesItemMock] = UNSET
    suspend: Union[Unset, BranchOneBranchesItemModulesItemSuspend] = UNSET
    retry: Union[Unset, BranchOneBranchesItemModulesItemRetry] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        value = self.value
        stop_after_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_after_if, Unset):
            stop_after_if = self.stop_after_if.to_dict()

        sleep: Union[Dict[str, Any], Unset]
        if isinstance(self.sleep, Unset):
            sleep = UNSET

        elif isinstance(self.sleep, BranchOneBranchesItemModulesItemSleepType0):
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        else:
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        cache_ttl = self.cache_ttl
        timeout = self.timeout
        summary = self.summary
        mock: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mock, Unset):
            mock = self.mock.to_dict()

        suspend: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.suspend, Unset):
            suspend = self.suspend.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
            }
        )
        if stop_after_if is not UNSET:
            field_dict["stop_after_if"] = stop_after_if
        if sleep is not UNSET:
            field_dict["sleep"] = sleep
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if summary is not UNSET:
            field_dict["summary"] = summary
        if mock is not UNSET:
            field_dict["mock"] = mock
        if suspend is not UNSET:
            field_dict["suspend"] = suspend
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        _stop_after_if = d.pop("stop_after_if", UNSET)
        stop_after_if: Union[Unset, BranchOneBranchesItemModulesItemStopAfterIf]
        if isinstance(_stop_after_if, Unset):
            stop_after_if = UNSET
        else:
            stop_after_if = BranchOneBranchesItemModulesItemStopAfterIf.from_dict(_stop_after_if)

        def _parse_sleep(
            data: object,
        ) -> Union[BranchOneBranchesItemModulesItemSleepType0, BranchOneBranchesItemModulesItemSleepType1, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _sleep_type_0 = data
                sleep_type_0: Union[Unset, BranchOneBranchesItemModulesItemSleepType0]
                if isinstance(_sleep_type_0, Unset):
                    sleep_type_0 = UNSET
                else:
                    sleep_type_0 = BranchOneBranchesItemModulesItemSleepType0.from_dict(_sleep_type_0)

                return sleep_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _sleep_type_1 = data
            sleep_type_1: Union[Unset, BranchOneBranchesItemModulesItemSleepType1]
            if isinstance(_sleep_type_1, Unset):
                sleep_type_1 = UNSET
            else:
                sleep_type_1 = BranchOneBranchesItemModulesItemSleepType1.from_dict(_sleep_type_1)

            return sleep_type_1

        sleep = _parse_sleep(d.pop("sleep", UNSET))

        cache_ttl = d.pop("cache_ttl", UNSET)

        timeout = d.pop("timeout", UNSET)

        summary = d.pop("summary", UNSET)

        _mock = d.pop("mock", UNSET)
        mock: Union[Unset, BranchOneBranchesItemModulesItemMock]
        if isinstance(_mock, Unset):
            mock = UNSET
        else:
            mock = BranchOneBranchesItemModulesItemMock.from_dict(_mock)

        _suspend = d.pop("suspend", UNSET)
        suspend: Union[Unset, BranchOneBranchesItemModulesItemSuspend]
        if isinstance(_suspend, Unset):
            suspend = UNSET
        else:
            suspend = BranchOneBranchesItemModulesItemSuspend.from_dict(_suspend)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, BranchOneBranchesItemModulesItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = BranchOneBranchesItemModulesItemRetry.from_dict(_retry)

        branch_one_branches_item_modules_item = cls(
            id=id,
            value=value,
            stop_after_if=stop_after_if,
            sleep=sleep,
            cache_ttl=cache_ttl,
            timeout=timeout,
            summary=summary,
            mock=mock,
            suspend=suspend,
            retry=retry,
        )

        branch_one_branches_item_modules_item.additional_properties = d
        return branch_one_branches_item_modules_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
