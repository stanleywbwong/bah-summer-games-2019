# Google Earth Output 

To visualize the current status of the live airspace, Google Earth was used to
display the three different elements: the current location of the UAV, the
previous path of the UAV and the potential location for the pilot. 

To display these elements in close to real time, a NetworkLink kml file was used
to repeated refresh each element. Three live files can bee seen in this folder,
livepath, livepilot, and liveposition. Each of them does not contain any
location data, but links to a file that is being overwritten and has it refresh
it every second.

## Current Limitations 
Because Google Earth was not designed to display real time data, it has a
refresh rate cap of 1 refresh per second. This creates a usable interface, but
one that looks choppy and is much slower than the Enforce Field system it
recieves data from. 
Another limitation of Google Earth is that displaying data can only be done from
a kml file, which means that whenever information needs to be updated, it must
be rewritten to the disk, incurring signnificant overhead. A solution for this
could be to create a RAM disk that could be overwritten very quickly, but that
does not solve the issue of Google Earth refreshing only once per second. 
In summary, Google Earth is a start to a vizualization module because it is
quick, easy to setup, well documented, and very forgiving, but is ultimatedly
not designed for this usecase. A realtime vizualizaiton engine designed for this
type of problem should be used.