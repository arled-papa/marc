import pandas as pd
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
measurement = "CPU"


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

# Figure related parameterscd
fig_width = 6.9  # Convert pt to inch
golden_mean = (math.sqrt(5) - 1.0) / 2.0  # Aesthetic ratio
fig_height = fig_width * golden_mean  # height in inches

fig = plt.figure(figsize=(fig_width, fig_height))
ax = fig.add_subplot(111)

"""
Dictionary that stores the data that need to be stored: 
key: The amount of users according to the users list
value: A list of the generated delay values for each agent in the agent list
"""
toPlot = {}
# Total number of runs
number_runs = 10
# List of users to plot
list_users = ['None', 30, 50, 100]
# List of agents to plot
list_agents = [1, 5, 10, 30, 50]

for users in list_users:
    # For each user create a list for the average CPU values for each agent
    toPlot[users] = []
    for agents in list_agents:
        # List the contains the final average CPU measurements for each agent
        results = []
        for run in range(number_runs):
            # List the contains the provisional CPU measurements for each configuration
            provisional = []
            # Open the file containing the measurements for the respective configuration
            with open("../{}/agent_{}/Agents_{}_Users_{}_{}".format(input_folder, agents, agents, users, run)) as fp:
                for line in fp:
                    t = (line.split(" "))
                    # Append the provisional CPU measurement to a list
                    provisional.append(float(t[0].rstrip("\n\r")))

            # Collect only the middle measurement points to avoid the transient phase of the measurements
            if run == 0:
                results = provisional[100:350]
            else:
                results = np.add(results, provisional[100:350])

        # Store in the results to plot the average of all runs
        results[:] = [element / number_runs for element in results]

        # Append the results in the list of agents for each user
        toPlot[users].append(results)

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

# Ylabel
plt.xlabel('Number of Agents', fontsize=24)
# Xlabel
plt.ylabel('{} utilization [%]'.format(measurement), fontsize=24)
plt.tick_params(labelsize=22)
# Tick labels
ax.set_xticklabels([1, 5, 10, 30, 50])
# Tick positions
ax.set_xticks([1.5, 6.5, 11.5, 16.5, 21.5])
# Legend parameters
lg = plt.legend(loc="upper left", handles=patches, prop={'size': 18})
plt.ylim(0, 105)
plt.tight_layout()
ax.axvspan(19, 23.5, alpha=0.2, color='gray')
ax.axvspan(9.1, 13.8, alpha=0.2, color='gray')
ax.axvspan(-0.5, 4, alpha=0.2, color='gray')
# Store the figure in the correct output format according to the chosen controller
plt.savefig("{}/{}_cpu.pdf".format(output_folder, controller))
plt.show()
