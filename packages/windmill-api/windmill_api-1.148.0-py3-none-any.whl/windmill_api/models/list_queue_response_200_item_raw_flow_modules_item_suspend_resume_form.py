from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.list_queue_response_200_item_raw_flow_modules_item_suspend_resume_form_schema import (
    ListQueueResponse200ItemRawFlowModulesItemSuspendResumeFormSchema,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListQueueResponse200ItemRawFlowModulesItemSuspendResumeForm")


@attr.s(auto_attribs=True)
class ListQueueResponse200ItemRawFlowModulesItemSuspendResumeForm:
    """
    Attributes:
        schema (Union[Unset, ListQueueResponse200ItemRawFlowModulesItemSuspendResumeFormSchema]):
    """

    schema: Union[Unset, ListQueueResponse200ItemRawFlowModulesItemSuspendResumeFormSchema] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, ListQueueResponse200ItemRawFlowModulesItemSuspendResumeFormSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = ListQueueResponse200ItemRawFlowModulesItemSuspendResumeFormSchema.from_dict(_schema)

        list_queue_response_200_item_raw_flow_modules_item_suspend_resume_form = cls(
            schema=schema,
        )

        list_queue_response_200_item_raw_flow_modules_item_suspend_resume_form.additional_properties = d
        return list_queue_response_200_item_raw_flow_modules_item_suspend_resume_form

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
