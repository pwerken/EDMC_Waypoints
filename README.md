# Waypoints plugin for [EDMC](https://github.com/Marginal/EDMarketConnector/wiki)

Plugin for [EDMC](https://github.com/EDCD/EDMarketConnector/wiki) that
automatically copies the next waypoint of your planned route the clipboard.

## Installation

 1. If you are on linux, you'll need to make sure *xclip* is installed before
    using the plugin.
 2. Clone this repository *or* download and extract the
    [repository zip archive](https://github.com/pwerken/EDMC_Waypoints/archive/main.zip)
    in your EDMC plugin directory.
 3. Then (re)start EDMC.

## Usage

 1. Plot your route using your favorite tool.
 2. Save the route to a local file.
 3. Load the route file into the plugin by right-clicking the label to bring
    up the context menu.

Once a route is loaded, the plugin displays the next system on your path. When
you reach that system, the plugin automatically advances to the next
destination and copies its name to your clipboard.

You can left-click the system name to manually copy it to the clipboard again.

## Route CSV format

The route must be saved as CSV file. Lines starting with # and empty lines are
ignored.  Either a comma ',' or a vertical bar '|' are accepted as field
separator.

The header line is optional for both formats. If the first line does not match
a recognized header, the plugin automatically treats it as a waypoint system.

### Proximity route

The file contains coordinates for each system.  The plugin automatically
targets the closest available system from your current location.

If coordinate parsing fails, the plugin fallsback to treating it as a
sequential route.

```csv
System name,x,y,z
Sol,0,0,0
Alpha Centauri,3.03125,-0.09375,3.15625
```

### Sequential route

The first field must contain the system name. Any other fields are ignored.
The plugin expects you to travel through these waypoint systems in sequential
order.

```csv
System Name
Alpha Centauri,for the mug
Lave,Lavian Brandy,for in the mug

#Go back home
Sol
```
