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
from marc_5gempower.agent_func import send_rec
from construct import *

# Encoder for 5G-EmPOWER according to the original protocol

"""
Function that responds to a hello message
Args:
seq: The sequence number of the message
agnt_id: The MAC address of the initiated 5G-EmPOWER agent

Returns:
encoded_msg: The encoded reply
"""


def encode_hello_response(seq, agnt_id):
    # construct the header
    hdr = Container(length=em.HEADER.sizeof())
    hdr.type = em.E_TYPE_SCHED
    hdr.version = em.PT_VERSION
    hdr.enbid = b'\x00\x00' + agnt_id
    hdr.cellid = 0
    hdr.xid = 0
    hdr.flags = Container(dir=0)
    hdr.seq = seq

    # Construct the event
    event = Container(length=em.E_SCHED.sizeof())
    event.action = em.EP_ACT_HELLO
    event.opcode = em.EP_OPERATION_UNSPECIFIED
    event.interval = 2000

    # Construct the data
    data = Container(length=em.HELLO.sizeof(), padding=0)

    # Calculate the size of the header
    hdr.length = em.HEADER.sizeof() + em.E_SCHED.sizeof() + em.HELLO.sizeof()

    # Build the msg
    encoded_msg = em.HEADER.build(hdr) + em.E_SCHED.build(event) + em.HELLO.build(data)
    return encoded_msg


"""
Function that responds to a cell_measurement message
Args:
seq: The sequence number of the message
agnt_id: The MAC address of the initiated 5G-EmPOWER agent

Returns:
encoded_msg: The encoded reply
"""


def encode_cell_measurement_response(seq, agnt_id):
    # Construct the header
    hdr = Container(length=em.HEADER.sizeof())
    hdr.type = em.E_TYPE_SCHED
    hdr.version = em.PT_VERSION
    hdr.enbid = b'\x00\x00' + agnt_id
    hdr.cellid = 0
    hdr.xid = 1
    hdr.flags = Container(dir=0)
    hdr.seq = seq

    # Construct the event
    event = Container(length=em.E_SCHED.sizeof())
    event.action = em.EP_ACT_CELL_MEASURE
    event.opcode = em.EP_OPERATION_SUCCESS
    event.interval = 2000

    Cell_Measurement = Container(length=em.MAC_PRBS_REPORT.sizeof())
    Cell_Measurement.dl_prbs_total = 6
    Cell_Measurement.dl_prbs_used = 2
    Cell_Measurement.ul_prbs_total = 6
    Cell_Measurement.ul_prbs_used = 3

    CelloptionMeasurement = Container()
    CelloptionMeasurement.type = em.EP_MAC_PRBS_REPORT
    CelloptionMeasurement.length = em.MAC_PRBS_REPORT.sizeof()
    CelloptionMeasurement.data = em.MAC_PRBS_REPORT.build(Cell_Measurement)

    # Construct the features of a UE report
    CelldataMeasurenent = Container()
    CelldataMeasurenent.options = [CelloptionMeasurement]

    # Calculate the size of the header
    hdr.length = em.HEADER.sizeof() + em.E_SCHED.sizeof() + len(em.CELL_MEASURE_RESPONSE.build(CelldataMeasurenent))

    # Build the msg
    encoded_msg = em.HEADER.build(hdr) + em.E_SCHED.build(event) + em.CELL_MEASURE_RESPONSE.build(CelldataMeasurenent)
    return encoded_msg


"""
Function that encodes a cell_capabilities message and sends it
Args:
writer: Asyncio TCP connection writer object
id: The header id of the retrieved message
seq: The sequence number of the message
agnt_id: The MAC address of the initiated 5G-EmPOWER agent
"""


