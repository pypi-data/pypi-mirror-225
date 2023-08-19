"""
variable_len_array_codec.py
---------------------------

module for VariableLenArrayCodec
"""

from __future__ import annotations
from typing import Any
from bitstring import BitArray, ConstBitStream
from .field_codec import FieldCodec
from .varint_codec import VarintCodec
import ltcodecs as ltcodecs
from .exceptions import EncodingFailed


class VariableLenArrayCodec(FieldCodec):
    """
    codec for variable-length array
    """

    def __init__(
        self, element_type: str, max_length: int, element_params=None, **kwargs
    ) -> None:
        self.max_length = max_length
        self.length_codec = VarintCodec(min_value=0, max_value=self.max_length)
        print("element_type", element_type)
        if element_params:
            self.element_field_codec = ltcodecs.field_codec_classes[element_type](
                **element_params
            )
        else:
            self.element_field_codec = ltcodecs.field_codec_classes[element_type]()

    def encode(self, value: list) -> tuple[BitArray, list[Any]]:
        """
        encodes list of elements
        """

        value = value[0 : self.max_length]
        length_bits, _ = self.length_codec.encode(len(value))
        value_bits = BitArray(length_bits)
        encoded_value_list = []
        for element in value:
            (
                element_bits,
                element_value,
            ) = self.element_field_codec.encode(element)

            value_bits.append(element_bits)
            encoded_value_list.append(element_value)
        return value_bits, encoded_value_list

    def decode(self, bits_to_decode: ConstBitStream) -> list:
        """
        decodes list of elements from bits
        """
        num_elements = self.length_codec.decode(bits_to_decode)
        decoded_list = []
        for i in range(num_elements):
            element = self.element_field_codec.decode(bits_to_decode)
            decoded_list.append(element)
        return decoded_list

    @property
    def min_length_bits(self) -> int:
        return self.length_codec.max_length_bits

    @property
    def max_length_bits(self) -> int:
        return self.length_codec.max_length_bits + (
            self.max_length * self.element_field_codec.max_length_bits
        )
