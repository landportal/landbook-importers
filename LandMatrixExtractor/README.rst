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
* Date (year YYYY)
* Indicator
* The composed value for country-date

It looks that the file that contains the entire database has a name that does not depend on dates, so it could be possible that in the next time that the importer need to execute the Download url may not change. If it does, the new URL must be specified in "url_download", in the configuration.ini file. 

This importer downloads the entire landmatrix database in XML format, but the observations have a complex nature, hard to fit in the general model. 
A node of information in the landmatrix does not refer to a concrete country, with a concrete indicator and a single value in a concrete date. 
The indicators built are aggregations of values, such as "total number of deals in some sector".

The python project of the importer includes a file "strategy.txt" where the indicators are detailed.


The date assigned to each observation is the highest date found when parsing a value that belongs to its aggregate. 
For this reason, when executing again the importer to incorporate new data, 
it may be something to consider removing from the system all the old observation 
and run the program in historical mode.

Date
^^^^

The importer is prepared to ignore data with a date lower than the value specified in the "first_valid_year" field 
(that can be manually set or automatically calculated by the importer) of the configuration.ini file. 
However, doing this, we will get observations of data aggregates between the specified date and the current one, 
meanwhile the old observations are aggregates of every available date. The meaning will not be consistent. 
By removing all the old observations we will obtain new ones that are aggregates of the old and the new values.
The date is obtained parsing the negotiation_status field.


INDICATORS SUPPORTED
====================

* FIXME
