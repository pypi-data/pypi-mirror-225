from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.get_flow_by_path_with_draft_response_200_draft_value_modules_item_suspend_resume_form_schema import (
    GetFlowByPathWithDraftResponse200DraftValueModulesItemSuspendResumeFormSchema,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFlowByPathWithDraftResponse200DraftValueModulesItemSuspendResumeForm")


@attr.s(auto_attribs=True)
class GetFlowByPathWithDraftResponse200DraftValueModulesItemSuspendResumeForm:
    """
    Attributes:
        schema (Union[Unset, GetFlowByPathWithDraftResponse200DraftValueModulesItemSuspendResumeFormSchema]):
    """

    schema: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueModulesItemSuspendResumeFormSchema] = UNSET
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
        schema: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueModulesItemSuspendResumeFormSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = GetFlowByPathWithDraftResponse200DraftValueModulesItemSuspendResumeFormSchema.from_dict(_schema)

        get_flow_by_path_with_draft_response_200_draft_value_modules_item_suspend_resume_form = cls(
            schema=schema,
        )

        get_flow_by_path_with_draft_response_200_draft_value_modules_item_suspend_resume_form.additional_properties = d
        return get_flow_by_path_with_draft_response_200_draft_value_modules_item_suspend_resume_form

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
