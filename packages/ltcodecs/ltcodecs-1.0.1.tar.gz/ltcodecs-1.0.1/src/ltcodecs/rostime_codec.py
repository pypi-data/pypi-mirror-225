"""
ltcodecs.ros_time_codec
-----------------------

This module contains the RosTimeCodec class, which is used to encode and decode ROS times.
"""

from __future__ import annotations

from math import ceil, log2
from bitstring import ConstBitStream, Bits
from rospy import Time

from .field_codec import FieldCodec


class RosTimeCodec(FieldCodec):
    """
    codec for encoding and decoding ROS times
    """

    def __init__(
        self,
        precision: int = 0,
        epoch_start=1622520000,
        epoch_end=(2**31 - 1),
        **kwargs,
    ) -> None:
        self.max_value = epoch_end
        self.min_value = epoch_start
        self.precision = int(precision)

        self.value_range = int(
            round(self.max_value - self.min_value, precision) * 10**precision
        )
        self.num_bits = ceil(log2(self.value_range))

    def encode(self, value: Time) -> tuple[Bits, Time]:
        """
        encode rostime

        :param value: rostime to encode
        """

        value = value.to_sec()
        if value < self.min_value:
            value = self.min_value
        elif value > self.max_value:
            value = self.max_value

        encoded_value = int(
            round(value - self.min_value, self.precision) * 10**self.precision
        )
        # print(value, self.min_value, self.precision)
        rounded_value = (
            round(value - self.min_value, self.precision) + self.min_value
        )  # Used only for validation
        rounded_value = Time.from_sec(rounded_value)
        encoded_bits = Bits(uint=encoded_value, length=self.num_bits)

        return encoded_bits, rounded_value

    def decode(self, bits_to_decode: ConstBitStream) -> Time:
        """
        decode rostime

        :param bits_to_decode: the bitstream to decode
        """

        float_offset = (
            bits_to_decode.read(f"uint:{self.num_bits}") / 10**self.precision
        )
        value = Time.from_sec(self.min_value + float_offset)
        return value

    @property
    def max_length_bits(self) -> int:
        return self.num_bits

    @property
    def min_length_bits(self) -> int:
        return self.num_bits
