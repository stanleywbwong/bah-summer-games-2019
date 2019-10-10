# Drone Simulator

This purpose of this simulator is to provide a stream of seemingly read data to the Enforce Field Operator Console (EFOC) or any other program reading from the Enforce Field server. This simulator uploades false timestamp, coordinate and offset data to the Enforce Field Redis Server in a channel called 'simulation'. This data is formatted in the same manner as the layer4 data provided by the layer4 channel.

## How to run
The simulator is composed of one main file, simulator.py and a supporting class Track, found in track_importer.py. To use simulator, you must have track files either recorded by a GPS or created manually. These track files should be put in the tracks folder and will be atomatically read into the program if they have a .kml extension.  
  
__NOTE: The track files required for the simulator need to have coordinates as well as time. Path files created in Google Earth are not equivalent to track files because they only posses coordinates.__  
__NOTE: The simulator does not check the .kml files for errors. If .kml files are added to the tracks folder that are not properly formatted the simulator will crash__  
  
To start the simulator just just run:  
  
  `python simulator.py`
  
You can then navigate the program using the onscreen options.
  
## Contributors

Peter Malinovsky (Tufts '20)

This project was developed as part of the Booz Allen Summer Games program at the Lexington, MA branch.

## License

This project is licensed under Booz Allen etc. __Check with David about this__

## Acknowledgments

* Our challenge leaders, David Levine and Regina Farren, for guiding us throughout our work
* Bruh
