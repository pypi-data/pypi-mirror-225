from typing import Optional

from deci_common.abstractions.base_model import Schema
from deci_common.data_types.enum.hardware_enums import (
    HardwareGroup,
    HardwareMachineModel,
    HardwareType,
    HardwareTypeLabel,
    HardwareVendor,
)


class HardwareReturnSchema(Schema):
    """
    A logic schema of hardware
    """

    name: HardwareType
    label: HardwareTypeLabel
    vendor: Optional[HardwareVendor] = None
    machine: Optional[HardwareMachineModel] = None
    group: Optional[HardwareGroup] = None
    future: bool = False
    deprecated: bool = False
