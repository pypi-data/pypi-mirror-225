from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDeployToResponse200")


@attr.s(auto_attribs=True)
class GetDeployToResponse200:
    """
    Attributes:
        deploy_to (Union[Unset, str]):
    """

    deploy_to: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        deploy_to = self.deploy_to

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deploy_to is not UNSET:
            field_dict["deploy_to"] = deploy_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        deploy_to = d.pop("deploy_to", UNSET)

        get_deploy_to_response_200 = cls(
            deploy_to=deploy_to,
        )

        get_deploy_to_response_200.additional_properties = d
        return get_deploy_to_response_200

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
