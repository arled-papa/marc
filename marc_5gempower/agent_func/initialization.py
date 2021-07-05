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

from data_plane.event_generation import events
import marc_5gempower.empower_msg.empower_messages as em
from marc_5gempower.agent_func import encode
from marc_5gempower.agent_func import decode
import time
import os

"""
Initial agent - controller synchronization messages
Args:
reader: Asyncio TCP connection reader object
writer: Asyncio TCP connection writer object
agnt_id: The MAC address of the 5G-EmPOWER agent
measure_agent_dealy: Binary that indicates if the delay for the specific FlexRAN agent will be measured or not
number_users: Number of users per each 5G-EmPOWER agent
number_agents: Number of 5G-EmPOWER agents generated
initialization_start: Time of the FlexRAN agent initialization messages
"""


async def init_phase_msg(reader, writer, agnt_id, measure_agent_delay, number_users, number_agents,
                         initialization_start):
    count = 0
    while True:
        data = await reader.read(1024)

        # Retrieve the message type and the header from the received data
        msgType, hdr = decode.decode_header(data)
        receivedMsg, offset, event, operation = decode.decode_msg(data, msgType)

        if receivedMsg == em.EP_ACT_CAPS:
            print("%%% the received msg is a capability request %%%")
            # If the messages is EP_ACT_CAPS send capabilities accordingly
            await encode.encode_capabilities_response(writer, hdr.xid, hdr.seq, agnt_id)

            count = count + 1

        if receivedMsg == em.EP_ACT_UE_REPORT:
            print("%%% the received msg is a ue report request %%%")
            # If the messages is EP_ACT_UE_REPORT send ue_report accordingly
            await encode.encode_empty_ue_report_response(writer, hdr.xid, hdr.seq, agnt_id)

            count = count + 1

        if receivedMsg == em.EP_ACT_RAN_MAC_SLICE:
            if operation == 4:
                print("%%% set a ran policy %%%")
                count = count + 1


            else:
                print("%%% the received msg is a ran mac slice request %%%")
                count = count + 1
                await encode.encode_ran_mac_slice_response(writer, hdr.xid, hdr.seq, agnt_id)

        # There are 3 initialization messages. After that the initialization is complete with the controller
        if count == 3:
            # print("Initialization done")
            if measure_agent_delay:
                initialization_termination = time.time()
                if not os.path.isdir("flexran_measurements/agent_delay"):
                    os.mkdir("flexran_measurements/agent_delay")
                # Store the results the measured agent delay
                filename = open("5gempower_measurements/agent_delay/Agents_{}_"
                                "Users_{}".format(number_agents, number_users), "a")
                filename.write(str(initialization_termination - initialization_start) + "\n")
                # filename.close()
            break


# Function that generates the number of events according the user count
def set_of_events(number_users):

    # According to the number of users parameter and the data plane model generate user events
    event_df = events("configuration_files/config_eMBB.json")
    # Each event is accompanied with the timestamp and the type (activation, deactivation)
    generated_events = event_df[['time', 'eventType']]

    cnt_deactivations = 0
    cnt_activations = 0
    list_of_events = generated_events.to_dict('records')
    # Output file that contains the generated events in case of debug
    f = open('generated_events.txt', 'w')

    for ev in list_of_events:
        if ev['eventType'] == 'deactivated':
            cnt_deactivations = cnt_deactivations + 1
        else:
            cnt_activations = cnt_activations + 1
        f.write(ev['eventType'])
        f.write(',')
        f.write(str(ev['time']))
        f.write('\n')

    f.write("the number of activations is \n")
    f.write(str(cnt_activations) + '\n')
    f.write("the number of deactivations is \n")
    f.write(str(cnt_deactivations))
    f.close()
    return list_of_events
