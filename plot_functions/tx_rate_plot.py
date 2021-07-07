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
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import math

# Choose the controller you want to plot: 1) flexran 2) 5gempower 3) altflexran
controller = "flexran"
# Location of the input folder according to the chosen controller
input_folder = "data/{}_measurements".format(controller)

# Location of the output folder storing the generated figures
output_folder = "output_plots/"
# The type of the measurement to plot
measurement = "tx Rate"

# Binary indicating whether we want to plot msg/s or Kbit/s for the packet_rate_rx
# If True we plot msg/s, otherwise False we plot Kbit/s
plot_msg = False

# The type of the output format either bytes or msg
out_format = None


# Boxplot related function to manipulate the color of the boxplots
def set_box_color(bp, color):
    print(color)
    for box in bp['boxes']:
        # change outline color
        box.set(color='#5f9ea0', linewidth=2)
        # change fill color
        box.set(color=color)

    # Change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color=color, linewidth=2)

    # Change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(color=color, linewidth=2)

    # Change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='black', linewidth=2)

    # Change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', color='#cd5c5c', alpha=0.1)


# Markers used for plotting
markers = ['s', 'o', 'p', 'd', 'x']

# Colors used for plotting
colors = ['burlywood', 'darkcyan', 'olive', 'firebrick']

# Figure related parameters
fig_width = 6.9  # Convert pt to inch
golden_mean = (math.sqrt(5) - 1.0) / 2.0  # Aesthetic ratio
fig_height = fig_width * golden_mean  # height in inches

fig = plt.figure(figsize=(fig_width, fig_height))
ax = fig.add_subplot(111)

"""
Dictionary that stores the data that need to be stored: 
key: The amount of users according to the users list
value: A list of the generated tx_rate values for each agent in the agent list
"""
toPlot = {}
# Total number of runs
number_runs = 10
# List of users to plot
list_users = ['None', 30, 50, 100]
# List of agents to plot
list_agents = [1, 5, 10, 30, 50]

for users in list_users:
    # For each user create a list for the average packet_rate_tx values for each agent
    toPlot[users] = []
    for agents in list_agents:
        # The number of bytes received by the controller
        bytesCnt = 0
        # List that contains the number of messages received by the controller per each agent
        resultsMsg = []
        # List that contains the number of bytes received by the controller per each agent
        resultsBytes = []
        # The measurement files from 20 to 29 contain measurements for packet_rate_tx
        for run in range(20, 20 + number_runs):
            # List the contains the provisional number of messages received by the controller for each agent
            provisionalMsg = []
            # Open the file containing the measurements for the respective configuration
            with open("../{}/packet_rate_tx/agent-{}-users-{}-{}".format(input_folder, agents, users, run)) as fp:
                for line in fp:
                    t = (line.split(" "))
                    bytesCnt = bytesCnt + 1
                    if bytesCnt % 2 != 0:
                        provisionalMsg.append(int(t[1].rstrip("\n\r")))
            # Collect only the middle measurement points to avoid the transient phase of the measurements
            if run == 20:
                resultsMsg = provisionalMsg[100:350]

            else:
                resultsMsg = np.add(resultsMsg, provisionalMsg[100:350])

        resultsMsg[:] = [element / number_runs for element in resultsMsg]

        # Calculate the number of received messages by substracting two adjacent values in the list
        resultsMsgFinal = []
        for diff in range(len(resultsMsg) - 1):
            resultsMsgFinal.append(resultsMsg[diff + 1] - resultsMsg[diff])

        if plot_msg:
            # If plotting msg True then save msg
            out_format = "msg"
            toPlot[users].append(resultsMsgFinal)

        for run in range(20, 20 + number_runs):
            provisionalBytes = []
            with open("../{}/packet_rate_tx/agent-{}-users-{}-{}".format(input_folder, agents, users, run)) as fp:
                for line in fp:
                    t = (line.split(" "))
                    bytesCnt = bytesCnt + 1
                    if bytesCnt % 2 == 0:
                        provisionalBytes.append(int(t[1].rstrip("\n\r")))

            if run == 20:
                resultsBytes = provisionalBytes[100:350]

            else:
                resultsBytes = np.add(resultsBytes, provisionalBytes[100:350])

        # Convert bytes to Kbit
        resultsBytes[:] = [8 * element / (10 * 1000) for element in resultsBytes]

        # Calculate the number of received bytes by substracting two adjacent values in the list
        resultsBytesFinal = []
        for diff in range(len(resultsBytes) - 1):
            resultsBytesFinal.append(resultsBytes[diff + 1] - resultsBytes[diff])

        if not plot_msg:
            # If plotting msg False then save bytes
            out_format = "bytes"
            toPlot[users].append(resultsBytesFinal)


# Indicator of how many boxplots exist for each x value to plot
number_boxplots = 0
patches = []

for users in list_users:
    # Properties for the mean value of the boxplot
    mean_props = dict(marker=markers[number_boxplots], markeredgecolor='black',
                      markerfacecolor='w', markersize=12, markeredgewidth=3)

    # Boxplot object
    boxplot = ax.boxplot(toPlot[users], notch=True, patch_artist=True,
                         positions=np.array(range(len(toPlot[users]))) * 5.0 + number_boxplots, sym='', widths=1.5,
                         meanprops=mean_props, showmeans=True)

    # Set the colors for the boxplot
    set_box_color(boxplot, colors[number_boxplots])

    # Set the legend for the figure
    legend = mlines.Line2D([], [], color=colors[number_boxplots], marker=markers[number_boxplots], linestyle='-',
                           markersize=12, label='Users={}'.format(users), markeredgecolor='black', markeredgewidth=3,
                           markerfacecolor='w')

    patches.append(legend)
    number_boxplots = number_boxplots + 1

# If we chose to plots the msg/s then the ylim differs as well as labels
if plot_msg:
    plt.ylim(0, 3000)
    # Xlabel
    plt.xlabel('Number of Agents', fontsize=24)
    # Legend parameters
    lg = plt.legend(loc="upper left", prop={'size': 18}, handles=patches, ncol=1)
    # Ylabel
    plt.ylabel('Rate [msg/s]'.format(measurement), fontsize=24)
else:
    # If we chose to plots the Kbit/s then the ylim differs and scale is log
    # Xlabel
    plt.xlabel('Number of Agents', fontsize=24)
    # Ylabel
    plt.ylabel('Rate [Kbit/s]'.format(measurement), fontsize=24)
    plt.yscale('log')
    # Legend parameters
    lg = plt.legend(loc="upper left", prop={'size': 18}, handles=patches, ncol=2)
    plt.ylim(10 ** 0, 10 ** 4.2)

plt.tick_params(labelsize=22)
# Tick labels
ax.set_xticklabels([1, 5, 10, 30, 50])
# Tick positions
ax.set_xticks([1.5, 6.5, 11.5, 16.5, 21.5])
ax.axvspan(19, 23.5, alpha=0.2, color='gray')
ax.axvspan(9.1, 13.8, alpha=0.2, color='gray')
ax.axvspan(-0.5, 4, alpha=0.2, color='gray')
plt.xlim(-0.5, 23.6)
plt.tight_layout()
# Store the figure in the correct output format according to the chosen controller
plt.savefig("{}/{}_packet_rate_tx_{}.pdf".format(output_folder, controller, out_format))
plt.show()