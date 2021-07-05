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

import marc_flexran.flexran_msg.stats_common_pb2 as stats_common_pb2
from collections import namedtuple

# generation of data for each type of message according to the FlexRAN protocol

def enb_msg():
    enb = {'cell_id': 0, 'pusch_hopping_offset': 0, 'hopping_mode': 0, 'n_sb': 0, 'phich_resource': 0,
           'phich_duration': 0,
           'dl_bandwidth': 50, 'ul_bandwidth': 50, 'ul_cyclic_prefix_length': 0, 'dl_cyclic_prefix_length': 0,
           'antenna_ports_count': 1, 'duplex_mode': 1, 'prach_config_index': 0,
           'mac_contention_resolution_timer': 5, 'max_HARQ_Msg3Tx': 0, 'n1PUCCH_AN': 0, 'deltaPUCCH_shift': 1,
           'nRB_cqi': 0, 'prach_freq_offset': 2, 'ra_response_window_size': 7,
           'enable_64QAM': 0, 'carrier_index': 0, 'dl_freq': 2685, 'ul_freq': 2565, 'eutra_band': 7,
           'dl_pdsch_power': -27, 'ul_pusch_power': -96, 'srs_subframe_config': 0, 'srs_bw_config': 0,
           'srs_mac_up_pts': 0
           }
    return namedtuple("enb_msg", enb.keys())(*enb.values())


def stats_msg():
    stats = {'carrier_index': 0, 'sfn_sf': 0, 'rip': 0, 'tnp': 0, 'p0_nominal_pucch': -104}
    return namedtuple("stats_msg", stats.keys())(*stats.values())


def trigger_msg():
    trigger_stat = {'reception_status': 0, 'tpc': 2, 'serv_cell_index': 0}
    return namedtuple("trigger_msg", trigger_stat.keys())(*trigger_stat.values())


def ue_report():
    ue_report = {'flags': 95, 'phr': 0, 'pending_mac_ces': 1, 'queue_size': 0,
                 'queue_delay': 0, 'pdu_size': 0, 'dl_serv_cell_index': 0, 'ul_serv_cell_index': 0, 'ri': 0,
                 'type': stats_common_pb2.FLCSIT_P10, 'wb_cqi': 15,
                 'carrier_index': 0, 'rip': 0, 'tnp': 0, 'p0_nominal_pucch': -104, 'sinr': 0, 'pucch_dbm': -104,
                 'pucch_serv_cell_index': 0, 'pucch_updated': 0, 'bsr': 0
                 }
    return namedtuple("ue_report", ue_report.keys())(*ue_report.values())


def init_ue_report():
    ue_report = {'flags': 30, 'phr': 0, 'pending_mac_ces': 0, 'queue_size': 0,
                 'queue_delay': 0, 'pdu_size': 0, 'dl_serv_cell_index': 0, 'ul_serv_cell_index': 0, 'ri': 0,
                 'type': stats_common_pb2.FLCSIT_P10, 'wb_cqi': 0,
                 'carrier_index': 0, 'rip': 0, 'tnp': 0, 'p0_nominal_pucch': -104, 'sinr': 0, 'pucch_dbm': -104,
                 'pucch_serv_cell_index': 0, 'pucch_updated': 0, 'bsr': 0
                 }
    return namedtuple("ue_report", ue_report.keys())(*ue_report.values())


def ue_state():
    ue_state = {'transmission_mode': 0, 'ue_aggregated_max_bitrate_UL': 0, 'ue_aggregated_max_bitrate_DL': 0,
                'capabilities': "", 'ue_transmission_antenna': 2,
                'beta_offset_ACK_index': 0, 'beta_offset_CQI_index': 8, 'beta_offset_RI_index': 0,
                'ack_nack_simultaneous_trans': 0, 'simultaneous_ack_nack_cqi': 0,
                'aperiodic_cqi_rep_mode': 3, 'ack_nack_repetition_factor': 0, 'pcell_carrier_index': 0,
                'time_alignment_timer': 7, 'tti_bundling': 0, 'max_HARQ_tx': 4
                }
    return namedtuple("ue_state", ue_state.keys())(*ue_state.values())


def lc_msg():
    lc = {'direction': 2, 'qos_bearer_type': 0, 'qci': 1
          }
    return namedtuple("lc_msg", lc.keys())(*lc.values())
