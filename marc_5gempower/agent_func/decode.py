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

import marc_5gempower.empower_msg.empower_messages as em


# Header decoder for 5G-EmPOWER according to the original protocol, where input is the received message
def decode_header(msg):
    hdr = em.HEADER.parse(msg)
    msgType = hdr.type
    return msgType, hdr


# Message decoder for 5G-EmPOWER according to the original protocol, where input is the received message
def decode_msg(dataStream, type):
    if type == 1:
        event = em.E_SINGLE.parse(dataStream[em.HEADER.sizeof():])
        offset = em.HEADER.sizeof() + em.E_SINGLE.sizeof()
        receivedMsg = event.action
        operationMsg = event.opcode
    elif type == 2:
        event = em.E_SCHED.parse(dataStream[em.HEADER.sizeof():])
        offset = em.HEADER.sizeof() + em.E_SCHED.sizeof()
        receivedMsg = event.action
        operationMsg = event.opcode
    else:
        event = em.E_TRIG.parse(dataStream[em.HEADER.sizeof():])
        offset = em.HEADER.sizeof() + em.E_TRIG.sizeof()
        receivedMsg = event.action
        operationMsg = event.opcode

    return receivedMsg, offset, event, operationMsg
