from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditErrorHandlerJsonBody")


@attr.s(auto_attribs=True)
class EditErrorHandlerJsonBody:
    """
    Attributes:
        error_handler (Union[Unset, str]):
    """

    error_handler: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        error_handler = self.error_handler

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error_handler is not UNSET:
            field_dict["error_handler"] = error_handler

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        error_handler = d.pop("error_handler", UNSET)

        edit_error_handler_json_body = cls(
            error_handler=error_handler,
        )

        edit_error_handler_json_body.additional_properties = d
        return edit_error_handler_json_body

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
