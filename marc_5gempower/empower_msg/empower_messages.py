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

from construct import *

# Structure of all messages for 5G-EmPOWER according to the original protocol

PT_BYE = "bye"
PT_REGISTER = "register"
PT_UE_JOIN = "ue_join"
PT_UE_LEAVE = "ue_leave"

# 5G-EmPower version
PT_VERSION = 0x01

# 5G-EmPower actions
EP_ACT_INVALID = 0
EP_ACT_HELLO = 1
EP_ACT_CAPS = 2
EP_ACT_UE_REPORT = 4
EP_ACT_UE_MEASURE = 5
EP_ACT_CELL_MEASURE = 6
EP_ACT_HANDOVER = 7
EP_ACT_RAN_SETUP = 9
EP_ACT_RAN_MAC_SLICE = 10

# 5G-EmPower type
E_TYPE_SINGLE = 0x01
E_TYPE_SCHED = 0x02
E_TYPE_TRIG = 0x03

# 5G-EmPower operation codes

EP_OPERATION_UNSPECIFIED = 0
EP_OPERATION_SUCCESS = 1
EP_OPERATION_FAIL = 2
EP_OPERATION_NOT_SUPPORTED = 3
EP_OPERATION_ADD = 4
EP_OPERATION_REM = 5
EP_OPERATION_SET = 6

E_SCHED = Struct("e_sched",
                 UBInt16("action"),
                 UBInt8("opcode"),
                 UBInt32("interval"))

E_SINGLE = Struct("e_single",
                  UBInt16("action"),
                  UBInt8("opcode"))

E_TRIG = Struct("e_trig",
                UBInt16("action"),
                UBInt8("opcode"))

OPTIONS = Struct("options",
                 UBInt16("type"),
                 UBInt16("length"),
                 Field("data", lambda ctx: ctx.length))

HEADER = Struct("header",
                UBInt8("type"),
                UBInt8("version"),
                Bytes("enbid", 8),
                UBInt16("cellid"),
                UBInt32("xid"),
                BitStruct("flags", Padding(15), Bit("dir")),
                UBInt32("seq"),
                UBInt16("length"))

HELLO = Struct("hello",
               UBInt32("padding"))

ENB_CAPS_REQUEST = Struct("caps_request",
                          UBInt8("type"),
                          UBInt8("version"),
                          Bytes("enbid", 8),
                          UBInt16("cellid"),
                          UBInt32("xid"),
                          BitStruct("flags", Padding(15), Bit("dir")),
                          UBInt32("seq"),
                          UBInt16("length"),
                          UBInt16("action"),
                          UBInt8("opcode"),
                          UBInt32("dummy"))

ENB_CAPS_RESPONSE = Struct("caps_response",
                           Rename("options",
                                  OptionalGreedyRange(OPTIONS)))

RAN_MAC_SLICE_REQUEST = Struct("ran_mac_slice_request",
                               UBInt8("type"),
                               UBInt8("version"),
                               Bytes("enbid", 8),
                               UBInt16("cellid"),
                               UBInt32("xid"),
                               BitStruct("flags", Padding(15), Bit("dir")),
                               UBInt32("seq"),
                               UBInt16("length"),
                               UBInt16("action"),
                               UBInt8("opcode"),
                               Bytes("plmn_id", 4),
                               UBInt8("dscp"),
                               Bytes("padding", 3))

RAN_MAC_SLICE_RESPONSE = Struct("ran_mac_slice_response",
                                Bytes("plmn_id", 4),
                                UBInt8("dscp"),
                                Bytes("padding", 3),
                                Rename("options",
                                       OptionalGreedyRange(OPTIONS)))

UE_REPORT_REQUEST = Struct("ue_report_request",
                           UBInt8("type"),
                           UBInt8("version"),
                           Bytes("enbid", 8),
                           UBInt16("cellid"),
                           UBInt32("xid"),
                           BitStruct("flags", Padding(15), Bit("dir")),
                           UBInt32("seq"),
                           UBInt16("length"),
                           UBInt16("action"),
                           UBInt8("opcode"),
                           UBInt32("dummy"))

UE_REPORT_RESPONSE = Struct("ue_report_response",
                            Rename("options",
                                   OptionalGreedyRange(OPTIONS)))

SET_RAN_MAC_SLICE_REQUEST = Struct("set_ran_mac_slice_request",
                                   UBInt8("type"),
                                   UBInt8("version"),
                                   Bytes("enbid", 8),
                                   UBInt16("cellid"),
                                   UBInt32("xid"),
                                   BitStruct("flags", Padding(15), Bit("dir")),
                                   UBInt32("seq"),
                                   UBInt16("length"),
                                   UBInt16("action"),
                                   UBInt8("opcode"),
                                   Bytes("plmn_id", 4),
                                   UBInt8("dscp"),
                                   Bytes("padding", 3),
                                   Rename("options",
                                          OptionalGreedyRange(OPTIONS)))

# Cell capabilities struct
CELL_CAPS = Struct("cell_caps",
                   UBInt16("pci"),
                   BitStruct("features", Padding(28),
                             Bit("handover"),
                             Bit("cell_measure"),
                             Bit("ue_measure"),
                             Bit("ue_report")),
                   UBInt16("dl_earfcn"),
                   UBInt8("dl_bandwidth"),
                   UBInt16("ul_earfcn"),
                   UBInt8("ul_bandwidth"),
                   UBInt16("max_ues"))

# Measurement struct
CELL_MEASURE_RESPONSE = Struct("cell_measure_response",
                               Rename("options",
                                      OptionalGreedyRange(OPTIONS)))


