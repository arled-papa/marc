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

import json
import os
import logging
import collections
import pandas as pd
from data_plane.distribution_func import checkDistr

"""
This Script can be implemented as a library to create a list with a Simulation of PDU-Setup and -Release events
triggered by UEs in a 5G-Network.

As an Input, a Config-File must be given with information about the amount of UEs, the distribution of Inter-Arrival
time as well as the distribution of the duration of each setup PDU-Session. Additional Slice-Parameters must be given
as well as further parameters for the distribution.

"""


def events(configPath):
    logconfig = {'format': '[%(asctime)s.%(msecs)-3d: %(name)-16s - %(levelname)-5s] %(message)s',
                 'datefmt': "%H:%M:%S"}
    logging.basicConfig(level=logging.DEBUG, **logconfig)

    exists = os.path.isfile(configPath)
    if not exists:
        logging.error('No Config-File ' + configPath + ' found! Make sure the configPath is correct!\n')
        raise SystemExit

    with open(configPath) as file:
        cfg = json.load(file)
    # we check how many active slices we have in cases that network slicing is activated
    numberActiveSlices = len(cfg['slices'])
    simulationTime = cfg['totalSimTime']

    """
    Parameters of the event
    1) Duration of the simulation
    2) The type of the event (ue activation or deactivation)
    3) Number of slices if activated
    4) The type of slice (eMBB, URLLC, MTC)
    """
    eventParams = ['time', 'eventType', 'sliceNumber', 'sliceType']
    eventList = list()
    event = collections.namedtuple('event', eventParams)

    # Initiate Value of currSliceNumber to 0
    currSliceNumber = 0

    for currSlice in cfg['slices']:

        currSliceNumber += 1
        numberUEs = int(currSlice['ueDensity']) * currSlice['cellArea']
        # retrieve the activation distribution function and the activation distribution parameters
        actDistrFunc, actDistrParam = checkDistr(currSlice['activation'])
        deactDistrFunc, deactDistrParam = checkDistr(currSlice['deactivation'])

        for ue in range(numberUEs):

            #  Initiate time-variable t to 0, reset t at the beginning of each simulated ue
            t = 0
            while t < simulationTime:

                t += actDistrFunc(*actDistrParam)

                if t < simulationTime:
                    currEvent = event(time=t, eventType='activated', sliceNumber=currSliceNumber,
                                      sliceType=currSlice['sliceType'])
                    eventList.append(currEvent)
                t += deactDistrFunc(*deactDistrParam)
                if t < simulationTime:
                    currEvent = event(time=t, eventType='deactivated', sliceNumber=currSliceNumber,
                                      sliceType=currSlice['sliceType'])
                    eventList.append(currEvent)


        else:
            logging.info(
                '######## Slice ' + str(currSliceNumber) + '/' + str(numberActiveSlices) + 'finished! ########')

    logging.info('All Users finished!')

    """
        Create a pandas DataFrame in variable df consisting of Data from eventList with columns saved in eventParams
        Sort df by time
    """
    df = pd.DataFrame(eventList)
    df.sort_values(["time"], inplace=True)

    return df
