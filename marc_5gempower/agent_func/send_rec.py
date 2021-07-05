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

from marc_5gempower.agent_func import encode
from marc_5gempower.agent_func import decode
import marc_5gempower.empower_msg.empower_messages as em

import asyncio
import random

active_rntis = []

seq = 5
ue_meas_start = 0
ue_meas_rnti = 0
ue_meas = 0

"""
Function that sends a keep alive hello message to the controller every 2 seconds

Args:
writer: Asyncio TCP connection writer object
agnt_id: The MAC address of the 5G-EmPOWER agent
"""


async def hb_hello(writer, agnt_id):
    global seq
    while True:
        seq = seq + 1
        msg = encode.encode_hello_response(seq, agnt_id)
        # print("Sending keep alive msg")
        writer.write(msg)
        await asyncio.sleep(2)

"""
Function that sends cell_measurement messages to the controller every 0.5 seconds

Args:
writer: Asyncio TCP connection writer object
agnt_id: The MAC address of the 5G-EmPOWER agent
"""


async def cell_measurement(writer, agnt_id):
    global seq

    while True:
        seq = seq + 1
        msg = encode.encode_cell_measurement_response(seq, agnt_id)
        # print("Sending cell_measurements")
        writer.write(msg)
        await asyncio.sleep(0.5)

"""
Function that sends ue periodic messages to the controller every 0.5 seconds

Args:
writer: Asyncio TCP connection writer object
x_id: The header id of the previously received message
agnt_id: The MAC address of the 5G-EmPOWER agent
"""


async def ue_periodic_measurement(writer, x_id, agnt_id):
    global seq
    while True:
        if len(active_rntis) != 0:
            for ue in range(len(active_rntis)):
                seq = seq + 1
                await encode.encode_ue_measurements_response(writer, x_id, seq, agnt_id)
            # print("Sending ue_per_measuements", len(active_rntis))
            await asyncio.sleep(0.5)
        else:
            await asyncio.sleep(0.5)

"""
Function that sends a message

Args:
msg: The message type
writer: Asyncio TCP connection writer object
"""


async def send_msg(msg, writer):
    writer.write(msg)

"""
Function that receives a message

Args:
reader: Asyncio TCP connection reader object
writer: Asyncio TCP connection writer object
agnt_id: The MAC address of the 5G-EmPOWER agent
"""


async def receive_msg(reader, writer, agnt_id):
    global active_rntis
    global ue_meas_start
    global ue_meas_rnti
    global ue_meas

    while True:
        data = await reader.read(1024)
        msgType, hdr = decode.decode_header(data)
        receivedMsg, offset, event, operation = decode.decode_msg(data, msgType)

        if receivedMsg == em.EP_ACT_CAPS:
            # print("%%% The received msg is a capability request %%%")
            await encode.encode_capabilities_response(writer, hdr.xid, seq, agnt_id)

        if receivedMsg == em.EP_ACT_UE_REPORT:
            # print("%%% The received msg is a ue report request %%%")
            await encode.encode_empty_ue_report_response(writer, hdr.xid, seq, agnt_id)

        if receivedMsg == em.EP_ACT_UE_MEASURE:
            # print("%%% The received msg is a ue measurement request %%%")
            msg = em.PT_TYPES[receivedMsg].parse(data[offset:])
            msgOptions = msg.options

            for options in msgOptions:
                option = em.RRC_MEASURE_REQUEST.parse(options.data)
                await encode.encode_ue_measurements_response(writer, hdr.xid, seq, agnt_id)

        if receivedMsg == em.EP_ACT_RAN_MAC_SLICE:
            if operation == 4:
                continue
                # print("%%% Set a ran policy %%%")

            else:
                # print("%%% The received msg is a ran mac slice request %%%")
                await encode.encode_ran_mac_slice_response(writer, hdr.xid, seq, agnt_id)


"""
Function that handles the ue events for each 5G-EmPOWER agents and send messages to the controller accordingly

Args:
writer: Asyncio TCP connection writer object
event_list: The generated list of ue activations and de-activations
rnti_list: The list of all user identifiers
imsi_list: The list with all the international mobile subscriber identities
xid: The id of the received message header
agnt_id: The MAC address of the 5G-EmPOWER agent
"""


async def events(writer, event_list, rnti_list, imsi_list, xid, agnt_id):
    global seq
    global ue_meas_start
    global ue_meas_rnti
    global ue_meas
    cnt = 0

    compare_time = event_list[0]['time']
    for ev in event_list:
        cnt = cnt + 1
        seq = seq + 1
        await asyncio.sleep(abs(compare_time - ev['time']))
        if ev['eventType'] == 'activated':
            rnti = random.randint(1, 100)
            # Generate random imsi identifier for every created UE
            imsi = random.randint(222930000000100, 222930000000200)
            rnti_list.append(rnti)
            imsi_list.append(imsi)
            state = 0
            active_rntis.append(rnti)
            await encode.encode_ue_report_response(writer, rnti, imsi, state, xid, seq, agnt_id)


        elif ev['eventType'] == 'deactivated':
            rnti = rnti_list.pop(0)
            imsi = imsi_list.pop(0)
            active_rntis.pop(0)
            state = 1
            await encode.encode_ue_report_response(writer, rnti, imsi, state, xid, seq, agnt_id)

        compare_time = ev['time']