async def encode_capabilities_response(writer, id, seq, agnt_id):
    # Construct the header
    hdr = Container(length=em.HEADER.sizeof())
    hdr.type = em.E_TYPE_SINGLE
    hdr.version = em.PT_VERSION
    hdr.enbid = b'\x00\x00' + agnt_id
    hdr.cellid = 0
    hdr.xid = id
    hdr.flags = Container(dir=0)
    hdr.seq = seq

    # Construct the event
    event = Container(length=em.E_SINGLE.sizeof())
    event.action = em.EP_ACT_CAPS
    event.opcode = em.EP_OPERATION_UNSPECIFIED

    dataCELL = Container(length=em.CELL_CAPS.sizeof())

    # Construct the features of a cell
    featuresCELL = {"handover": 0, "cell_measure": 1, "ue_measure": 1, "ue_report": 1}

    dataCELL.pci = 3
    dataCELL.features = featuresCELL
    dataCELL.dl_earfcn = 3500
    dataCELL.dl_bandwidth = 50
    dataCELL.ul_earfcn = 21500
    dataCELL.ul_bandwidth = 50
    dataCELL.max_ues = 2

    # Construction options : 1) is the CELL capabilities, 2) is the RAN capabilities
    optionCELL = Container()
    optionCELL.type = em.EP_CELL_CAPS
    optionCELL.length = em.CELL_CAPS.sizeof()
    optionCELL.data = em.CELL_CAPS.build(dataCELL)

    dataRAN = Container(length=em.RAN_CAPS.sizeof())

    dataRAN.pci = 3
    dataRAN.layer1 = {}
    dataRAN.layer2 = {"rbg_slicing": 1, "prb_slicing": 0}
    dataRAN.layer3 = {}
    dataRAN.mac_sched = 1
    dataRAN.max_slices = 8

    optionRAN = Container()
    optionRAN.type = em.EP_RAN_CAPS
    optionRAN.length = em.RAN_CAPS.sizeof()
    optionRAN.data = em.RAN_CAPS.build(dataRAN)

    # Construct the features of a Capabilities reports
    dataCAPS = Container()
    dataCAPS.options = optionCELL, optionRAN

    # Calculate the size of the header
    hdr.length = em.HEADER.sizeof() + em.E_SINGLE.sizeof() + len(em.ENB_CAPS_RESPONSE.build(dataCAPS))

    # Cuild the msg
    encoded_msg = em.HEADER.build(hdr) + em.E_SINGLE.build(event) + em.ENB_CAPS_RESPONSE.build(dataCAPS)
    await send_rec.send_msg(encoded_msg, writer)


"""
Function that encodes an empty_ue_report message and sends it
Args:
writer: Asyncio TCP connection writer object
id: The header id of the retrieved message
seq: The sequence number of the message
agnt_id: The MAC address of the initiated 5G-EmPOWER agent
"""


async def encode_empty_ue_report_response(writer, id, seq, agnt_id):
    # Construct the header
    hdr = Container(length=em.HEADER.sizeof())
    hdr.type = em.E_TYPE_TRIG
    hdr.version = em.PT_VERSION
    hdr.enbid = b'\x00\x00' + agnt_id
    hdr.cellid = 3
    hdr.xid = id
    hdr.flags = Container(dir=0)
    hdr.seq = seq

    # Construct the event
    event = Container(length=em.E_TRIG.sizeof())
    event.action = em.EP_ACT_UE_REPORT
    event.opcode = em.EP_OPERATION_SUCCESS

    # Construct the features of a UE reports
    dataUE = Container()
    dataUE.options = []

    # Calculate the size of the header
    hdr.length = em.HEADER.sizeof() + em.E_TRIG.sizeof() + len(em.UE_REPORT_RESPONSE.build(dataUE))

    # Cuild the msg
    encoded_msg = em.HEADER.build(hdr) + em.E_TRIG.build(event) + em.UE_REPORT_RESPONSE.build(dataUE)
    await send_rec.send_msg(encoded_msg, writer)

"""
Function that encodes a ue_report message and sends it
Args:
writer: Asyncio TCP connection writer object
rnti: Unique identifier for each user
imsi: International mobile subscriber identity
id: The header id of the retrieved message
seq: The sequence number of the message
agnt_id: The MAC address of the initiated 5G-EmPOWER agent
"""


async def encode_ue_report_response(writer, rnti, imsi, state, id, seq, agnt_id):
    # Construct the header
    hdr = Container(length=em.HEADER.sizeof())
    hdr.type = em.E_TYPE_TRIG
    hdr.version = em.PT_VERSION
    hdr.enbid = b'\x00\x00' + agnt_id
    hdr.cellid = 3
    hdr.xid = id
    hdr.flags = Container(dir=0)
    hdr.seq = seq

    # Construct the event
    event = Container(length=em.E_TRIG.sizeof())
    event.action = em.EP_ACT_UE_REPORT
    event.opcode = em.EP_OPERATION_SUCCESS

    # Co add/remove UEs
    data = Container(length=em.UE_REPORT_IDENTITY.sizeof())
    data.rnti = rnti
    data.plmn_id = b'\x00"/\x93'
    data.imsi = imsi
    data.tmsi = 1
    data.state = state

    # Cptions for UE reports
    optionUE = Container()
    optionUE.type = em.EP_UE_REPORT_IDENTITY
    optionUE.length = em.UE_REPORT_IDENTITY.sizeof()
    optionUE.data = em.UE_REPORT_IDENTITY.build(data)

    # Construct the features of a UE report
    dataUE = Container()
    dataUE.options = [optionUE]

    # Calculate the size of the header
    hdr.length = em.HEADER.sizeof() + em.E_TRIG.sizeof() + len(em.UE_REPORT_RESPONSE.build(dataUE))

    # Cuild the msg
    encoded_msg = em.HEADER.build(hdr) + em.E_TRIG.build(event) + em.UE_REPORT_RESPONSE.build(dataUE)
    await send_rec.send_msg(encoded_msg, writer)

"""
Function that encodes a ran_mac_slice_response message and sends it
Args:
writer: Asyncio TCP connection writer object
id: The header id of the retrieved message
seq: The sequence number of the message
agnt_id: The MAC address of the 5G-EmPOWER agent
"""


