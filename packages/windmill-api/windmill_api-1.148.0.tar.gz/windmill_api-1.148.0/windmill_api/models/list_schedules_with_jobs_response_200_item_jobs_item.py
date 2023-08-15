from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ListSchedulesWithJobsResponse200ItemJobsItem")


@attr.s(auto_attribs=True)
class ListSchedulesWithJobsResponse200ItemJobsItem:
    """
    Attributes:
        id (str):
        success (bool):
        duration_ms (float):
    """

    id: str
    success: bool
    duration_ms: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        success = self.success
        duration_ms = self.duration_ms

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "success": success,
                "duration_ms": duration_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        success = d.pop("success")

        duration_ms = d.pop("duration_ms")

        list_schedules_with_jobs_response_200_item_jobs_item = cls(
            id=id,
            success=success,
            duration_ms=duration_ms,
        )

        list_schedules_with_jobs_response_200_item_jobs_item.additional_properties = d
        return list_schedules_with_jobs_response_200_item_jobs_item

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
