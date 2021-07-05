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

import marc_flexran.agent_func.send_rec as send_rec
import marc_flexran.flexran_msg.flexran_pb2 as flexran_pb2
import marc_flexran.flexran_msg.header_pb2 as header_pb2
import marc_flexran.flexran_msg.config_common_pb2 as config_common_pb2
import marc_flexran.flexran_msg.stats_common_pb2 as stats_common_pb2
import asyncio
import random

"""
FlexRAN messages generated according to the FlexRAN protocol
1) Hello message
2) Base Station configuration (referred to as enb)
3) UE configuration
4) Logical Channel (LC) configuration (initial + logical channel in case of activation and deactivation of users)
5) Periodic statistics reply
6) UE state change (activation)
7) UE state change (deactivation)

"""

list_of_ue = []  # list that retains the users in the system
frame_id = 4000  # the id of the lte frame
local = []

""" hello message """


async def hello_msg(msg, writer):
    header = msg.hello_msg.header
    header.type = header_pb2.FLPT_HELLO
    header.xid = 1
    header.version = 0
    msg.msg_dir = flexran_pb2.SUCCESSFUL_OUTCOME
    await send_rec.encode_msg(msg, writer)


"""enodeB config message """


async def enb_config(msg, enb_lst, writer):
    header = msg.enb_config_reply_msg.header
    header.type = header_pb2.FLPT_GET_ENB_CONFIG_REPLY
    header.xid = 0
    header.version = 0

    payload = msg.enb_config_reply_msg.cell_config.add()
    payload.cell_id = enb_lst.cell_id
    payload.pusch_hopping_offset = enb_lst.pusch_hopping_offset
    payload.hopping_mode = enb_lst.hopping_mode
    payload.n_sb = enb_lst.n_sb
    payload.phich_resource = enb_lst.phich_resource
    payload.phich_duration = enb_lst.phich_duration
    payload.dl_bandwidth = enb_lst.dl_bandwidth
    payload.ul_bandwidth = enb_lst.dl_bandwidth
    payload.ul_cyclic_prefix_length = enb_lst.ul_cyclic_prefix_length
    payload.dl_cyclic_prefix_length = enb_lst.dl_cyclic_prefix_length
    payload.antenna_ports_count = enb_lst.antenna_ports_count
    payload.duplex_mode = enb_lst.duplex_mode

    payload.prach_config_index = enb_lst.prach_config_index
    payload.prach_freq_offset = enb_lst.prach_freq_offset
    payload.ra_response_window_size = enb_lst.ra_response_window_size
    payload.mac_contention_resolution_timer = enb_lst.mac_contention_resolution_timer
    payload.max_HARQ_Msg3Tx = enb_lst.max_HARQ_Msg3Tx
    payload.n1PUCCH_AN = enb_lst.n1PUCCH_AN
    payload.deltaPUCCH_shift = enb_lst.deltaPUCCH_shift
    payload.nRB_cqi = enb_lst.nRB_cqi

    payload.srs_subframe_config = enb_lst.srs_subframe_config
    payload.srs_bw_config = enb_lst.srs_bw_config
    payload.srs_mac_up_pts = enb_lst.srs_mac_up_pts
    payload.enable_64QAM = enb_lst.enable_64QAM
    payload.carrier_index = enb_lst.carrier_index
    payload.dl_freq = enb_lst.dl_freq
    payload.ul_freq = enb_lst.ul_freq
    payload.eutra_band = enb_lst.eutra_band
    payload.dl_pdsch_power = enb_lst.dl_pdsch_power
    payload.ul_pusch_power = enb_lst.ul_pusch_power
    await send_rec.encode_msg(msg, writer)


""" ue config message """


async def ue_config(msg, writer):
    header = msg.ue_config_reply_msg.header
    header.type = header_pb2.FLPT_GET_UE_CONFIG_REPLY
    header.xid = 1
    header.version = 0
    await send_rec.encode_msg(msg, writer)


""" initial logical control config message as part of synchronous messages """


async def init_lc_config(msg, writer):
    header = msg.lc_config_reply_msg.header
    header.type = header_pb2.FLPT_GET_LC_CONFIG_REPLY
    header.xid = 2
    header.version = 0

    await send_rec.encode_msg(msg, writer)


""" logical control message in case of an activated or deactivated user in the system """


async def lc_config(msg, writer, lc, rnti):
    header = msg.lc_config_reply_msg.header
    header.type = header_pb2.FLPT_GET_LC_CONFIG_REPLY
    header.xid = 2
    header.version = 0
    config = msg.lc_config_reply_msg.lc_ue_config.add()
    config.rnti = rnti
    lc_config = config.lc_config.add()

    for logical_channel in range(1, 4):
        lc_config.lcid = logical_channel
        lc_config.direction = lc.direction
        lc_config.qos_bearer_type = lc.qos_bearer_type
        lc_config.qci = lc.qci

    await send_rec.encode_msg(msg, writer)


"""user stat report incuding the rnti (radio network identifier) that is send to the controller as synchronous 
message """


