FAOSTAT Norm data Importer
================================
The way in which importer works is:

* It downloads a huge CSV file containing all the info available of FAO STAT database related
* It converts each line of the csv into an intermediate object that represents it (register).
* It filters this list of objects, removing all those that:

 - They contain data of indicators that had not been requested.
 - They refers to countries or regions that are not in the official list of countries.
 - They contain observations that has been already incorporated to the system (when the importer is not executing in historical mode).

* It turns that intermediate objects in objects of the common model.

It looks that the file that contains the entire database has a name that does not depend on dates, so it could be possible that in the next time that the importer need to execute the Download url may not change. If it does, the new URL must be specified in "zip_url", in the configuration.ini file. 

The importer expects an URL pointing to a zip that contains a single CSV file.

You may notice that the log of this importers produces many warnings. 
In general, it is not something to worry about: it is the normal behavior of the importer.
The algorithm downloads the entire database of FAO STAT and filters not neeeded data. 
In that process, many observations referred to unsupported regions are detected as "unknown countries" and registered in the log as it. 
But that observations should not be present in the final system.


INDICATORS SUPPORTED
====================

configuration-ASTI_Researchers
------------------------------

:Download URL: http://fenixservices.fao.org/faostat/static/bulkdownloads/ASTI_Researchers_E_All_Data_(Norm).zip
:Indicator ID pattern: FAO-{ITEM_CODE}-{ELEMENT_CODE}

* Agricultural researchers (FTE) (Number)

  * FAOSTAT item_code = 23046
  * FAOSTAT element_code = 6085

* Agricultural researchers (FTE)(Per 100,000 farmers)

  * FAOSTAT item_code = 23046
  * FAOSTAT element_code = 6086

  
configuration-ASTI_Research_Spending
------------------------------------

:Download URL: http://fenixservices.fao.org/faostat/static/bulkdownloads/ASTI_Research_Spending_E_All_Data_(Norm).zip
:Indicator ID pattern: FAO-{ITEM_CODE}-{ELEMENT_CODE}

* Agriculture research spending (2011 PPP$)

  * FAOSTAT item_code = 23045
  * FAOSTAT element_code = 6084

* Agriculture research spending (Share of Value Added (Agriculture, Forestry and Fishing))

  * FAOSTAT item_code = 23045
  * FAOSTAT element_code = 6083
  

configuration-Food_Security
---------------------------

:Download URL: http://fenixservices.fao.org/faostat/static/bulkdownloads/Food_Security_Data_E_All_Data_(Norm).zip
:Indicator ID pattern: FAO-{ITEM_CODE}-{ELEMENT_CODE}

* Domestic food price index (index)

  * FAOSTAT item_code = 21018
  * FAOSTAT element_code = 6125

* Prevalence of undernourishment (%) (3-year average)

  * FAOSTAT item_code = 21004
  * FAOSTAT element_code = 6121

* Share of food expenditure of the poor (%)

  * FAOSTAT item_code = 21022
  * FAOSTAT element_code = 6121

* Depth of the food deficit (kcal/capita/day) (3-year average)

  * FAOSTAT item_code = 21023
  * FAOSTAT element_code = 6128

* Access to improved water sources (%)

  * FAOSTAT item_code = 21019
  * FAOSTAT element_code = 6121

* Access to improved sanitation facilities (%)

  * FAOSTAT item_code = 21020
  * FAOSTAT element_code = 6121


configuration-Land
------------------

:Download URL: http://fenixservices.fao.org/faostat/static/bulkdownloads/Inputs_Land_E_All_Data_(Normalized).zip
:Indicator ID pattern: FAO-{ITEM_CODE}-{ELEMENT_CODE}

* Agricultural land

  * FAOSTAT item_code = 6610
  * FAOSTAT element_code = 5110

* Arable land

  * FAOSTAT item_code = 6621
  * FAOSTAT element_code = 5110

* Forest land

  * FAOSTAT item_code = 6661
  * FAOSTAT element_code = 5110

* Land areaLand area

  * FAOSTAT item_code = 6601
  * FAOSTAT element_code = 5110

* Relative agricultural land (FAO-X-6610-5110, from 6610-5110)

* Relative arable land (FAO-X-6621-5110, from 6621-5110)

* Relative forest land (FAO-X-6661-5110, from 6661-5110)

* Permanent crops

  * FAOSTAT item_code = 6650
  * FAOSTAT element_code = 5110

* Permanent meadows and pastures

  * FAOSTAT item_code = 6655
  * FAOSTAT element_code = 5110

* Agricultural area organic, total

  * FAOSTAT item_code = 6671
  * FAOSTAT element_code = 5110
