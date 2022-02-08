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

First plot your route using your favorite tool.  Copy your route to a file.
This should be a csv-file, where the first field contains the system name.
As an alternative field-seperator '|' is also accepted.
Empty lines and lines starting with '#' are ignored.

```csv
System Name
Alpha Centauri,for the mug
Lave,Lavian Brandy,for in the mug

#Go back home
Sol
```

Load the route file using the 'Open'-button.

When a route is loaded, the label of the 'Open'-button changes to the
remaining systems in the list.  If you double-click this number the route is
cleared.

The plugin expects you to go through the waypoint systems in order.  When the
plugin gets journal events that indicate you have reached the waypoint system,
it automatically selects the next waypoint system. It also copies to the
system to the clipboard for easy pasting in the Galaxy Map search bar.
