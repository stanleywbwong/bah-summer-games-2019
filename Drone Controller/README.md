<!-- language: lang-none -->

# Drone Controller
  
This drone controller is specific to the DJI Tello. For swarming capabilities the Tello EDU is required, a different model than the "normal" Tello. The Tello comes in only white while the Tello EDU comes in only black. Make sure you get the right one because none of the swarming code will work on the normal Tello

## Drone Swarm
  
### Requirements:
+ Computer with configurable network settings
+ 2.4 GHz Wireless Access Point (WAP)
+ Several Tello EDU drones


### Run a Swarm Demo
The current configuration should support a demo if the drones in the Lexington, MA office are used. The computer running the demo just needs to be connected to a wireless network with an SSID of "drone" and a password of "drones". If this setup can be achieved all that has to be run is `python swarm.py` in the swarm_controller folder.

### Setup 

1) Setup the WAP to have with a specific SSID and password. For our setup the SSID "drones" and password "swarm123" was used. In our case a CentOS server with a wifi card was used because a WAP was not allowed. The command:  
`nmcli dev wifi hotspot ifname wlan0 ssid drones password "swarm123"`  
was used to create a WiFi hotspot where wlan0 was the card name after running the `nmcli` command.
2) Turn on the first Tello EDU and use a computer or phone to connect to the WiFi network it creates. All commands sent to the drone are via UDP packets sent to the Tello's address, by default 192.168.10.1, and port 8889. Responses come on port 53486 and are UDP packets as well. (Tello documents the recieving port as 8890 which does report UDP data but not the relevant command responses. Still unknown on why port 53486 is never mentioned) On a phone several UDP apps are available or on a computer a simple python scrip can be written. A simple UDP python script can be found in individual_controller/new_drone.py.
3) To connect the Tello EDU to the WAP send the command: <br/>
`command` <br/>
followed by <br/>
`ap drones swarm123` <br/>
4) The drone should reboot and connect to the WAP. Use the WAP software to note the drones new IP address. If possible use manual addressing to give the drone a static IP for organization. We were not able to do so because of the CentOS hotspot setup which uses DHCP by default.
5) Repeat steps 2-5 for each drone giving each drone a unique IP address.

### Configuration
Once the drones have been configured, modify the configuration file, config.txt, with the relevant information. The file should come in the format:

    drones: list of drones actively used
    folder: folder where commands for active drones are located
    timeout: timeout value in seconds (default 5)
    bind_port: server bind port (default 53486)
    drone_addr: list of all drone addresses (default 10.42.0.171 10.42.0.207 10.42.10.174 10.42.0.192 10.42.0.187)
    drone_port: list of all drone ports (default 8889 8889 8889 8889 8889)
  
The current config file used by the summer games team is:

    drones: 0 2 3 4
    folder: 4_drone_square_full_sync
    timeout: 3
    bind_port: 53486
    drone_addr: 10.42.0.171 10.42.0.207 10.42.10.174 10.42.0.192 10.42.0.187
    drone_port: 8889 8889 8889 8889 8889

This specifies that the command in 4_drone_square_full_sync will be run using drones 0, 2, 3, and 4 as drones 0, 1, 2, 3. The command files are agnostic to the drone it is controlling, so the the order of the drone list specifies which drone will recieve which commands.

### Understanding Swarm Demos
For full Tello documentation the current Tello SDK is verion 2.0 and can be found here: https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf

The easiest way to understand how the drone swarming works, start by looking in the folder 2_drone_square and opening the two files side by side. To understand the commands here we must understand what Mission Pads are and how they're setup.


#### Mission Pads

Mission Pads are usefull for improving the accuracy and 3D location of the Tello EDUs while they are running. We define a square configuration as a square with the center of each pad 1 meter apart aligned along the same axis. Pad 1 is lower left, pad 2 is lower right, pad 3 is upper right, pad 4 is upper left. It looks like: 

    Sqaure Setup
    _____            _____
    | 4 |  <- 1m ->  | 3 |
    ‾‾‾‾‾            ‾‾‾‾‾
      ^                ^  
      |                |  
     1 m              1 m 
      |                |  
      v                v  
    _____            _____
    | 1 |  <- 1m ->  | 2 |
    ‾‾‾‾‾            ‾‾‾‾‾
    
    Leap Frog Setup
    _____
    | 6 | 
    ‾‾‾‾‾  
      ^  
      |  
    .5 m  
      |  
      v  
    _____  
    | 5 |  
    ‾‾‾‾‾
      .
      .
      .
    _____
    | 2 | 
    ‾‾‾‾‾  
      ^  
      |  
    .5 m  
      |  
      v  
    _____  
    | 1 |  
    ‾‾‾‾‾
    
