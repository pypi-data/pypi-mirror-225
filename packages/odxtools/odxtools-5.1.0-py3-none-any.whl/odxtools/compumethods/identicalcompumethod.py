# SPDX-License-Identifier: MIT
from typing import Union

from ..odxtypes import DataType
from .compumethod import CompuMethod


class IdenticalCompuMethod(CompuMethod):

    def __init__(self, *, internal_type: Union[DataType, str], physical_type: Union[DataType, str]):
        super().__init__(
            internal_type=internal_type, physical_type=physical_type, category="IDENTICAL")

    def convert_physical_to_internal(self, physical_value):
        return physical_value

    def convert_internal_to_physical(self, internal_value):
        return internal_value

    def is_valid_physical_value(self, physical_value):
        return self.physical_type.isinstance(physical_value)

    def is_valid_internal_value(self, internal_value):
        return self.internal_type.isinstance(internal_value)
