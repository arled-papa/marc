# Table of Contents: #

1. [Introduction to MARC](#introduction-to-marc)

2. [Hardware Requirements](#hardware-requirements)

3. [Software Requirements 5G-EmPOWER](#software-requirements-5gempower)

4. [Running 5G-EmPOWER](#running-5g-empower)

5. [Software Requirements FlexRAN](#software-requirements-flexran)

6. [Running FlexRAN](#running-flexran)

7. [Applying Changes to FlexRAN](#applying-changes-to-flexran)

8. [Software Requirements MARC](#software-requirements-marc)

9. [Running MARC](#running-marc)

10. [Fetching Results](#fetching-results)

11. [Plotting Results](#plotting-results)

# Introduction to MARC #

MARC is a Software-Defined Radio Access Network controller benchmark. This is the original version of the code as it appeared in the journal published at TNSM 2021.
Curenntly, MARC is utilized to benchark [5G-EmPOWER](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8680665) and [FlexRAN](https://dl.acm.org/doi/pdf/10.1145/2999572.2999599) SD-RAN controllers.


# Hardware Requirements #

One PC running a recent Linux distribution. There are no particular hardware requirements. Any reasonably recent laptop/desktop should be able to run the controller.
The tests have been developed with Desktop PCs, each one equipped with an Intel(R) Core(TM) i5-3470 CPU, containing 4 physical CPU cores at frequency 3.2 GHz and 8 GB RAM.
The reference operating system for this guide is Ubuntu 18.04.02 LTS.

# Software Requirements 5G-EmPOWER #

```
sudo apt-get update
sudo apt-get install git
sudo apt-get install python-pip
sudo apt-get install python3-pip
```

python 3.6.7 required (comes usually with Ubuntu 18.04)

If python2.7 is not installed, then install python2.7:

```sudo apt-get install python-minimal```

## Install the Required python Libraries using pip3: ##

```pip3 install construct==2.5.5-reupload  tornado==6.0.3 SQLAlchemy==1.3.10```

## Install the Openssh: ##

```sudo apt-get install openssh-server```

## Install the Required Dependencies for Measurements: ##

```
sudo apt-get install python-psutil==5.6.3
pip install python-iptables==0.14
```

## Create iptable Chains: ##

```
sudo iptables -N TRAFFIC_COUNT_IN (create in counter chain)
sudo iptables -N TRAFFIC_COUNT_OUT (create out counter chain)
sudo iptables -I INPUT -j TRAFFIC_COUNT_IN (redirect in packets)
sudo iptables -I OUTPUT -j TRAFFIC_COUNT_OUT (redirect out packets)
sudo iptables -A TRAFFIC_COUNT_IN -i "your interface" -p tcp --dport "your controller port: usually 2210" -j ACCEPT (count incoming packets)
sudo iptables -A TRAFFIC_COUNT_OUT -o "your interface" -p tcp --sport "your controller port: usually 2210" -j ACCEPT (count outgoing packets)
```

## Manipulate iptable Chains: ##

```
sudo iptables -L -n -v -x ( check the table)
sudo iptables -Z (name of the chain) to reset the counters
```

# Running 5G-EmPOWER #

## Clone 5g-EmPOWER from Github: ##

```
git clone https://github.com/arled-papa/marc.git

cd marc/5G-EmPOWER/

git submodule update --init

mkdir deploy
```

## Copy the Created Database: ##

```cp ~/marc/empower.db ~/marc/5G-EmPOWER/deploy```

## Run 5G-Empower: ##

``` cd ~/marc/5G-EmPOWER
./empower-runtime.py apps.pollers.cellmeasurementspoller --tenant_id=1b3d5de4-dbda-493a-ac3f-b92f9136a243 apps.pollers.uemeasurementspoller --tenant_id=1b3d5de4-dbda-493a-ac3f-b92f9136a243
```

# Software Requirements FlexRAN #

```
sudo apt-get update
sudo apt-get install git
sudo apt-get install python3-pip
sudo apt-get install python-pip
```

python 3.6.7 required (comes usually with Ubuntu 18.04)

If python2.7 is not installed, then install python2.7:

```sudo apt-get install python-minimal```

## Install the Openssh: ##

```sudo apt-get install openssh-server```

## Install Google Protobuf: ##

```
wget https://github.com/google/protobuf/releases/download/v2.6.1/protobuf-2.6.1.tar.gz
tar xzf protobuf-2.6.1.tar.gz
cd protobuf-2.6.1
sudo apt-get update
sudo apt-get install build-essential
sudo ./configure
sudo make
sudo make check
sudo make install 
sudo ldconfig
protoc --version (should be libprotoc 2.6.1)
```

## Install Required Libraries : ##

```sudo apt-get install cmake libboost-all-dev liblog4cxx-dev```

## Install the Pistache Library: ##

```
cd ~
git clone https://github.com/pistacheio/pistache.git
cd pistache
git checkout d6a2ff625d
mkdir build
cd build
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ..
make
sudo make install
sudo ldconfig
```

## Install the Required Dependencies for Measurements: ##

```
sudo apt-get install python-psutil==5.6.3
pip install python-iptables==0.14
```

## Create iptable Chains: ##

```
sudo iptables -N TRAFFIC_COUNT_IN (create in counter chain)
sudo iptables -N TRAFFIC_COUNT_OUT (create out counter chain)
sudo iptables -I INPUT -j TRAFFIC_COUNT_IN (redirect in packets)
sudo iptables -I OUTPUT -j TRAFFIC_COUNT_OUT (redirect out packets)
sudo iptables -A TRAFFIC_COUNT_IN -i "your interface" -p tcp --dport "your controller port: usually 2210" -j ACCEPT (count incoming packets)
sudo iptables -A TRAFFIC_COUNT_OUT -o "your interface" -p tcp --sport "your controller port: usually 2210" -j ACCEPT (count outgoing packets)
```

## Manipulate iptable Chains: ##

```
sudo iptables -L -n -v -x ( check the table)
sudo iptables -Z (name of the chain) to reset the counters
```

# Running FlexRAN #

## Clone FlexRAN from Github: ##

```
git clone https://github.com/arled-papa/marc.git
```
## Compile FlexRAN: ##

```
cd marc/FlexRAN/

./build_flexran_rtc.sh
```

## Run FlexRAN: ##

```
./run_flexran_rtc.sh
```

# Applying Changes to FlexRAN #

```
cd ~
nano marc/FlexRAN/src/rib/rib_updater.h
```

Change the value in the next two functions from 2 to 8 

```
rib_updater(flexran::network::async_xface& xface, Rib& storage)

rib_updater(flexran::network::async_xface& xface, Rib& storage, int n_msg_check)
```

```
nano marc/FlexRAN/src/app/component.h
```

Change the value in the following function from 8 to 2

```
component(rib::Rib& rib, const core::requests_manager& rm)

cd ~/marc/FlexRAN/

./build_flexran_rtc.sh
```

# Software Requirements MARC #

```
sudo apt-get update
sudo apt-get install git
sudo apt-get install python-pip
sudo apt-get install python3-pip
```

python 3.6.7 required (comes usually with Ubuntu 18.04)

## Install Google Protobuf: ##

```
wget https://github.com/google/protobuf/releases/download/v2.6.1/protobuf-2.6.1.tar.gz
tar xzf protobuf-2.6.1.tar.gz
cd protobuf-2.6.1
sudo apt-get update
sudo apt-get install build-essential
sudo ./configure
sudo make
sudo make check
sudo make install 
sudo ldconfig
protoc --version (should be libprotoc 2.6.1)
```

## Install the Required python Libraries: ##

```
pip3 install pandas matplotlib aiomultiprocess construct==2.5.5-reupload
sudo apt-get install python3-paramiko python3-scp
```

## Install the Openssh: ##

```sudo apt-get install openssh-server```

# Running MARC #

## Clone MARC from Github: ##

```
git clone https://github.com/arled-papa/marc.git

cd marc 

mkdir flexran_measurement 5gempower_measurements reports
```

## Modify the File with IP of the Controller of Choice and Username, Password of the Machine Running Controller: ##

```cd marc/marc_flexran/measurement_helper_func/ ```

1) measurement_func.py 
2) connect_controller.py

```cd marc/marc_5gempower/measurement_helper_func/ ```

1) measurement_func.py 
2) connect_controller.py

## Modify the File with IP and Port of the Controller of Choice: ##

```cd marc/marc_flexran/ ```

1) run_flexran.py 
2) benchmark_flexran.py


```cd marc/marc_5gempower/ ```

1) run_5gempower.py 
2) benchmark_5gempower.py

## Run MARC: ##

```
cd marc/
python3 main -c "specify the controller of choice" -a "specify number of agents" -u "specify number of users" -b "specify to do more measurements" -d "specify if you want to measure delay"
```

Running the controller a single time requires specifying the number of agents -a and users -u,  without -b parameters. 
In that case the controller has to be initiated manually.
Otherwise, if -b is "True" then -a, -u are not required since the benchmark_"controller".py file has the configurations of choise.
In that case ssh is used to connect to the controller automatically, so the controller shall not be initiated manually.
In case that delay measurements are required then -d shall be "True".

# Fetching Results #

The results are stored in the PC running MARC as follows:

```cd marc/```

1) 5gempower_measurements
2) flexran_measurements

Be aware that when changes are made on the FlexRAN controller the results should be copied to a folder named altflexran_measurements

# Plotting Results #

Currently ```~/marc/data.zip``` contains the original data from original version of the MARC as it appeared in the journal published at TNSM 2021. 

## Install Python Dependencies: ##

``` pip3 install pandas==0.25.3 matplotlib==3.1.1 numpy==1.16.2```

## Plot Current Measurements: ##

```
git clone https://github.com/arled-papa/marc.git

cd marc

unzip data.zip

cd plot_functions

mkdir output_plots

```

### For CPU Measurements: ###

```nano cpu_plot.py```

Select the controller you want to plot

```python3 cpu_plot.py```

### For Memory Measurements: ###

```nano mem_plot_heatmap.py```

Select the controller you want to plot

```python3 mem_plot_heatmap.py```

### For Delay Measurements: ###

```nano delay_plot.py```

Select the controller you want to plot

```python3 delay_plot.py```

### For Controller Received Msg/Bytes Measurements: ###

```nano rx_rate_plot.py```

Select the controller you want to plot also the msg/s or Kbit/s

```python3 rx_rate_plot.py```

### For Controller Transmitted Msg/Bytes Measurements: ###

```nano tx_rate_plot.py```

Select the controller you want to plot also the msg/s or Kbit/s

```python3 tx_rate_plot.py```

All the plots are stored in:

``` ~/marc/plot_functions/output_plots ```

## Plot New Measurements: ##

Run the measurements according to your configurations. Store the results into a folder named data in the marc directory as in the current version. 
Inside the data folder store the 3 folders: 1) 5gempower_measurements 2) flexran_measurements 3) altflexran_measurements.
Run the plot_functions as above.



