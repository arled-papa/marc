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
import marc_flexran.agent_func.send_rec as send_rec
import marc_flexran.agent_func.msg_handler as msg_handler
import marc_flexran.agent_func.msg_param as msg_param
import time
import os


"""
Initial agent - controller synchronization messages
Args:
msg: Is the type of FlexRAN message
reader: Asyncio TCP connection reader object
writer: Asyncio TCP connection writer object
measure_agent_dealy: Binary that indicates if the delay for the specific FlexRAN agent will be measured or not
init_start_time: Time of the FlexRAN agent initialization messages
"""


async def sync_messages(msg, reader, writer, number_users, number_agents, measure_agent_delay, init_start_time):
    initialization_start = init_start_time
    # Decoded received messages
    received = await send_rec.decode_msg(msg, reader)

    if received.HasField("hello_msg"):
        # If the messages is Hello reply accordingly
        await msg_handler.hello_msg(msg, writer)

    count_init_msg = 0
    while True:
        received = await send_rec.decode_msg(msg, reader)
        if received.HasField("enb_config_request_msg"):
            # If the messages is Enb_config reply accordingly
            count_init_msg = count_init_msg + 1
        if received.HasField("ue_config_request_msg"):
            # If the messages is Ue_config reply accordingly
            count_init_msg = count_init_msg + 1
        if received.HasField("lc_config_request_msg"):
            # If the messages is Lc_config reply accordingly
            count_init_msg = count_init_msg + 1
        # There are 3 initialization messages. After that the initialization is complete with the controller
        if count_init_msg == 3:
            # print("Initialization done")
            if measure_agent_delay:
                # Contains the time of the termination of the initialization of the agent
                initialization_termination = time.time()
                if not os.path.isdir("flexran_measurements/agent_delay"):
                    os.mkdir("flexran_measurements/agent_delay")
                # Store the results the measured agent delay
                filename = open("flexran_measurements/agent_delay/Agents_{}_"
                                "Users_{}".format(number_agents, number_users), "a")
                filename.write(str(initialization_termination - initialization_start) + "\n")
                filename.close()
            break

    await msg_handler.enb_config(msg, msg_param.enb_msg(), writer)
    await msg_handler.ue_config(msg, writer)
    await msg_handler.init_lc_config(msg, writer)


# Function that generates the number of events according the user count
def set_of_events(number_users):
    if number_users is not None:
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