async def encode_ran_mac_slice_response(writer, id, seq, agnt_id):
    # Construct the header
    hdr = Container(length=em.HEADER.sizeof())
    hdr.type = em.E_TYPE_SINGLE
    hdr.version = em.PT_VERSION
    hdr.enbid = b'\x00\x00' + agnt_id
    hdr.cellid = 3
    hdr.xid = id
    hdr.flags = Container(dir=0)
    hdr.seq = seq

    # Construct the event
    event = Container(length=em.E_SINGLE.sizeof())
    event.action = em.EP_ACT_RAN_MAC_SLICE
    event.opcode = em.EP_OPERATION_UNSPECIFIED

    sched_id_data = Container(length=em.RAN_MAC_SLICE_SCHED_ID.sizeof())
    sched_id_data.sched_id = 2147483649

    # Options for RAN_MAC_Slice_Sched
    optionRAN_MAC_Slice_Sched = Container()
    optionRAN_MAC_Slice_Sched.type = em.EP_RAN_MAC_SLICE_SCHED_ID
    optionRAN_MAC_Slice_Sched.length = 0x4
    optionRAN_MAC_Slice_Sched.data = em.RAN_MAC_SLICE_SCHED_ID.build(sched_id_data)

    rbgs_data = Container(length=em.RAN_MAC_SLICE_RBGS.sizeof())
    rbgs_data.rbgs = 6

    # Options for RAN_MAC_Slice_RGBs (Resource Block Groups)
    optionRAN_MAC_Slice_Rbgs = Container()
    optionRAN_MAC_Slice_Rbgs.type = em.EP_RAN_MAC_SLICE_RBGS
    optionRAN_MAC_Slice_Rbgs.length = 0x2
    optionRAN_MAC_Slice_Rbgs.data = em.RAN_MAC_SLICE_RBGS.build(rbgs_data)

    # Construct the features of a RAN_MAC_Slice
    data_RAN_MAC_Slice = Container()

    data_RAN_MAC_Slice.plmn_id = b'\x00"/\x93'
    data_RAN_MAC_Slice.dscp = 0
    data_RAN_MAC_Slice.padding = b'\x00\x00\x00'
    data_RAN_MAC_Slice.options = [optionRAN_MAC_Slice_Rbgs, optionRAN_MAC_Slice_Sched]

    # Calculate the size of the header
    hdr.length = em.HEADER.sizeof() + em.E_SINGLE.sizeof() + len(em.RAN_MAC_SLICE_RESPONSE.build(data_RAN_MAC_Slice))

    # Build the msg
    encoded_msg = em.HEADER.build(hdr) + em.E_SINGLE.build(event) + em.RAN_MAC_SLICE_RESPONSE.build(data_RAN_MAC_Slice)
    await send_rec.send_msg(encoded_msg, writer)

"""
Function that encodes a ue_measurements_response message and sends it
Args:
writer: Asyncio TCP connection writer object
id: The header id of the retrieved message
seq: The sequence number of the message
agnt_id: The MAC address of the 5G-EmPOWER agent
"""


async def encode_ue_measurements_response(writer, id, seq, agnt_id):
    # Construct the header
    hdr = Container(length=em.HEADER.sizeof())
    hdr.type = em.E_TYPE_TRIG
    hdr.version = em.PT_VERSION
    hdr.enbid = b'\x00\x00' + agnt_id
    hdr.cellid = 0
    hdr.xid = id
    hdr.flags = Container(dir=0)
    hdr.seq = seq

    # Construct the event
    event = Container(length=em.E_TRIG.sizeof())
    event.action = em.EP_ACT_UE_MEASURE
    event.opcode = em.EP_OPERATION_SUCCESS

    UE_Measurement = Container(length=em.RRC_MEASURE_REPORT.sizeof())
    UE_Measurement.measure_id = 0
    UE_Measurement.pci = 3
    UE_Measurement.rsrp = 60
    UE_Measurement.rsrq = 3

    UEoptionMeasurement = Container()
    UEoptionMeasurement.type = em.EP_RRC_MEASURE_REPORT
    UEoptionMeasurement.length = em.RRC_MEASURE_REPORT.sizeof()
    UEoptionMeasurement.data = em.RRC_MEASURE_REPORT.build(UE_Measurement)

    # Construct the features of a UE reports
    UEdataMeasurenent = Container()
    UEdataMeasurenent.options = [UEoptionMeasurement]

    # Calculate the size of the header
    hdr.length = em.HEADER.sizeof() + em.E_TRIG.sizeof() + len(em.UE_MEASURE_RESPONSE.build(UEdataMeasurenent))
    encoded_msg = em.HEADER.build(hdr) + em.E_TRIG.build(event) + em.UE_MEASURE_RESPONSE.build(UEdataMeasurenent)
    await send_rec.send_msg(encoded_msg, writer)
