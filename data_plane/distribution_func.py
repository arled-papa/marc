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

import numpy as np
import logging

def checkDistr(dic):
    if dic['type'] == "Poisson":
        distribution = np.random.poisson
        distributionParam = (dic['lam'],)
    elif dic['type'] == "Det":
        distribution = returnDetConstant
        distributionParam = (dic['constant'],)
    elif dic['type'] == "Beta":
        distribution = np.random.beta
        distributionParam = (dic['alpha'], dic['beta'])
    elif dic['type'] == "Exp":
        distribution = np.random.exponential
        distributionParam = (1/dic['lam'],)
    else:
        logging.error('No such Distribution "' + dic['type'] + '" defined!')
        raise SystemExit
    return distribution, distributionParam


def returnDetConstant(const):
    return const
