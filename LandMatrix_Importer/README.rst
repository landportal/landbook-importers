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

:N1: Total number of deals
:HA1: Total hectares in deals
	
:N2: Total number of Concluded deals
:HA2: Total hectares in Concluded deals
	
:N3: Total number of Intended deals
:HA3: Total hectares in Intended deals
	
:N4: Total number of Failed deals
:HA4: Total hectares of Failed deals
	
:N5: Total number of deals in Production
:HA5: Total hectares in deals in Production
	
:N6: Total number of Agriculture deals
:HA6: Total hectares in Agriculture deals
	
:N7: Total number of Conservation deals
:HA7: Total hectares in Conservation deals
	
:N8: Total number of Forestry deals
:HA8: Total hectares in Forestry deals
	
:N9: Total number of Industry deals
:HA9: Total hectares in Industry deals
	
:N10: Total number of Renewable Energy deals
:HA10: Total hectares in Renewable Energy deals
	
:N11: Total number of Tourism deals
:HA11: Total hectares in Tourism deals
	
:N12: Total number of deals of Other Topic
:HA12: Total hectares in deals of Other Topic
	
:N13: Total number of deals of Unknown Topic
:HA13: Total hectares in deals of Unknown Topic
	
:N14: Total number of biofuel (Agriculture) deals
:HA14: Total hectares in biofuel (Agriculture) deals
	
:N15: Total number of Food crops (Agriculture) deals
:HA15: Total hectares in Food crops (Agriculture) deals
	
:N16: Total number of Livestock (Agriculture) deals
:HA16: Total hectares in Livestock (Agriculture) deals
	
:N17: Total number of Non-food agricultural commodities (Agriculture) deals
:HA17: Total hectares in Non-food agricultural commodities (Agriculture) deals
	
:N18: Total number of Agriunspecified (Agriculture) deals
:HA18: Total hectares in Agriunspecified (Agriculture) deals
	
:N19: Total number of For wood and fibre (Forestry) deals
:HA19: Total hectares in For wood and fibre (Forestry) deals
	
:N20: Total number of For carbon sequestration/REDD (Forestry) deals
:HA20: Total hectares in For carbon sequestration/REDD (Forestry) deals
	
:N21: Total number of Forestunspecified (Forestry) deals
:HA21: Total hectares in Forestunspecified (Forestry) deals


