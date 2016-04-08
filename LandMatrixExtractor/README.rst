Land Matrix data Importer
================================

:Download URL: http://landmatrix.org/get-the-detail/database.csv?download_format=xml

Process
^^^^^^^

#. The importer downloads an XML file containing all the info available of Land Matrix
#. After, it converts each item element of the XML into an intermediate object that represents it (deal).
#. After, it converts the deals into DealAnalyserEntry
#. Finally, it converts the DealAnalyserEntry into Observations (landportal intermediate entity)


A deal contains:

* Country (pristine name that is storage in the XML)
* Date (a year (YYYY). View more info)
* Production hectares (integer)
* Intended hectares (integer)
* Contract hectares (integer)
* Sectors (list of topics obtained from intention field)
* Negotiation status (available values: INTENDED, CONCLUDED, FAILED


A DealAnalyserEntry contains:

* Country
* First date (year YYYY)
* Last date (year YYYY)
* Indicator
* The composed value for country-date

It looks that the file that contains the entire database has a name that does not depend on dates, so it could be possible that in the next time that the importer need to execute the Download url may not change. If it does, the new URL must be specified in "url_download", in the configuration.ini file. 

This importer downloads the entire landmatrix database in XML format, but the observations have a complex nature, hard to fit in the general model. 
A node of information in the landmatrix does not refer to a concrete country, with a concrete indicator and a single value in a concrete date. 
The indicators built are aggregations of values, such as "total number of deals in some sector".

The python project of the importer includes a file "strategy.txt" where the indicators are detailed.


The date assigned to each observation is the highest date found when parsing all the deals. 
For this reason, when executing again the importer to incorporate new data, 
it may be something to consider removing from the system all the old observation 
and run the program in historical mode.

Date
^^^^
Each country will only have an observation per indicator (the date will be the same for all the indicators)
The date is an interval

The start date of the interval is 2000
From http://www.landmatrix.org/en/about/#what-is-a-land-deal
"Deals must: - Have been initiated since the year 2000"

The end date is obtained parsing the negotiation_status field.
The end date (last date) of the interval is calculated. The value is the maximun between all the deals years.The ini


Historical: The importer is prepared to ignore data with a date lower than the value specified in the "first_valid_year" field 
(that can be manually set or automatically calculated by the importer) of the configuration.ini file. 
However, doing this, we will get observations of data aggregates between the specified date and the current one, 
meanwhile the old observations are aggregates of every available date. The meaning will not be consistent. 
By removing all the old observations we will obtain new ones that are aggregates of the old and the new values.

How to calculate the total hectares
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The algorithm to obtain the value to add to the total hectares is:
1) Try to obtain the contract hectares
2) If not, try to obtain the intended hectares
3) If not, try to obtain the production hectares
4) If not, not add any value

If the value of the hectares is zero (or below), the proccess discard this value and tries the next one in the chain.


Upper categories calculation algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is two upper categories in the LandMatrix: Agriculture and Forestry.
The values of the indicators related to them are the aggregation of the values of the subcategories that contains.

In production
^^^^^^^^^^^^^
The algorithm to calculate the indicators "Total Number of Deals in Production" and 
"Total Hectares in Deals in Production" take into account deals with 
"implementation_status" equals to "In operation (production)".


INDICATORS SUPPORTED
====================

:0: Total Number of Deals
:12: Total Hectares in Deals

:10: Total Number of Concluded Deals
:14: Total Hectares in Concluded Deals

:9: Total Number of Intended Deals
:13: Total Hectares in Intended Deals

:11: Total Number of Failed Deals
:40: Total hectares of Failed Deals

:41: Total Number of Deals in Production
:15: Total Hectares in Deals in Production

:1: Total Number of Agriculture Deals
:24: Total Hectares in Agriculture Deals

:2: Total Number of Conservation Deals
:25: Total Hectares in Conservation Deals

:3: Total Number of Forestry Deals
:26: Total Hectares in Forestry Deals

:4: Total Number of Industry Deals
:27: Total Hectares in Industry Deals

:5: Total Number of Renewable Energy Deals
:28: Total Hectares in Renewable Energy Deals

:6: Total Number of Tourism Deals
:29: Total Hectares in Tourism Deals

:7: Total Number of Deals of Other Topic
:30: Total Hectares in Deals of Other Topic

:8: Total Number of Deals of Unknown Topic
:31: Total Hectares in Deals of Unknown Topic

:16: Total number of biofuel (Agriculture) deals
:32: Total hectares in biofuel (Agriculture) deals

:17: Total number of Food crops (Agriculture) deals
:33: Total hectares in Food crops (Agriculture) deals

:18: Total number of Livestock (Agriculture) deals
:34: Total hectares in Livestock (Agriculture) deals

:19: Total number of Non-food agricultural commodities (Agriculture) deals
:35: Total hectares in Non-food agricultural commodities (Agriculture) deals

:20: Total number of Agriunspecified (Agriculture) deals
:36: Total hectares in Agriunspecified (Agriculture) deals

:21: Total number of For wood and fibre (Forestry) deals
:37: Total hectares in For wood and fibre (Forestry) deals

:22: Total number of For carbon sequestration/REDD (Forestry) deals
:38: Total hectares in For carbon sequestration/REDD (Forestry) deals

:23: Total number of Forestunspecified (Forestry) deals
:39: Total hectares in Forestunspecified (Forestry) deals

:23: Total number of Forestunspecified (Forestry) deals
:39: Total hectares in Forestunspecified (Forestry) deals

