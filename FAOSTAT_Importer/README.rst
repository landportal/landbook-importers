FAOSTAT data Importer
================================

The way in which importer works is:

* It downloads a huge CSV file containing all the info available of FAO STAT database related
* It converts each line of the csv into an intermediate object that represents it (register).
* It filters this list of objects, removing all those that:

 - They contain data of indicators that had not been requested.
 - They refers to countries or regions that are not in the official list of countries.
 - They contain observations that has been already incorporated to the system (when the importer is not executing in historical mode).

* It turns that intermediate objects in objects of the common model.

It looks that the file that contains the entire database has a name that does not depend on dates, so it could be possible that in the next time that the importer need to execute the Download url may not change. If it does, the new URL must be specified in "zip_url", in the configuration-XXXX.ini file. 

The importer expects an URL pointing to a zip that contains a single CSV file.

You may notice that the log of this importers produces many warnings. 
In general, it is not something to worry about: it is the normal behavior of the importer.
The algorithm downloads the entire database of FAO STAT and filters not neeeded data. 
In that process, many observations referred to unsupported regions are detected as "unknown countries" and registered in the log as it. 
But that observations should not be present in the final system.

In order to generate the relatives indicators, the indicator FAO-6601-5110 (Land area) MUST be generated.

To select the indicators to generate, you need to:
* describe them in to the configuration-XXXX.ini
* add them into the section [INDICATORS], in the codes list
* add them in the "indicator_names.txt"
* add them in the \es\weso\faostat\translator\translator_const

The code of the relative indicators is generated adding a X to the original indicator

INDICATORS SUPPORTED
====================

configuration
-------------

:Download URL: http://faostat.fao.org/Portals/_Faostat/Downloads/zip_files/Resources_Land_E_All_Data.zip
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

* Relative agricultural land (from 6610-5110)

* Relative arable land (from 6621-5110)

* Relative forest land (from 6661-5110)

* Permanent crops

  * FAOSTAT item_code = 6650
  * FAOSTAT element_code = 5110

* Permanent meadows and pastures

  * FAOSTAT item_code = 6655
  * FAOSTAT element_code = 5110

* Agricultural area organic, total

  * FAOSTAT item_code = 6671
  * FAOSTAT element_code = 5110

  
configuration-water
-------------------

:Download URL: http://faostat3.fao.org/faostat-bulkdownloads/Environment_Water_E_All_Data.zip
:Indicator ID pattern: FAO-{ITEM_CODE}-{ELEMENT_CODE}

* Water withdrawal for agricultural use

  * FAOSTAT item_code = 6720
  * FAOSTAT element_code = 7222

