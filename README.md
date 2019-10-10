# Enforce Field Operator Console (EFOC)

_The official project of the Booz Allen Summer Games 2019 Lexington, MA team._

A GUI-based application for Enforce Field (EF) operators, extending the base EF setup. Includes live Google Earth visualizations of UAS tracks and airspace boundaries, (live video feed via gstreamer?), and interactive, customizable console upon UAS detection. Written primarily in Python.

## Getting Started

+ Enforce Field must be cloned and built locally: https://github.boozallencsn.com/ENF/enforcefield. See __Installing__ for more details.
+ Clone via SSH from within the BAH CSN network: `git clone git@github.boozallencsn.com:Malinovsky-Peter/summer-games.git`

## Installing 

These instructions will let you run EFOC on your local machine for testing/development purposes. Note that EFOC requires the base EF setup (2 separate Nvidia Jetson TX2's running EF) before it will run on a host computer. Instructions below.

### Prerequisites

For base EF build:
+ 2 Nvidia Jetson TX2's (with OS/base software installed via Nvidia SDK Manager
+ 2 webcams, one connected to each TX2
+ Host server locally connected to both TX2s

For EF Operator Console (runs on host):
+ Python 3.7+

### Installing

+ On each TX2, clone/build cpp-redis: https://github.com/Cylix/cpp_redis/wiki/Mac-&-Linux-Install
+ On each TX2, clone/build opencv w/ contrib modules: https://github.com/opencv/opencv_contrib/blob/master/README.md
+ ON each TX2 and on host, clone via SSH/build EF:
    + Install dependencies: `sudo apt install ntp ntpdate cmake qt4-qmake libqt4-dev libglew-dev libi2c-dev libpgs-dev libboost-dev libboost-all-dev nodejs npm`
    + `git clone git@github.boozallencsn.com:ENF/enforcefield.git`
    + `git checkout devkit-dev`
    + Comment out submodule warning from lines 5-22 in enforcefield/jetson/inference/CMakeLists.txt
    + In enforcefield/jetson/ `mkdir build && cd build`, `cmake ..`
    + Clone jetson-utils from https://github.com/dusty-nv/jetson-utils.git, rename as utils, and move to enforcefield/jetson/inference/
    + Before building:
        + Copy contents of enforcefield/jetson/inference/utils/cuda/ into jetson/inference/
        + Copy commandLine.h, filesystem.h from jetson/inference/utils/ into jetson/inference/
        + Rename cudaRectOutlineOverlay() as cudaRectFill() in jetson/inference/detectNet.cpp line 631
        + Modify /jetson/inference/detectnet-camera/detectnet-camera.cpp:
            + Line 14 comment out NO_SERVER
            + Line 62 change DEFAULT_CAMERA to "/dev/video1"
            + Line 172, 234 change IP address to server IP (192.168.10.110)
            + Line 502 change void* to float* declaration
        + Copy contents of jetson/inference/utils/image/ into jetson/inference/
        + Change path of stb_truetype.h in line 32 of jetson/inference/cudaFont.cu
        + Copy mat33.h from jetson/inference/utils/ into jetson/inference/
        + Copy contents of jetson/inference/utils/display/ into jetson/inference/detectnet-camera/ __EXCEPT__ glDisplay.cpp
        + Copy contents of jetson/inference/utils/camera/ into jetson/inference/detectnet-camera/ __EXCEPT__ gstCamera.cpp
        + Copy contents of jetson/inference/utils/threads/ into jetson/inference/detectnet-camera/
        + Copy timespec.h from jetson/inference/utils/ into jetson/inference/detectnet-camera
     + `sudo make -j5 install` in build directory
     + Compare with latest EF repo to see if above steps are no longer required

To run EF (on TX2's) w/ example codrone model:
+ On both TX2's:
  + `cd enforcefield/jetson/build/inference/aarch64/bin`
  + Create and cd to enforcefield/jetson/inference/data/networks/codrone
  + Untar codrone model (zip file available here: https://nvidia.box.com/shared/static/0wbxo6lmxfamm1dk90l8uewmmbpbcffb.gz)
  + Create class_labels.txt file with model name 'codrone' on line 1
  + Modify enforcefield/jetson/inference/detectNet.cpp
    + Line 314: add class_labels.txt file path in argument list after 0.0f
    + Line 408: add new else if case for codrone model
  + Run `./detectnet-camera codrone` and enter camera configuration data when prompted
    + Other models must be trained for EF to recognize, and can be installed similarly
+ On host computer:
  + `git checkout server_update`
  + `cd /enforcefield/redis_server/`
  + Change file paths in startup.sh
  + Run `./start_redis.sh && ./startup.sh` (several terminals should pop up)
  + If EF is running with cameras on both TX2s, messages should be displayed on pop-up terminals
  
To run EFOC:
+ On host computer:
  + `git clone git@github.boozallencsn.com:Malinovsky-Peter/summer-games.git`
  + `git checkout dev`
  + Additional steps:
      + Download NLCD Land Cover Data (for pilot locator functionality) at https://s3-us-west-2.amazonaws.com/mrlc/NLCD_2016_Land_Cover_L48_20190424.zip
      + Unzip and copy the .ige file into summer-games/EFOC/GIS_data
      + Install ArcGIS Pro (also for pilot locator functionality and use of the arcpy module) at https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview. Be sure to activate ArcGIS and enable the Spatial Analyst and Image Analyst extensions through the Esri license manager online.
  + `cd summer-games/EFOC/`
  + `python EFOC.py`

## Contributors

Timothy Dowling (Denison '21), Allison Greenberg (Cornell '21), Peter Malinovsky (Tufts '20), Stanley Wong (Yale '22), and David Yu (Georgia Tech '21)

This project was developed as part of the Booz Allen Summer Games program at the Lexington, MA branch.

## License

This project is licensed under Booz Allen etc. __Check with David about this__

## Acknowledgments

* The original EF development team (Jamie Ter Beest, Aylin Uyar, Sanjana Thirumalai, Alex Tejada, Jeremy White) for permitting us to expand on their project
* Our challenge leaders, David Levine and Regina Farren, for guiding us throughout our work
