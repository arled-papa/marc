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

from marc_5gempower.agent_func import empower_agent
import marc_5gempower.measurement_helper_func.measurement_func as util_stats_report
import time
import asyncio
import aiomultiprocess as mp

controller_ip = "Your Controller's PC IP"  # Place your own controller ip
controller_port = 2210  # Typical 5G-EmPOWER controller port
measurement_time = 600  # Place your own measurement time (currently 10 min)

"""
This dictionary stores all the agent ids that are recognized by the 5G-EmPOWER controller.
Since the controller only accepts agents that registered at the database this has to be done beforehand
Currently 100 agent ids are registered as follows
"""

agntMAC = {0: b'\x00\x00\x00\x00\x00\x00', 1: b'\x00\x00\x00\x00\x00\x01', 2: b'\x00\x00\x00\x00\x00\x02',
           3: b'\x00\x00\x00\x00\x00\x03', 4: b'\x00\x00\x00\x00\x00\x04', 5: b'\x00\x00\x00\x00\x00\x05',
           6: b'\x00\x00\x00\x00\x00\x06', 7: b'\x00\x00\x00\x00\x00\x07', 8: b'\x00\x00\x00\x00\x00\x08',
           9: b'\x00\x00\x00\x00\x01\x00', 10: b'\x00\x00\x00\x00\x01\x01', 11: b'\x00\x00\x00\x00\x01\x02',
           12: b'\x00\x00\x00\x00\x01\x03', 13: b'\x00\x00\x00\x00\x01\x04', 14: b'\x00\x00\x00\x00\x01\x05',
           15: b'\x00\x00\x00\x00\x01\x06', 16: b'\x00\x00\x00\x00\x01\x07', 17: b'\x00\x00\x00\x00\x01\x08',
           18: b'\x00\x00\x00\x00\x02\x00', 19: b'\x00\x00\x00\x00\x02\x01', 20: b'\x00\x00\x00\x00\x02\x02',
           21: b'\x00\x00\x00\x00\x02\x03', 22: b'\x00\x00\x00\x00\x02\x04', 23: b'\x00\x00\x00\x00\x02\x05',
           24: b'\x00\x00\x00\x00\x02\x06', 25: b'\x00\x00\x00\x00\x02\x07', 26: b'\x00\x00\x00\x00\x02\x08',
           27: b'\x00\x00\x00\x00\x03\x00', 28: b'\x00\x00\x00\x00\x03\x01', 29: b'\x00\x00\x00\x00\x03\x02',
           30: b'\x00\x00\x00\x00\x03\x03', 31: b'\x00\x00\x00\x00\x03\x04', 32: b'\x00\x00\x00\x00\x03\x05',
           33: b'\x00\x00\x00\x00\x03\x06', 34: b'\x00\x00\x00\x00\x03\x07', 35: b'\x00\x00\x00\x00\x03\x08',
           36: b'\x00\x00\x00\x00\x04\x00', 37: b'\x00\x00\x00\x00\x04\x01', 38: b'\x00\x00\x00\x00\x04\x02',
           39: b'\x00\x00\x00\x00\x04\x03', 40: b'\x00\x00\x00\x00\x04\x04', 41: b'\x00\x00\x00\x00\x04\x05',
           42: b'\x00\x00\x00\x00\x04\x06', 43: b'\x00\x00\x00\x00\x04\x07', 44: b'\x00\x00\x00\x00\x04\x08',
           45: b'\x00\x00\x00\x00\x05\x00', 46: b'\x00\x00\x00\x00\x05\x01', 47: b'\x00\x00\x00\x00\x05\x02',
           48: b'\x00\x00\x00\x00\x05\x03', 49: b'\x00\x00\x00\x00\x05\x04', 50: b'\x00\x00\x00\x00\x05\x05',
           51: b'\x00\x00\x00\x00\x05\x06', 52: b'\x00\x00\x00\x00\x05\x07', 53: b'\x00\x00\x00\x00\x05\x08',
           54: b'\x00\x00\x00\x00\x06\x00', 55: b'\x00\x00\x00\x00\x06\x01', 56: b'\x00\x00\x00\x00\x06\x02',
           57: b'\x00\x00\x00\x00\x06\x03', 58: b'\x00\x00\x00\x00\x06\x04', 59: b'\x00\x00\x00\x00\x06\x05',
           60: b'\x00\x00\x00\x00\x06\x06', 61: b'\x00\x00\x00\x00\x06\x07', 62: b'\x00\x00\x00\x00\x06\x08',
           63: b'\x00\x00\x00\x00\x07\x00', 64: b'\x00\x00\x00\x00\x07\x01', 65: b'\x00\x00\x00\x00\x07\x02',
           66: b'\x00\x00\x00\x00\x07\x03', 67: b'\x00\x00\x00\x00\x07\x04', 68: b'\x00\x00\x00\x00\x07\x05',
           69: b'\x00\x00\x00\x00\x07\x06', 70: b'\x00\x00\x00\x00\x07\x07', 71: b'\x00\x00\x00\x00\x07\x08',
           72: b'\x00\x00\x00\x00\x08\x00', 73: b'\x00\x00\x00\x00\x08\x01', 74: b'\x00\x00\x00\x00\x08\x02',
           75: b'\x00\x00\x00\x00\x08\x03', 76: b'\x00\x00\x00\x00\x08\x04', 77: b'\x00\x00\x00\x00\x08\x05',
           78: b'\x00\x00\x00\x00\x08\x06', 79: b'\x00\x00\x00\x00\x08\x07', 80: b'\x00\x00\x00\x00\x08\x08',
           81: b'\x00\x00\x00\x01\x00\x00', 82: b'\x00\x00\x00\x01\x00\x01', 83: b'\x00\x00\x00\x01\x00\x02',
           84: b'\x00\x00\x00\x01\x00\x03', 85: b'\x00\x00\x00\x01\x00\x04', 86: b'\x00\x00\x00\x01\x00\x05',
           87: b'\x00\x00\x00\x01\x00\x06', 88: b'\x00\x00\x00\x01\x00\x07', 89: b'\x00\x00\x00\x01\x00\x08',
           90: b'\x00\x00\x00\x01\x01\x00', 91: b'\x00\x00\x00\x01\x01\x01', 92: b'\x00\x00\x00\x01\x01\x02',
           93: b'\x00\x00\x00\x01\x01\x03', 94: b'\x00\x00\x00\x01\x01\x04', 95: b'\x00\x00\x00\x01\x01\x05',
           96: b'\x00\x00\x00\x01\x01\x06', 97: b'\x00\x00\x00\x01\x01\x07', 98: b'\x00\x00\x00\x01\x01\x08',
           99: b'\x00\x00\x00\x01\x02\x00'}