The coordinate system used by the mission pads is the standard coordinate axis with the positive x direction being the direction of the rocket ship. For the Square Setup relative to mission pad 1, pad 2 is located at (0, -100) pad 3 is at (100,-100) and pad 4 is at (100, 0). The magnitude of the coordinates is in centimeters so 100 cm is 1 meter.

For this demo, refer to the 2_drone_sqaure demo setup.
Both drones are issued the action `command` which tells them to listen to commands from the Tello SDK. Next, both drones are told `takeoff`. Both drones will takeoff and respond with `ok` if they are both okay. The next command, the wait command is required because both drones will not respond at the same time. One drone may take much longer to takeoff and stabilize, causing loss of synchronization. To rectify this, the wait command can be used to delay any further command. The command `wait for drone 1 step 2` does exactly what is sounds like, it tells drone 0 to wait for drone 1 to complete step 2. If both drones wait for each other to complete the previous step, the will execute the next step simultaneously, whenever the last drone issues a response of `ok`. The command `mon` enables Mission Pad detection and `mdirection 2` enables sensing in both directions. The next command `go 0 -100 70 100 m1` tells drone 0 to fly to the coordinate (0, -100, 70), 70 being the height in cm. Based on this setup the drone will stop directly over mission pad 2. The drone is then told `ccm 90` to spin counter-clockwise 90 degrees and then to `go 0 0 70 20 m2` which it should already be at. This step is used to realign the drones and calibrate their location so that any unintention wandering is removed. The subsequent commands repeat this same wait and move action until the drones return to their orignal location and land. 

The 4_drone_square_demo is just an extension of the 2_drone_square demo with a drone on each pad. The following command can be seen in the drone0.txt file to sync drone 0 with all the other drones:

    wait for drone 1 step 2
    wait for drone 2 step 2
    wait for drone 3 step 2
    
Only when drones 1, 2, and 3 have reached at least step 2 will drone 0 move on to the next step. Drones 1, 2, and 3 do not have to wait for drone 0 if they do not want to, they do wait in this demo, and they do not have to be on exactly step 2 for drone 0 to move on, they only have had to successfully reach step 2 at some time.

### Creating Swarm Demos
1) To create a new drone swarm demo, create a new folder with your demo name. 
2) Create N new files named drone0.txt throught drone(N-1).txt where N is the number of drones you want in your demo.
3) Each drone file must start with the action `command` before anything can be done.
4) Typically the next command is `takeoff` but any of the read commands can be executed like `battery?` or `time?`.
5) Write out all of the action items you want the drone to do, WITHOUT wait statments.
6) Once all of the action items have been written out, append line numbers to the front of each line like `1 command`.
7) Once all line numbers are in, add wait statments and DO NOT apply line numbers to the wait statements. Line numbers are used for commands that are actually sent to the Tello and wait statments are taken out by the controller.
8) Change the config.txt file to reflect the folder of the demo you want to run and the drone information as needed.
9) Run swarm.py 

NOTE: The controller keeps track of the current line number and does not use the number you put in the command file. If you mess up in counting the program will not know and will wait on the correct line instead of the line you want it to. Unexpected behavior may result if you do not count line numbers properly.

### Current Demos
There are currently (6) drone swarm demos. They are:
    2_drone_leapfrog
    2_drone_sidefrog
    2_drone_sqaure
    4_drone_square
    4_drone_square_full_sync
    4_drone_testing
    
#### 2_drone_leapfrog
This demo should be run on the Leap Frog Setup with 6 pads. Drone 0 should be on pad 1 facing pad 2 and drone 1 should be on pad 2 facing pad 3.

#### 2_drone_sidefrog
This demo is setup the same way as 2_drone_leapfrog. Instead of going over each other the drones should swing sideways around each other.

#### 2_drone_sqaure
This demo should be run on the Square Setup with 4 pads. Drone 0 starts on pad 1 and faces pad 2 and drone 2 starts on pad 3 and faces pad 4. 
