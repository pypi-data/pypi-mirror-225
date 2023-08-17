"""Type relay.component.gt, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gwproto.data_classes.components.relay_component import RelayComponent
from gwproto.errors import SchemaError


def check_is_uuid_canonical_textual(v: str) -> None:
    """Checks UuidCanonicalTextual format

    UuidCanonicalTextual format:  A string of hex words separated by hyphens
    of length 8-4-4-4-12.

    Args:
        v (str): the candidate

    Raises:
        ValueError: if v is not UuidCanonicalTextual format
    """
    try:
        x = v.split("-")
    except AttributeError as e:
        raise ValueError(f"Failed to split on -: {e}")
    if len(x) != 5:
        raise ValueError(f"{v} split by '-' did not have 5 words")
    for hex_word in x:
        try:
            int(hex_word, 16)
        except ValueError:
            raise ValueError(f"Words of {v} are not all hex")
    if len(x[0]) != 8:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[1]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[2]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[3]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[4]) != 12:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")


class RelayComponentGt(BaseModel):
    """Type for tracking Relay Components.

    GridWorks Spaceheat SCADA uses the GridWorks GNodeRegistry structures and abstractions for managing relational device data. The Component associated to a SpaceheatNode is part of this structure.
    [More info](https://g-node-registry.readthedocs.io/en/latest/component.html).
    """

    ComponentId: str = Field(
        title="ComponentId",
    )
    ComponentAttributeClassId: str = Field(
        title="ComponentAttributeClassId",
    )
    DisplayName: Optional[str] = Field(
        title="DisplayName",
        default=None,
    )
    Gpio: Optional[int] = Field(
        title="Gpio",
        default=None,
    )
    HwUid: Optional[str] = Field(
        title="HwUid",
        default=None,
    )
    NormallyOpen: bool = Field(
        title="Normally Open",
        description="Normally open relays default in the open position, meaning that when they're not in use, there is no contact between the circuits. When power is introduced, an electromagnet pulls the first circuit into contact with the second, thereby closing the circuit and allowing power to flow through",
    )
    TypeName: Literal["relay.component.gt"] = "relay.component.gt"
    Version: str = "000"

    @validator("ComponentId")
    def _check_component_id(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"ComponentId failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("ComponentAttributeClassId")
    def _check_component_attribute_class_id(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"ComponentAttributeClassId failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        if d["DisplayName"] is None:
            del d["DisplayName"]
        if d["Gpio"] is None:
            del d["Gpio"]
        if d["HwUid"] is None:
            del d["HwUid"]
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class RelayComponentGt_Maker:
    type_name = "relay.component.gt"
    version = "000"

    def __init__(
        self,
        component_id: str,
        component_attribute_class_id: str,
        display_name: Optional[str],
        gpio: Optional[int],
        hw_uid: Optional[str],
        normally_open: bool,
    ):
        self.tuple = RelayComponentGt(
            ComponentId=component_id,
            ComponentAttributeClassId=component_attribute_class_id,
            DisplayName=display_name,
            Gpio=gpio,
            HwUid=hw_uid,
            NormallyOpen=normally_open,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: RelayComponentGt) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> RelayComponentGt:
        """
        Given a serialized JSON type object, returns the Python class object
        """
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> RelayComponentGt:
        d2 = dict(d)
        if "ComponentId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ComponentId")
        if "ComponentAttributeClassId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ComponentAttributeClassId")
        if "DisplayName" not in d2.keys():
            d2["DisplayName"] = None
        if "Gpio" not in d2.keys():
            d2["Gpio"] = None
        if "HwUid" not in d2.keys():
            d2["HwUid"] = None
        if "NormallyOpen" not in d2.keys():
            raise SchemaError(f"dict {d2} missing NormallyOpen")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return RelayComponentGt(
            ComponentId=d2["ComponentId"],
            ComponentAttributeClassId=d2["ComponentAttributeClassId"],
            DisplayName=d2["DisplayName"],
            Gpio=d2["Gpio"],
            HwUid=d2["HwUid"],
            NormallyOpen=d2["NormallyOpen"],
            TypeName=d2["TypeName"],
            Version="000",
        )

    @classmethod
    def tuple_to_dc(cls, t: RelayComponentGt) -> RelayComponent:
        if t.ComponentId in RelayComponent.by_id.keys():
            dc = RelayComponent.by_id[t.ComponentId]
        else:
            dc = RelayComponent(
                component_id=t.ComponentId,
                component_attribute_class_id=t.ComponentAttributeClassId,
                display_name=t.DisplayName,
                gpio=t.Gpio,
                hw_uid=t.HwUid,
                normally_open=t.NormallyOpen,
            )

        return dc

    @classmethod
    def dc_to_tuple(cls, dc: RelayComponent) -> RelayComponentGt:
        t = RelayComponentGt_Maker(
            component_id=dc.component_id,
            component_attribute_class_id=dc.component_attribute_class_id,
            display_name=dc.display_name,
            gpio=dc.gpio,
            hw_uid=dc.hw_uid,
            normally_open=dc.normally_open,
        ).tuple
        return t

    @classmethod
    def type_to_dc(cls, t: str) -> RelayComponent:
        return cls.tuple_to_dc(cls.type_to_tuple(t))

    @classmethod
    def dc_to_type(cls, dc: RelayComponent) -> str:
        return cls.dc_to_tuple(dc).as_type()

    @classmethod
    def dict_to_dc(cls, d: dict[Any, str]) -> RelayComponent:
        return cls.tuple_to_dc(cls.dict_to_tuple(d))
