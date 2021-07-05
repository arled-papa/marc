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

import psutil
import logging
import time


"""
Function that retrieves the process_id of the respective controller and measurements the cpu consumption
"""


def utilization():

   logging.basicConfig(
        filename='mem_utilization',
        format='%(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

   for p in psutil.process_iter(attrs=['pid', 'name']):
     if p.info['name'] == 'rt_controller':
       pid = p.info['pid']
       process_id = psutil.Process(pid)
   while True:
        time.sleep(1)
        logging.info(process_id.memory_percent())

if __name__ == "__main__":
    utilization()
