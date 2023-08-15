# MIT License
#
# Copyright (c) 2023 MatrixEditor
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

__doc__ = """CAF Object Model"""
__all__ = [
    "caf__header_t",
    "caf__chunk_header_t",
    "caf__audio_format_flags",
    "caf__audio_format_t",
    "caf__data_t",
    "caf__strings_chunk_t",
    "caf__packet_table_t",
    "caf__chunk_t",
    "caf__header",
    "caf__chunk_header",
    "caf__audio_format",
    "caf__data",
    "caf__strings_chunk",
    "caf__packet_table",
    "caf__chunk",
    "caf_t",
    "caf",
]

import dataclasses as dc
import enum
import typing as t
import construct as cs

from construct_dataclasses import *


@dc.dataclass
class caf__header_t:
    """A CAF file begins with a simple header."""

    m_file_type: bytes = csfield(cs.Const(b"caff"))  # Core Audio File Format
    """The file type. This value must be set to 'caff'"""

    m_file_version: int = csfield(cs.Int16ub)
    """
    The file version. For CAF files conforming to this specification, the
    version must be set to 1.
    """

    m_file_flags: int = csfield(cs.Int16ub)
    """Flags reserved by Apple for future use. For CAF v1 files, must be set to 0."""


caf__header = DataclassStruct(caf__header_t)


@container
@dc.dataclass
class caf__chunk_header_t:
    """
    Every chunk in a CAF file has a header, and each such header contains
    two required fields.
    """

    m_chunk_type: bytes = csfield(cs.Bytes(4))
    """The chunk type, described as a four-character code."""

    m_chunk_size: int = csfield(cs.Int64ub)
    """
    The size, in bytes, of the data section for the chunk. This is the size
    of the chunk not including the header.
    """


caf__chunk_header = DataclassStruct(caf__chunk_header_t)


class caf__audio_format_flags(enum.IntEnum):
    kCAFLinearPCMFormatFlagIsFloat = 1
    kCAFLinearPCMFormatFlagIsLittleEndian = 0


@container
@dc.dataclass
class caf__audio_format_t:
    m_sample_rate: float = csfield(cs.Float64b)
    m_format_id: str = csfield(cs.StringEncoded(cs.Bytes(4), "utf-8"))
    m_format_flags: caf__audio_format_flags = tfield(
        caf__audio_format_flags, cs.Enum(cs.Int32ub, caf__audio_format_flags)
    )
    m_bytes_per_packet: int = csfield(cs.Int32ub)
    m_frames_per_packet: int = csfield(cs.Int32ub)
    m_channels_per_frame: int = csfield(cs.Int32ub)
    m_bits_per_channel: int = csfield(cs.Int32ub)


caf__audio_format = DataclassStruct(caf__audio_format_t)


@dc.dataclass
class caf__data_t:
    m_edit_count: int = csfield(cs.Int32ub)  # initially set to 0
    m_data: bytes = csfield(cs.Bytes(cs.this._.m_chunk_header.m_chunk_size - 4))


caf__data = DataclassStruct(caf__data_t)


@cs.singleton
class GreedyTerminatedString(cs.Adapter):
    def __init__(self):
        super().__init__(cs.RepeatUntil(lambda idx, lst, ctx: idx == 0, cs.Byte))

    def _decode(self, obj: list[int], context, path):
        return bytes(obj).decode().rstrip("\x00")

    def _encode(self, obj: str, context, path):
        return obj.encode() + b"\x00"


@dc.dataclass
class caf__information_t:
    m_key: str = csfield(GreedyTerminatedString)
    m_value: str = csfield(GreedyTerminatedString)


caf__information = DataclassStruct(caf__information_t)


@dc.dataclass
class caf__strings_chunk_t:
    m_num_entries: int = csfield(cs.Int32ub)
    m_strings: list[str] = csfield(cs.Array(cs.this.m_num_entries, caf__information))


caf__strings_chunk = DataclassStruct(caf__strings_chunk_t)


@dc.dataclass
class caf__packet_table_t:
    m_num_packets: int = csfield(cs.Int64sb)
    m_num_valid_frames: int = csfield(cs.Int64sb)
    m_priming_frames: int = csfield(cs.Int32sb)
    m_remainder_frames: int = csfield(cs.Int32sb)
    m_table_data: list[int] = csfield(cs.Array(cs.this.m_num_packets, cs.VarInt))


caf__packet_table = DataclassStruct(caf__packet_table_t)


@dc.dataclass
class caf__channel_desc_t:
    m_channel_label: int = csfield(cs.Int32ub)
    m_channel_flags: int = csfield(cs.Int32ub)
    m_coordinates: list[float] = csfield(cs.Array(3, cs.Float32b))


caf__channel_desc = DataclassStruct(caf__channel_desc_t)


@dc.dataclass
class caf__channel_layout_t:
    m_channel_layout_tag: int = csfield(cs.Int32ub)
    m_channel_bitmap: int = csfield(cs.Int32ub)
    m_num_descriptions: int = csfield(cs.Int32ub)
    m_descriptions: int = csfield(
        cs.Array(cs.this.m_num_descriptions, caf__channel_desc)
    )


@dc.dataclass
class caf__chunk_t:
    m_chunk_header: caf__chunk_header_t = csfield(caf__chunk_header)
    m_data: t.Union[t.Any, bytes] = csfield(
        cs.Switch(
            cs.this.m_chunk_header.m_chunk_type,
            cases={
                b"desc": caf__audio_format,
                b"info": caf__strings_chunk,
                b"pakt": caf__packet_table,
                b"data": caf__data,
            },
            default=cs.Bytes(cs.this.m_chunk_header.m_chunk_size),
        )
    )


caf__chunk = DataclassStruct(caf__chunk_t)


@dc.dataclass
class caf_t:
    m_header: caf__header_t = csfield(caf__header)
    """header of this CAF file"""
    m_chunks: list[caf__chunk_t] = csfield(cs.GreedyRange(caf__chunk))


caf = DataclassStruct(caf_t)
_schema = caf
