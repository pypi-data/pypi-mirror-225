# Colorset 
A set of classes for working with color legends.

## Usage 
To use the library, you need to import it and call the function getLegend(cs_file, sys_cs_file, colorset_used), 
where cs_file is the full name of the main legend XML file, 
sys_cs_file is the full name of the additional legend XML file, 
and colorset_used is the name of the desired legend.

The function returns a tuple legend, colorType, where legend is an object of the class ColorSetNumerical, ColorSetString, or ColorSetAutomatic, depending on the contents of the legend files, and colorType is a string indicating the type of legend from the list ['numerical', 'string', 'automatic'].

The following methods are supported:

show() - displays the contents of the legend in the standard console. 
createDescription() - automatically fills in the description property. 
valueToColor(value) - calculates the integer color code based on the parameter value.

## Required Files 
Main and additional XML files containing the color legends.

## Integration 
The library requires the presence of lxml.etree for operation.

## Related Projects 
The library was developed for use with its own projects.

## Future Plans 
Implementation of the ability to edit legends and save them in XML files. Integration to work with a PostgreSQL database. Preparation of a GUI - a visual legend editor.

## Current Status 
Debugging.