async def periodic_stats_reply(msg, writer, stats, frame_id, list_of_ue, ue_report={}):
    header = msg.stats_reply_msg.header
    header.type = header_pb2.FLPT_STATS_REPLY
    header.version = 0
    header.xid = 0

    if len(list_of_ue) != 0:
        for ue in range(len(list_of_ue)):
            report = msg.stats_reply_msg.ue_report.add()
            report.rnti = list_of_ue[ue]

            report.flags = ue_report.flags
            report.bsr.append(ue_report.bsr)
            report.phr = ue_report.phr
            report.pending_mac_ces = ue_report.pending_mac_ces

            for logical_channel in range(1, 4):
                rlc_rep1 = report.rlc_report.add()
                rlc_rep1.lc_id = logical_channel
                rlc_rep1.tx_queue_size = ue_report.queue_size
                rlc_rep1.tx_queue_hol_delay = ue_report.queue_delay
                rlc_rep1.status_pdu_size = ue_report.pdu_size

            dl_cqi_rep = report.dl_cqi_report
            dl_cqi_rep.sfn_sn = frame_id

            csi_rep = dl_cqi_rep.csi_report.add()
            csi_rep.serv_cell_index = ue_report.dl_serv_cell_index
            csi_rep.ri = ue_report.ri
            csi_rep.type = ue_report.type
            csi_rep.p10csi.wb_cqi = ue_report.wb_cqi

            ul_cqi_rep = report.ul_cqi_report
            ul_cqi_rep.sfn_sn = frame_id

            cqi_meas = ul_cqi_rep.cqi_meas.add()
            cqi_meas.type = stats_common_pb2.FLUCT_SRS
            cqi_meas.sinr.append(ue_report.sinr)
            cqi_meas.serv_cell_index = ue_report.ul_serv_cell_index
            pucch_dbm = ul_cqi_rep.pucch_dbm.add()

            pucch_dbm.p0_pucch_dbm = ue_report.pucch_dbm
            pucch_dbm.serv_cell_index = ue_report.pucch_serv_cell_index
            pucch_dbm.p0_pucch_updated = ue_report.pucch_updated

    payload = msg.stats_reply_msg.cell_report.add()
    payload.carrier_index = stats.carrier_index
    payload.flags = 1
    payload.noise_inter_report.sfn_sf = frame_id
    payload.noise_inter_report.rip = stats.rip
    payload.noise_inter_report.tnp = stats.tnp
    payload.noise_inter_report.p0_nominal_pucch = stats.p0_nominal_pucch

    await send_rec.encode_msg(msg, writer)


""" user activation events """


async def ue_active_state(msg, ue_state, rnti_value, writer):
    msg.ue_state_change_msg.type = config_common_pb2.FLUESC_ACTIVATED
    config = msg.ue_state_change_msg.config
    config.rnti = rnti_value
    config.transmission_mode = ue_state.transmission_mode
    config.ue_aggregated_max_bitrate_UL = ue_state.ue_aggregated_max_bitrate_UL
    config.ue_aggregated_max_bitrate_DL = ue_state.ue_aggregated_max_bitrate_DL
    config.ue_transmission_antenna = ue_state.ue_transmission_antenna
    config.beta_offset_ACK_index = ue_state.beta_offset_ACK_index
    config.beta_offset_CQI_index = ue_state.beta_offset_CQI_index
    config.beta_offset_RI_index = ue_state.beta_offset_RI_index
    config.ack_nack_simultaneous_trans = ue_state.ack_nack_simultaneous_trans
    config.simultaneous_ack_nack_cqi = ue_state.simultaneous_ack_nack_cqi
    config.aperiodic_cqi_rep_mode = ue_state.aperiodic_cqi_rep_mode
    config.ack_nack_repetition_factor = ue_state.ack_nack_repetition_factor
    config.pcell_carrier_index = ue_state.pcell_carrier_index
    await send_rec.encode_msg(msg, writer)


""" user deactivation events """


async def ue_deactive_state(msg, writer, rnti):
    msg.ue_state_change_msg.type = config_common_pb2.FLUESC_DEACTIVATED
    config = msg.ue_state_change_msg.config
    config.rnti = rnti
    await send_rec.encode_msg(msg, writer)


"""user periodic reply function """


async def user_periodic_func(writer, stats, ue_report):
    global frame_id
    while True:
        await periodic_stats_reply(flexran_pb2.flexran_message(), writer, stats, frame_id, list_of_ue, ue_report)
        frame_id = frame_id + 1
        await asyncio.sleep(0.05)


""" synchronous periodic function in case of no users in the system """


async def no_user_periodic_func(writer, stats):
    global frame_id
    while True:
        await periodic_stats_reply(flexran_pb2.flexran_message(), writer, stats, frame_id, [])
        frame_id = frame_id + 1
        await asyncio.sleep(0.05)


""" Receive LC Config msg """


async def lc_request(reader, writer, lc, rnti):
    msg = flexran_pb2.flexran_message()

    """ receive the lc config request message and send the lc config reply """
    received = await send_rec.decode_msg(msg, reader)

    if received.HasField("lc_config_request_msg"):
        await lc_config(msg, writer, lc, rnti)


""" Function that handles events in the agent. A list of events is generated at the beginning of the measurement.
Then the events are extracted from the list and served accordingly. The type of events include UE activation and
deactivation together with their timestamp.
"""


async def ue_connect(msg, writer, list_of_events, ue_state, lc, reader):
    compare_time = list_of_events[0]['time']
    for ev in range(len(list_of_events)):

        """ Time to wait for the next event """
        await asyncio.sleep(list_of_events[ev]['time'] - compare_time)

        if list_of_events[ev]['eventType'] == 'activated':

            # in case ue was activated generate the rnti (radio network identifier for that ue)
            rnti_value = random.randint(4000, 50000)

            """ append the rnti values for the new users in order to generate the ue report """
            list_of_ue.append(rnti_value)

            """ change the rnti value for each user and send the user active event message """
            await ue_active_state(msg, ue_state, rnti_value, writer)

        else:

            # in case of ue deactivation remove that user from the list of users
            """ Take the rnti value from the list to deactivate the user """
            rnti_value = list_of_ue.pop()
            """ send user deactive event message """
            await ue_deactive_state(msg, writer, rnti_value)

        """ LC Config reply message send """
        await lc_request(reader, writer, lc, rnti_value)
        compare_time = list_of_events[ev]['time']
