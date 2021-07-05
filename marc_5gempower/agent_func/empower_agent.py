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
from  marc_5gempower.agent_func import send_rec
from marc_5gempower.agent_func import initialization
import marc_5gempower.empower_msg.empower_messages as em
import asyncio
import time

""" 
5G-EmPOWER Agent 

Args:
controller_ip: The IP of the FlexRAN controller
controller_port: The running Port of the FlexRAN controller
number_users: The number of users
number_agents: The number of agents
agnt_id: The MAC address of the 5G-EmPOWER agent
measure_agent_delay: Binary that indicates if the delay for the specific FlexRAN agent will be measured or not
"""



async def enode_agent(controller_ip, controller_port, number_users, number_agents, agnt_id, measure_agent_delay):
    eNB_id = b'\x00\x00' + agnt_id
    print("the new enb id is", eNB_id)
    cell_id = 0

    # Message sequential number after the initialization phase
    seq = 5

    loop = asyncio.get_event_loop()

    # Establishing the Controller connection
    reader, writer = await asyncio.open_connection(controller_ip, controller_port)

    # Send the hello message to the controller
    init_msg = encode.encode_hello_response(seq, agnt_id)
    writer.write(init_msg)
    initialization_start = 0
    # In case that measure_agent_delay is True record the start of the agent initialization
    if measure_agent_delay:
        initialization_start = time.time()

    # Send the initialization messages to the controller
    await initialization.init_phase_msg(reader, writer, agnt_id, measure_agent_delay, number_users, number_agents,
                                        initialization_start)

    data = await reader.read(1024)
    msgType, hdr = decode.decode_header(data)
    receivedMsg, offset, event, operation = decode.decode_msg(data, msgType)

    if receivedMsg == em.EP_ACT_RAN_MAC_SLICE:

        if number_users is not None:
            # Get the list of UE events according to the given the user setup
            list_of_events = initialization.set_of_events(number_users)

            """
            Now create the loops with the tasks of the agent including if there are users:
            hb_hello: keep alive messages
            receive_msg: function that receives messages
            events: function that generates all the user events
            cell_measurement: Function that sends all the cell measurements
            ue_periodic_measurement: Function that sends all the user periodic measurements
            """
            task1 = loop.create_task(send_rec.hb_hello(writer, agnt_id))
            task2 = loop.create_task(send_rec.receive_msg(reader, writer, agnt_id))
            task3 = loop.create_task(send_rec.events(writer, list_of_events, [], [], hdr.xid, agnt_id))
            task4 = loop.create_task(send_rec.cell_measurement(writer, agnt_id))
            task5 = loop.create_task(send_rec.ue_periodic_measurement(writer, hdr.xid, agnt_id))
            await asyncio.wait([task1, task2, task3, task4, task5])

        else:

            """
            Since ue reports and ue events are not needed, create the loops with the tasks 
            of the agent including if there are no users:
            hb_hello: keep alive messages
            receive_msg: function that receives messages
            cell_measurement: Function that sends all the cell measurements
            """
            task1 = loop.create_task(send_rec.hb_hello(writer, agnt_id))
            task2 = loop.create_task(send_rec.receive_msg(reader, writer, agnt_id))
            task3 = loop.create_task(send_rec.cell_measurement(writer, agnt_id))
            await asyncio.wait([task1, task2, task3])
