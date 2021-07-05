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

from marc_flexran.agent_func import flexran_agent
import marc_flexran.measurement_helper_func.measurement_func as util_stats_report
import time
import asyncio
import aiomultiprocess as mp

controller_ip = "Your controller's PC IP"  # Place your own controller ip
controller_port = 2210  # Typical FlexRAN controller port
measurement_time = 600  # Place your own measurement time (currently 10 min)


# Function that terminates the initial agent to avoid control delegation messages
def terminate_agent(agent, task):
    if agent == 0:
        time.sleep(1)
        task.terminate()


# Function that terminates all processes once the measurement time has been finalized
def terminate_all_processes(processes):
    target_time = time.time() + measurement_time
    while time.time() < target_time:
        pass
    for proc in processes:
        proc.terminate()


"""
Function that initiates the benchmarking of FlexRAN.

Args: 
agents: The number of FlexRAN agents to initiate
users: The number of users per each initiated FlexRAN agent
delay: Binary that indicated if agent related delay measurement are taking place
"""


async def run_flexran(args=None):
    processes = []

    # Generate the user activations and de-activations from the data plane according to the configuration setup
    print(args)
    util_stats_report.update_configuration_file(args["users"])
    measure_agent_delay = False
    if args["agents"]:
        """ 
        In this ( args.agent + 1 ) shows that one agent will be discarded to avoid the controller control
        delegation messages 
        """
        for agnt in range(int(args["agents"]) + 1):
            if agnt == int(args["agents"]) - 1:
                # In case that delay is True measure the initialization delay of the FlexRAN agent
                if args["delay"] == "True":
                    measure_agent_delay = True
                    print("Start measuring agent's delay")

            # Each FlexRAN agent is initiated as a process targeting the FlexRAN agent function
            task = mp.Process(target=flexran_agent.enode_agent,
                              args=(controller_ip, controller_port, args["users"], args["agents"], measure_agent_delay))
            # Append the process to the list of processes
            processes.append(task)
            # Task initiation
            task.start()
            time.sleep(0.5)
            # Terminate the initial agent to avoid delegation control messages
            terminate_agent(agnt, task)
        # Once the measurement has finalized terminate all tasks
        terminate_all_processes(processes)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_flexran())
    loop.close()