MAC_PRBS_REPORT = Struct("mac_prbs_report",
                         UBInt8("dl_prbs_total"),
                         UBInt32("dl_prbs_used"),
                         UBInt8("ul_prbs_total"),
                         UBInt32("ul_prbs_used"))

EP_MAC_PRBS_REQUEST = 0x0101
EP_MAC_PRBS_REPORT = 0x0102

CELL_MEASURE_TYPES = {
    EP_MAC_PRBS_REPORT: MAC_PRBS_REPORT
}


# UE report identity struct
UE_REPORT_IDENTITY = Struct("ue_report_identity",
                            UBInt16("rnti"),
                            Bytes("plmn_id", 4),
                            UBInt64("imsi"),
                            UBInt32("tmsi"),
                            UBInt8("state"))

# RAN capabilities. This is a valid TLV for the ENB_CAPS_RESPONSE message.
RAN_CAPS = Struct("ran_caps",
                  UBInt16("pci"),
                  BitStruct("layer1", Padding(32)),
                  BitStruct("layer2", Padding(30),
                            Bit("prb_slicing"),
                            Bit("rbg_slicing")),
                  BitStruct("layer3", Padding(32)),
                  UBInt32("mac_sched"),
                  UBInt16("max_slices"))

RAN_MAC_SLICE_RBGS = Struct("ran_mac_slice_rbgs", UBInt16("rbgs"))
RAN_MAC_SLICE_SCHED_ID = Struct("ran_mac_slice_sched_id", UBInt32("sched_id"))
RAN_MAC_SLICE_RNTI_LIST = Struct("ran_mac_slice_rntis",
                                 OptionalGreedyRange(UBInt16("rntis")))

EP_CELL_CAPS = 0x0100
EP_RAN_CAPS = 0x0503

# RAN capability types
# Scheduler id
EP_RAN_MAC_SLICE_SCHED_ID = 0x0502
# Number of resources
EP_RAN_MAC_SLICE_RBGS = 0x0501
# The list of rntis
EP_RAN_MAC_SLICE_RNTI_LIST = 0x0001

RAN_MAC_SLICE_TYPES = {
    EP_RAN_MAC_SLICE_RBGS: RAN_MAC_SLICE_RBGS,
    EP_RAN_MAC_SLICE_SCHED_ID: RAN_MAC_SLICE_SCHED_ID,
    EP_RAN_MAC_SLICE_RNTI_LIST: RAN_MAC_SLICE_RNTI_LIST
}

# eNB capability types
ENB_CAPS_TYPES = {
    EP_CELL_CAPS: CELL_CAPS,
    EP_RAN_CAPS: RAN_CAPS
}

EP_UE_REPORT_IDENTITY = 0x0700
# UE report types

EP_ACT_UE_MEASURE = 0x05

# message structure for UE measurements report
UE_MEASUREMENT_REPORT = Struct("ue_measure_report",
                               UBInt8("type"),
                               UBInt8("version"),
                               Bytes("enbid", 8),
                               UBInt16("cellid"),
                               UBInt32("xid"),
                               BitStruct("flags", Padding(15), Bit("dir")),
                               UBInt32("seq"),
                               UBInt16("length"),
                               UBInt16("action"),
                               UBInt8("opcode"))

# Message structure for UE measurements request
UE_MEASURE_REQUEST = Struct("ue_measure_request",
                            UBInt8("type"),
                            UBInt8("version"),
                            Bytes("enbid", 8),
                            UBInt16("cellid"),
                            UBInt32("xid"),
                            BitStruct("flags", Padding(15), Bit("dir")),
                            UBInt32("seq"),
                            UBInt16("length"),
                            UBInt16("action"),
                            UBInt8("opcode"),
                            Rename("options",
                                   OptionalGreedyRange(OPTIONS)))

UE_MEASURE_RESPONSE = Struct("ue_measure_response",
                             Rename("options",
                                    OptionalGreedyRange(OPTIONS)))

RRC_MEASURE_REQUEST = Struct("rrc_measure_request",
                             UBInt16("measure_id"),
                             UBInt16("rnti"),
                             UBInt16("earfcn"),
                             UBInt16("interval"),
                             UBInt16("max_cells"),
                             UBInt16("max_measure"))

RRC_MEASURE_REPORT = Struct("rrc_measure_report",
                            UBInt16("measure_id"),
                            UBInt16("pci"),
                            SBInt16("rsrp"),
                            SBInt16("rsrq"))

EP_RRC_MEASURE_REQUEST = 0x0600
EP_RRC_MEASURE_REPORT = 0x0601

UE_MEASURE_TYPES = {
    EP_RRC_MEASURE_REPORT: RRC_MEASURE_REPORT,
}

UE_REPORT_TYPES = {
    EP_UE_REPORT_IDENTITY: UE_REPORT_IDENTITY
}

PT_TYPES = {PT_BYE: None,
            PT_REGISTER: None,
            PT_UE_JOIN: None,
            PT_UE_LEAVE: None,
            EP_ACT_HELLO: HELLO,
            EP_ACT_CAPS: ENB_CAPS_RESPONSE,
            EP_ACT_RAN_MAC_SLICE: RAN_MAC_SLICE_RESPONSE,
            EP_ACT_UE_REPORT: UE_REPORT_RESPONSE,
            EP_ACT_UE_MEASURE: UE_MEASURE_RESPONSE,
            EP_ACT_CELL_MEASURE: CELL_MEASURE_RESPONSE
            }