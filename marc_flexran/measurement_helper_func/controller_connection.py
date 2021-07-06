import paramiko
import multiprocessing as mp

processes = []


"""
Function that establishes the connection to the respective controller.

Args:
address: The IP address of the controller
command: The specific python command used to run the controller
status: The specific action that you want to run for instance start, stop the controller or measure 
"""


def start(address, command, status=None):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=address, port=22, username="controller's pc username",
                password="controller's pc password")
    chan = ssh.get_transport().open_session()

    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    stdin.write("controller's pc password\n")
    stdin.flush()

    print(stdout.readlines())


"""
Function that connects to the specific controller and performs measurements according to the specific action with 
respect to cpu, memory consumption, received and transmitted packet rate.

Args:
address: The IP address of the controller
status: The specific action that you want to run for instance start, stop the controller or measure 
agents: The number of FlexRAN agents
userDensity: The number of users per each FlexRAN agent
count: The number of run for which the benchmark is utilized
"""


def connect_flexran(address, status, agents=None, users=None, runs=None):
    if status == "start":
        task = mp.Process(target=start,
                          args=(address, "cd ~/marc/FlexRAN; sudo "
                                         "./run_flexran_rtc.sh", "start"))

    elif status == "stop":
        task = mp.Process(target=start, args=(address, "sudo pkill -9 rt_controller"))

    elif status == "cpu_stats":
        command = 'cd ~/marc/measurement_tools; ' \
                  'sudo rm -rf cpu_utilization; sudo python flexran_cpu_utilization.py'
        task = mp.Process(target=start, args=(address, command))

    elif status == "packet_rx":
        command = "cd ~/marc/measurement_tools;" \
                  " sudo rm -rf packet_rate_rx; sudo python packet_monitor_rx.py"
        task = mp.Process(target=start, args=(address, command))

    elif status == "packet_tx":
        command = "cd ~/marc/measurement_tools;" \
                  " sudo rm -rf packet_rate_tx; sudo python packet_monitor_tx.py"
        task = mp.Process(target=start, args=(address, command))

    elif status == "mem_stats":
        command = "cd ~/marc/measurement_tools;" \
                  " sudo rm -rf mem_utilization; sudo python flexran_mem_utilization.py"
        task = mp.Process(target=start, args=(address, command))

    elif status == "terminate_all_scripts":
        task = mp.Process(target=start, args=(address, "sudo pkill -9 python"))

    processes.append(task)
    task.start()
