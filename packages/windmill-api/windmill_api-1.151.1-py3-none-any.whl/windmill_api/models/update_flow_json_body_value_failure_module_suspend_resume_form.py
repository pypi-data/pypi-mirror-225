from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.update_flow_json_body_value_failure_module_suspend_resume_form_schema import (
    UpdateFlowJsonBodyValueFailureModuleSuspendResumeFormSchema,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateFlowJsonBodyValueFailureModuleSuspendResumeForm")


@attr.s(auto_attribs=True)
class UpdateFlowJsonBodyValueFailureModuleSuspendResumeForm:
    """
    Attributes:
        schema (Union[Unset, UpdateFlowJsonBodyValueFailureModuleSuspendResumeFormSchema]):
    """

    schema: Union[Unset, UpdateFlowJsonBodyValueFailureModuleSuspendResumeFormSchema] = UNSET
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
        schema: Union[Unset, UpdateFlowJsonBodyValueFailureModuleSuspendResumeFormSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = UpdateFlowJsonBodyValueFailureModuleSuspendResumeFormSchema.from_dict(_schema)

        update_flow_json_body_value_failure_module_suspend_resume_form = cls(
            schema=schema,
        )

        update_flow_json_body_value_failure_module_suspend_resume_form.additional_properties = d
        return update_flow_json_body_value_failure_module_suspend_resume_form

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
