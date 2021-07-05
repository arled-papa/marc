# Table of Contents: #

1. [Hardware Requirements](#hardware-requirements)

2. [Software Requirements 5G-EmPOWER](#software-requirements-5gempower)

3. [Running 5G-EmPOWER](#running-5g-empower)

4. [Software Requirements FlexRAN](#software-requirements-flexran)

5. [Running FlexRAN](#running-flexran)

6. [Applying Changes to FlexRAN](#applying-changes-to-flexran)

7. [Software Requirements MARC](#software-requirements-marc)

8. [Running MARC](#running-marc)

9. [Fetching Results](#fetching-results)

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


