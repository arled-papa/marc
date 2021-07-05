#!/usr/bin/env python3
#
# Copyright (c) 2021 Arled Papa
# Author: Arled Papa <arled.papa@tum.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import struct


# socket sending function for the encoded message
async def sock_send(encoded_msg, writer):
    packed_len = struct.pack('>L', len(encoded_msg))
    writer.write(packed_len)
    writer.write(encoded_msg)


# encoder function for FlexRAN
async def encode_msg(flex_msg, writer):
    encoded_msg = flex_msg.SerializeToString()
    await sock_send(encoded_msg, writer)


# decoder function for FlexRAN
async def decode_msg(msg, reader):
    """ Read a message from a socket. msgtype is a subclass of
        of protobuf Message.
    """
    len_buf = await reader.read(4)

    """Converts sequence of bytes into integer value (length of the message)"""
    msg_len = struct.unpack('>L', len_buf)[0]

    message = await reader.read(msg_len)
    if len(message) > 0:
        msg.ParseFromString(message)
        return msg
    else:
        return None