# Function that terminates all processes once the measurement time has been finalized
def terminate_all_processes(processes):
    target_time = time.time() + measurement_time
    while time.time() < target_time:
        pass
    for proc in processes:
        proc.terminate()


"""
Function that initiates the run of 5G-EmPOWER.

Args: 
agents: The number of 5G-EmPOWER agents to initiate
users: The number of users per each initiated FlexRAN agent
delay: Binary that indicated if agent related delay measurement are taking place
"""


async def run_5gempower(args=None):
    print(args)
    processes = []

    # Generate the user activations and de-activations from the data plane according to the configuration setup
    util_stats_report.update_configuration_file(args["users"])

    measure_agent_delay = False
    if args["agents"]:
        for agnt in range(int(args["agents"])):
            if agnt == int(args["agents"]) - 1:
                # In case that delay is True measure the initialization delay of the FlexRAN agent
                if args["delay"] == "True":
                    measure_agent_delay = True
                    print("Start measuring agent's delay")

            # Each 5G-EmPOWER agent is initiated as a process targeting the 5G-EmPOWER agent function
            task = mp.Process(target=empower_agent.enode_agent, args=(controller_ip, controller_port, args["users"],
                                                                      args["agents"], agntMAC[agnt],
                                                                      measure_agent_delay))
            # Append the process to the list of processes
            processes.append(task)
            # Task initiation
            task.start()
            time.sleep(0.5)
        # Once the measurement has finalized terminate all tasks
        terminate_all_processes(processes)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_5gempower())
    loop.close()
