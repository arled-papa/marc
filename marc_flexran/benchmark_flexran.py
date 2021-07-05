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

import marc_flexran.measurement_helper_func.controller_connection as connect_controller
import marc_flexran.measurement_helper_func.measurement_func as util_stats_report
from marc_flexran.run_flexran import run_flexran
import time
import os
import asyncio

"""
Function that initiates the benchmarking of FlexRAN.
It connects via ssh to the controller given the IP and it starts the measurements of cpu, memory, throughput, delay if
indicated. At the end of the measurements the controller is stopped and all the measurements are terminated.

Args: 
list_agents: The list of FlexRAN agents to initiate for the benchmark
list_users: The list of users for each initiated 5G-EmPOWER agent
args["delay"]: Binary that indicated if agent related delay measurement are taking place
"""


def run_benchmark_flexran(args=None):

    list_agents = ['1', '5', '10', '30', '50']
    list_users = [None, '10', '30', '50', '100']

    controller_ip = "Your Controller's PC IP"

    # Generate measurement files if not present
    if not os.path.isdir("flexran_measurements/packet_rate_rx"):
        os.mkdir("flexran_measurements/packet_rate_rx")

    if not os.path.isdir("flexran_measurements/packet_rate_tx"):
        os.mkdir("flexran_measurements/packet_rate_tx")

    for agent in list_agents:
        if not os.path.isdir("flexran_measurements/agent_{}".format(agent)):
            os.mkdir("flexran_measurements/agent_{}".format(agent))
        if not os.path.isdir("flexran_measurements/mem_agent_{}".format(agent)):
            os.mkdir("flexran_measurements/mem_agent_{}".format(agent))
        for users in list_users:
            # Number of runs per each configuration
            runs = 3
            for run in range(runs):
                # Start the FlexRAN controller
                connect_controller.connect_flexran(controller_ip, "start")
                time.sleep(10)
                # Start cpu consumption measurements
                connect_controller.connect_flexran(controller_ip, "cpu_stats")
                # Start memory consumption measurements
                connect_controller.connect_flexran(controller_ip, "mem_stats")
                # Start controller sent packet measurements
                connect_controller.connect_flexran(controller_ip, "packet_tx", agent, users, run)
                # Start controller received packet measurements
                connect_controller.connect_flexran(controller_ip, "packet_rx", agent, users, run)

                #if users is not None:
                    
                cpu_utilization_data = [{"Number of Agents": agent, "Number of Users": users,
                                         "cpu utilization": 'None'}]
                mem_utilization_data = [{"Number of Agents": agent, "Number of Users": users,
                                         "mem_utilization": 'None'}]
                # Arguments for running MARC for 5G-EmPOWER
                argsv = {"agents": agent, "users": users, "delay": args["delay"]}
                loop = asyncio.get_event_loop()
                loop.run_until_complete(run_flexran(argsv))

                # Stop the controller
                connect_controller.connect_flexran(controller_ip, "stop")
                # Terminate all measurement scripts
                connect_controller.connect_flexran(controller_ip, "terminate_all_scripts")
                # Fetch all the measurements from the controller
                util_stats_report.utilization_report(agent, users, cpu_utilization_data, mem_utilization_data, run)
                time.sleep(10)


if __name__ == '__main__':
    run_benchmark_flexran()
