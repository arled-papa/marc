import pandas as pd
import json
import paramiko
from scp import SCPClient

"""
Function that fetches all the measurements from the controller back to MARC.

Args:
number_agents: The number of initiated 5G-EmPOWER agents
number_users: The number of users per each initiated 5G-EmPOWER agent
cpu_utilization_data: The data with respect to the cpu utilization measurements
mem_utilization_data: The data with respect to the memory consumption measurements
round_no: The run for which the measurements where performed
"""


def utilization_report(number_agents, number_users, cpu_utilization_data, mem_utilization_data, round_no):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    ssh.connect(hostname="controller's ip", port=22, username="controller's pc username",
                password="controller's pc password")

    # Fetch the measurements started at the controller for memory, cpu and packet utilization
    with SCPClient(ssh.get_transport()) as scp:
        scp.get('~/marc/measurement_tools/cpu_utilization', 'reports/5gempower_cpu_utilization')
        scp.get('~/marc/measurement_tools/mem_utilization', 'reports/5gempower_mem_utilization')
        scp.get('~/marc/measurement_tools/packet_rate_tx', '5gempower_measurements/packet_rate_tx/'
                                                           'agent-{}-users-{}-{}'.format(number_agents, number_users,
                                                                                         round_no))
        scp.get('~/marc/measurement_tools/packet_rate_rx', '5gempower_measurements/packet_rate_rx/'
                                                           'agent-{}-users-{}-{}'.format(number_agents, number_users,
                                                                                         round_no))

    cpu_utilization = list(line.rstrip() for line in open('reports/5gempower_cpu_utilization'))
    mem_utilization = list(line.rstrip() for line in open('reports/5gempower_mem_utilization'))

    cpu_df = pd.DataFrame(cpu_utilization)
    mem_df = pd.DataFrame(mem_utilization)

    # Store the data to the respective folder
    file_name = "5gempower_measurements/agent_{}/Agents_{}_Users_{}_{}" \
        .format(number_agents, number_agents, number_users, round_no)
    mem_file_name = "5gempower_measurements/mem_agent_{}/Agents_{}_Users_{}_{}" \
        .format(number_agents, number_agents, number_users, round_no)

    with open(file_name, 'w') as csv_file, open(mem_file_name, 'w') as mem_csv_file:
            cpu_df.to_csv(csv_file, mode='w', header=False, index=False)
            mem_df.to_csv(mem_csv_file, mode='w', header=False, index=False)


"""
Function that updates configuration files for the user activation and de-activation generation.

Args:
number_agents: The number of initiated 5G-EmPOWER agents
"""


def update_configuration_file(number_users):
    with open('configuration_files/config_eMBB.json', 'r') as configuration_file:
        user_configuration = json.load(configuration_file)

    if number_users is not None:
        user_configuration['slices'][0]['ueDensity'] = int(number_users)
        with open('configuration_files/config_eMBB.json', 'w') as configuration_file:
            json.dump(user_configuration, configuration_file)
