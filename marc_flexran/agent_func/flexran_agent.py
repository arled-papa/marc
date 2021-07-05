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
import marc_flexran.agent_func.msg_handler as msg_handler
import marc_flexran.agent_func.msg_param as msg_param
import marc_flexran.flexran_msg.flexran_pb2 as flexran_pb2
from marc_flexran.agent_func import initialization
import time
import asyncio

""" 
FlexRAN Agent 

Args:
controller_ip: The IP of the FlexRAN controller
controller_port: The running Port of the FlexRAN controller
number_users: The number of users
number_agents: The number of agents
measure_agent_delay: Binary that indicates if the delay for the specific FlexRAN agent will be measured or not
"""


async def enode_agent(controller_ip, controller_port, number_users, number_agents, measure_agent_delay):
    loop = asyncio.get_event_loop()

    # Establishing the Controller connection
    reader, writer = await asyncio.open_connection(controller_ip, controller_port)

    initialization_start = time.time()
    # Send synchronous ue,lc,enb and hello messages to the controller
    await initialization.sync_messages(flexran_pb2.flexran_message(), reader, writer, number_users, number_agents,
                                       measure_agent_delay, initialization_start)

    # Receive stat request messages from the controller in order to initiate the communication with stats reply message
    received = await send_rec.decode_msg(flexran_pb2.flexran_message(), reader)

    # Get the list of UE events according to the given the user setup
    list_of_events = initialization.set_of_events(number_users)

    # Check if the stats request message has been received
    if received.HasField("stats_request_msg"):
        # If there are users in the system then generate async user and periodic events
        if number_users is not None:
            task1 = loop.create_task(
                msg_handler.ue_connect(flexran_pb2.flexran_message(), writer, list_of_events, msg_param.ue_state(),
                                       msg_param.lc_msg(), reader))
            task2 = loop.create_task(
                msg_handler.user_periodic_func(writer, msg_param.stats_msg(), msg_param.ue_report()))
            await asyncio.wait([task1, task2])

        else:
            # Send only periodic events in case of no users
            await loop.create_task(msg_handler.no_user_periodic_func(writer, msg_param.stats_msg()))
