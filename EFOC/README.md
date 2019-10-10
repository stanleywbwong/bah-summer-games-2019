# EFOC GUI
Graphical User Interface for Enforce Field

## Installation
Use the package manager pip to install necessary packages.

```bash
pip install pyshp
```
```bash
pip install shapely
```
If the pip install is unsuccessful, then select the correct version and download the package from this website https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely
```bash
pip install geopy
```
```bash
pip install pandas
```
```bash
pip install pyproj
```
```bash
pip install simplekml
```
```bash
pip install redis
```
## Setup Window
<img width="284" alt="efoc_setup" src="https://media.github.boozallencsn.com/user/7905/files/e9663e80-ba9b-11e9-804f-d034f132b5e5"> 

Enter category of airspace, specific location name of airspace, altitude/boundary height of interest, and protocol. Note for FAA Controlled Airspace, the user should enter the three letter IATA code for airports. The altitude is the maximum height in which the geofence reaches. Anything above that altitude is ignored during detection. Protocols are user-customizable and define the rules of engagement. The user's inputs are stored in a text file called EFOC_setup.txt. The text file is read when the GUI starts up and autofills the GUI entries with the user's previously saved inputs. Click run to start the program and begin searching for drones in the airspace. 


### Shapefiles and Airspace
Each category corresponds to a specific shapefile. Selecting a category creates a object which stores the shapefile data of that category. Shapefile data are converted to geoJSON format so they can easily be parsed.  
The program searches for the location which the user entered and specifically pulls out all shapefile data relating to that location, most importantly the coordinates which make up the geofence.  
Since the coordinates do not include altitude, the user must specifally enter how high the geofence can go. 

## Detection Window

<img width="214" alt="loading_screen" src="https://media.github.boozallencsn.com/user/7905/files/1adf0a00-ba9c-11e9-8bbb-b76d527fd945">
Once the run button is clicked, the shapefile data is loaded in, the user's current configuration is saved, and the detection window will pop up. Also, Google Earth will open and the geofence boundary can be viewed. In the backend, the program subscribes to the Redis server and a separate thread is created to handle any new drone coordinates from the server. The coordinates from the server are continuously being checked to see if they are within the boundary. The user can press cancel to end the drone monitoring and go back to the setup window.   

## Google Earth Visualization
The selected airspace geofence, the drone's current position, the drone's previous path, and potential drone pilot location are stored in KML files and are opened upon startup of Google Earth. The drone's previous path is being plotted in realtime. A list of the drone's coordinates is stored and continously plotted. The drone's current position is updated with new server coordinates. The potential drone pilot location changes as the drone moves, drawing a circle representing the drone's transmitter range. The intersection of each transmitter range circle is taken and displayed on Google Earth. 

## Drone Detected Window
<img width="404" alt="warning" src="https://media.github.boozallencsn.com/user/7905/files/a6962e00-ad5b-11e9-93df-bb02aea05fb0">  
Once the coordinate from the server is within the geospatial boundary, a warning window pops up telling the user the drone is within the airspace. Pressing the OK button triggers the Rules of Engagement module. 

## Rules of Engagement
<img width="221" alt="roe" src="https://media.github.boozallencsn.com/user/7905/files/17d5e100-ad5c-11e9-8b32-8bd36282cedb">  
The dialog and questions of the following windows are based on the user profile selected in the setup screen. The profiles essentially tell how the program should behave. Currently, there are only default profiles for each airspace category which all ask two questions: Is the drone authorized and if it is causing immediate danger. The user can create his or her own profile with custom questions and answers to those questions.  
<img width="264" alt="roe_end" src="https://media.github.boozallencsn.com/user/7905/files/54a1d800-ad5c-11e9-95d0-02a3ea338d63">  

### Drone Pilot Locator
On the final window displaying actions needed to be taken, there is a button to locate the drone pilot. This creates a heat map of the last intersection circle saved, cross-referencing the area with a land cover database. Different land cover are assigned weights depending on how likely a drone pilot would be and correspond to a color in the heat map. There is also an activate C-UAS system button which currently has no functionality. In the future, it can be programmed to an actual C-UAS system. 




