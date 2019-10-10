# Pilot Locator Assumptions

This document seeks to answer questions regarding the purpose, design structure,
and assumptions made in tracking a UAV pilot.

## PURPOSE
The purpose of creating a pilot tracking module was to supplement the lack of
action caused by the current legal framework for most of the airspace in the US.
Currently, it is illegal to take action against a UAV because it is considered
an aircraft, so the most common legal path is to take action against the
pilot. In order to take action against the pilot, you must know where the
pilot is, hence the creation of a UAV pilot locator module. 

In most cases issues with UAVs arise because pilots are being negilgent and
do not know they are breaking the law. This negilgent pilot was chosen as the
model for this module because it allowed us to make a lot of reasonable
assumptions so that we could come up with a narrow scope to focus on.

## DESIGN STRUCTURE
The current strategy for locating the pilot of a UAV is linked to the radio link
between them and their UAV. At all times a UAV must be within radio range of its
pilot, so at it moves around in space, the potential area that the UAV pilot
could be decreases. This Venn Diagram like reduction is used to reduce a list of
coordinates where the pilot could potentially be located and is displayed in
Google Earth. Once a small enough area is present, the EFOC operator then has
the ability to cross reference that area with topographical data to find areas
that the pilot is likely in.

### Potential Improvements
There are several improvements that can be made to this system to improve
accuracy and reduce the time it would take to locate a UAV pilot. 

The first is a battery link check based on where the UAV currently is. As the
UAV flys around it uses battery and has a smaller range which it can travel. If 
you see a UAV at time 0, the worst case scenario is that it has used half of its
battery to where you can see it and will use half of its battery to get back.
To you that range is a circle with a radius of the UAV's range. If you can see
the UAV at time 2, that means it has used 2 units of its battery, and only could
have used 49 units to arrive and 49 to depart. The longer you see the drone, the
smaller this potential range of travel, the overlap of two circles, one from the
first place it was observed and the other from its current location, the smaller
the overlapping area gets.
The second means of area reduction is much more specific to the location of the
Enforce Field setup. When the system initially detects a UAV, it can be assumed
that the UAV was not in view of any of the other cameras, meaning that pilot
is not located in sight of those cameras and did not fly their UAV through that
airspace. In this inital area reduction, it can be assuded that the pilot is not
inside of the restrcited area, a military base or airport, which is already
taken out in the current implementation. But also that they haven't previously
flown through that area, reducing their potential range.
Further methods of area reduction can be implemented from area access
restriction, fenced areas, and hard to reach places. This was goal of the
topographical cross reference which only returns a heatmap of the area.

## ASSUMPTIONS MADE
In order to narrow the scope of this project several extremely important
assumptions were made, all of which were models of a negligent pilot. 
1) There is a pilot controlling the UAV, its flight has not be preprogrammed.
2) The pilot does not move from where they launched the UAV from.
3) The UAV has not been modified to extend the radio range. 

If potential improvedments are added to this design they will bring on
additional assumptions which need to be stated.