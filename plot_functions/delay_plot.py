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
measurement = "Delay"


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
value: A list of the generated delay values for each agent in the agent list
"""
toPlot = {}

# For altflexran plot up to 400 users, else for other controllers up to 100
if controller == "altflexran":
    # List of users to plot
    list_users = ["None", 50, 100, 400]
else:
    # List of users to plot
    list_users = ["None", 50, 100]
# List of agents to plot
list_agents = [1, 30, 50]

for users in list_users:
    #  For each user create a list for the average delay values for each agent
    toPlot[users] = []
    # List of agents to plot
    for agents in list_agents:
        # List the contains the final average delay measurements for each agent
        results = []
        # Open the file containing the measurements for the respective configuration
        with open("../{}/delay/Agents_{}_Users_{}".format(input_folder, agents, users)) as fp:
            for line in fp:
                t = line.rstrip("\n\r")
                # Store the results to plot for the delay
                results.append(float(t))

        # Append the results in the list of agents for each user
        toPlot[users].append(results)

number_boxplots = 0
patches = []
for users in list_users:
    meanpointprops = dict(marker=markers[number_boxplots], markeredgecolor='black',
                          markerfacecolor='w', markersize=12, markeredgewidth=3)

    # Boxplot object
    boxplot = ax.boxplot(toPlot[users], patch_artist=True,
                         positions=np.array(range(len(toPlot[users]))) * 5.0 + number_boxplots, sym='',
                         widths=1.5, meanprops=meanpointprops, showmeans=True)

    # Set the colors for the boxplot
    set_box_color(boxplot, colors[number_boxplots])

    t1 = "patch_{}".format(users)
    if users == 'None':
        users = 0
    # Set the legend for the figure
    legend = mlines.Line2D([], [], color=colors[number_boxplots], marker=markers[number_boxplots], linestyle='-',
                           markersize=12, label='Users={}'.format(users), markeredgecolor='black', markeredgewidth=3,
                           markerfacecolor='w')

    patches.append(legend)
    number_boxplots = number_boxplots + 1

# Xlabel
plt.xlabel('Number of Agents', fontsize=24)
# Ylabel
plt.ylabel('{} [s]'.format(measurement), fontsize=24)
plt.tick_params(labelsize=22)
# Tick labels
ax.set_xticklabels([1, 30, 50])
# Tick positions
ax.set_xticks([1.1, 6.1, 11.1])
plt.yscale('log')
# Legend parameters
lg = plt.legend(loc="upper left", handles=patches, prop={'size': 18})
plt.ylim(10 ** (-3), 10 ** 3)
plt.tight_layout()
# Store the figure in the correct output format according to the chosen controller
plt.savefig("{}/{}_delay.pdf".format(output_folder, controller))
plt.show()
