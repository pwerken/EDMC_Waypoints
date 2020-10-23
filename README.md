# EDMC_Waypoints

Plugin for [EDMC](https://github.com/EDCD/EDMarketConnector/wiki) that
automatically copies to clipboard the next waypoint on a route you planned.

## Installation

 1. If you are on linux, you'll need to make sure *xclip* is installed before
    using the plugin.
 2. Clone this repository or download and extract the [repository zip archive](https://github.com/pwerken/EDMC_Waypoints/archive/master.zip)
	in your EDMC plugin directory.
 3. Then (re)start EDMC.

## Usage

First plot your route using your favorite tool.
Copy your route to a file, where each line is a new waypoint.

This can be a csv-file, where the first field contains the system name.
As an alternative field-seperator '|' is also accepted.
Empty lines and lines starting with '#' are ignored.

```csv
System Name
Alpha Centauri,for the mug
Lave,Lavian Brandy,for in the mug

#Go back home
Sol
```

Load this route file using the 'O'-button.

The 'X'-button clears the current route.
