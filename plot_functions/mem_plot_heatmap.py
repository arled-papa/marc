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
import matplotlib.pyplot as plt
import math

# Choose the controller you want to plot: 1) flexran 2) 5gempower 3) altflexran
controller = "flexran"
# Location of the input folder according to the chosen controller
input_folder = "data/{}_measurements".format(controller)

# Location of the output folder storing the generated figures
output_folder = "output_plots/"
# The type of the measurement to plot
measurement = "Memory"


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
value: A list of the generated Memory values for each agent in the agent list
"""
toPlot = {}
# Total number of runs
number_runs = 10
# List of users to plot
list_users = ['None', 10, 30, 50, 100]
# List of agents to plot
list_agents = [1, 5, 10, 30, 50]

for users in list_users:
    # For each user create a list for the average Memory values for each agent
    toPlot[users] = []
    for agents in list_agents:
        # List the contains the final average Memory measurements for each agent
        results = []
        for run in range(number_runs):
            # List the contains the provisional Memory measurements for each configuration
            provisional = []
            # Open the file containing the measurements for the respective configuration
            with open("../{}/mem_agent_{}/Agents_{}_Users_{}_{}".format(input_folder, agents, agents, users, run)) as fp:
                for line in fp:
                    t = (line.split(" "))
                    # Append the provisional Memory measurement to a list
                    provisional.append(float(t[0].rstrip("\n\r")))

            # Collect only the middle measurement points to avoid the transient phase of the measurements
            if run == 0:
                results = provisional[100:350]
            else:
                results = np.add(results, provisional[100:350])

        # Store in the results to plot the average of all runs
        results[:] = [element / number_runs for element in results]

        # Append the results in the list of agents for each user, given a 16 GB RAM convertion
        toPlot[users].append(np.mean(results) * (16000 / 100))

x = np.array(range(len(list_users) + 1))
y = np.array(range(len(list_agents) + 1))

# Heatmap related parameters
intensity = []
for key in toPlot:
    intensity.append(toPlot[key])

# Setup the 2D grid with Numpy
x, y = np.meshgrid(x, y)

cmap = plt.get_cmap('hot')

im = ax.pcolormesh(x, y, intensity, cmap=cmap)
cb = plt.colorbar(im)
cb.ax.tick_params(labelsize=18)
cb.set_label('Memory Utilization [MB]', fontsize=18)
# Xlabel
plt.xlabel('Number of Users', fontsize=24)
# Ylabel
plt.ylabel('Number of Agents', fontsize=24)
plt.tick_params(labelsize=22)
# Tick labels
ax.set_xticklabels([0, 10, 30, 50, 100])
ax.set_yticklabels(list_agents)
# Tick positions
ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5])
# Tick positions
ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
plt.tight_layout()
# Store the figure in the correct output format according to the chosen controller
plt.savefig("{}/{}_memory.pdf".format(output_folder, controller))
plt.show()
