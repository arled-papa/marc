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

import logging
import time
import iptc


"""
Function that utilizes iptables to retrieve from the counter the amount of packet and bytes received
by the respective controller.
"""


def packet_rate():

    logging.basicConfig(
       filename='packet_rate_tx',
       format='%(asctime)s %(message)s',
       level=logging.INFO,
       datefmt='%H:%M:%S')

    table = iptc.Table(iptc.Table.FILTER)
    chain = iptc.Chain(table, 'TRAFFIC_COUNT_IN')
    while True:
        for rule in chain.rules:
            for match in rule.matches:
                if match.dport == '2210':
                    table.refresh()
                    # get the previous count of packets
                    (packets, bytes) = rule.get_counters()
                    rx_pkts = packets
                    logging.info(rx_pkts)
                    time.sleep(1)
                    

if __name__ == "__main__":
    packet_rate()
