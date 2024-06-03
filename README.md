# Project 4: Brevet time calculator with Ajax
Author: Ryan Doolittle

Reimplemented the RUSA ACP controle time calculator with flask and ajax.
Data is stored in a database on "submit", which is retrieved on "display"

Credits to Michal Young for the initial version of this code.

## ACP controle times

acp_times.py uses table-driven logic to calculate open and close times for brevet controles. The table can be easily modified to allow for different controle specifications. Explicit open and close times for the final checkpoint are included according to article 9 of https://rusa.org/pages/rulesForRiders

Controle inputs in the webpage can be entered as floats, however the kilometer input is rounded down to the nearest km before calculation in accordance with ACP rules. All times are rounded to the nearest minute. If a controle location is beyond the brevet length (i.e. controle at 305 km on a 300 km brevet), the brevet length is used in the time calculations.

NOTE: According to ACP rules, if a controle point is is over 20% longer than the brevet distance, the controle is considered invalid. This calculator does not account for this, and will just use the brevet distance in calculations.

## API Specifications
http://<host:port>/listAll returns all open and close times in the database
http://<host:port>/listOpenOnly returns open times only
http://<host:port>/listCloseOnly returns close times only

JSON and CSV formats are available for all three of these representations, i.e.:
http://<host:port>/listOpenOnly/json returns open times only in JSON format
http://<host:port>/listAll/csv returns all open and close times in CSV format

If no format is specified, JSON is assumed.

Additionally, there is a query parameter, "top=k," that allows for pulling only the top "k" controle times in ascending order, i.e.:
http://<host:port>/listOpenOnly/json?top=3 returns the top 3 open times only (in ascending order) in JSON format
http://<host:port>/listCloseOnly/csv?top=6 returns the top 6 close times only (in ascending order) in CSV format

This parameter is has no functionality for listAll, as the top k open times are not necessarily from the same controles as the top k close times.

## Sources
https://rusa.org/pages/acp-brevet-control-times-calculator
https://rusa.org/pages/rulesForRiders
https://rusa.org/octime_acp.html