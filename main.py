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

from marc_flexran.run_flexran import run_flexran
from marc_flexran.benchmark_flexran import run_benchmark_flexran
from marc_5gempower.run_5gempower import run_5gempower
from marc_5gempower.benchmark_5gempower import run_benchmark_5gempower
import argparse
import asyncio

"""
Function that initiates MARC.
It runs either the FlexRAN controller of the 5G-EmPOWER in a single run mode or benchmark mode.
If MARC is run in non benchmark mode i.e., -b "False" then the number of agents and users needs to be specified and
the controller has to be manually start. Otherwise if -b is "True" then number of agents and users does not need to be
specified since the benchmark python file contains all the necessary data for the number of agents and users.
In that case the controller is automatically started by MARC via ssh. Do not start it manually.
Finally, -d can be "True" or "False" in both cases. It indicates whether agent delay measurements are to be taken.

Example:

python3 main.py -c flexran -b True -d True (run flexran, benchmark with delay measurements)
python3 main.py -c 5gempower -a 5 -u 10 (run 5gempower, single run with 5 agents and 10 users per agent)

Args: 
-c: The controller to be benchmarked or connected
-a: The number of agents to initiate
-u: The number of users to initiate for each agent
-d: Binary, "True" if the agent delay is to be measured "False" otherwise
-b: Binary, "True" if controller is to be benchmarked "False" otherwise
"""


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-controller', '-c', help='specify the controller you want to benchmark')
    parser.add_argument('-agents', '-a', help='specify the number of agents')
    parser.add_argument('-users', '-u', help='specify the number of users')
    parser.add_argument('-delay', '-d', help="specify if you want to measure the agent delay")
    parser.add_argument('-benchmark', '-b', help='specify if you want to run multiple runs and benchmark')
    args = parser.parse_args()

    if args.controller == "5gempower":
        if args.benchmark == "True":
            print("Benchmark 5G-EmPOWER")
            # Arguments for running MARC
            argsv = {"delay": args.delay}
            run_benchmark_5gempower(argsv)
        else:
            print("Run 5G-EmPOWER")
            # Arguments for running MARC
            argsv = {"agents": args.agents, "users": args.users, "delay": args.delay}
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_5gempower(argsv))
    elif args.controller == "flexran":
        if args.benchmark == "True":
            print("Benchmark FlexRAN")
            # Arguments for running MARC
            argsv = {"delay": args.delay}
            run_benchmark_flexran(argsv)
        else:
            print("Run FlexRAN")
            # Arguments for running MARC
            argsv = {"agents": args.agents, "users": args.users, "delay": args.delay}
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_flexran(argsv))


if __name__ == "__main__":
    main()

