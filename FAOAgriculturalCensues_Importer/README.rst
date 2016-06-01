FAO Agricultural Census Importer
================================
FAO organization has four different importers, depending on where we have find the data. This one in particular handles three different excel files, which represents the same indicators through time. Every excel file has a different format which made impossible the development of an homogeneous importer, driving to this situation:

In the configuration.ini file there are the next properties:
 - file_names: Points what files there have to been parser, separated by commas.
 - data_range_rows_file_name: Indicates the valid rows of the excel file separated by '-'.
 - data_range_cols_file_name: Indicated the valid cols of the excel file separated by '-'.
 
Those properties are needed because the excel files contain a lot of metadata, which is useless for the importer.

The excel reader, as many others importers, load a data matrix with the required cells of the file, making it easier to the importer to work with them.

Due to the differences between files, all of them has a customize method in which are specified the columns for every indicator, but at the end all this methods rely in a last one that is the same for every file.


INPUT DATA
==========

It uses previously downloaded files present at "data" folder.

The links to the original data are:

- Land tenure_1970.1980.1990.xlsx
http://www.fao.org/fileadmin/templates/ess/documents/world_census_of_agriculture/additional_international_comparison_tables/table3_tenuren.xls

- Land_tenure 2000.xls
http://www.fao.org/fileadmin/templates/ess/ess_test_folder/World_Census_Agriculture/WCA2000_data_comparison/Final_3.1_Land_tenure_types_number_and_area_of_holdings.xls

- Land_operated_by_tenure_type 2000.xls
http://www.fao.org/fileadmin/templates/ess/ess_test_folder/World_Census_Agriculture/WCA2000_data_comparison/Final_3.2_Land_operated_by_tenure_type.xls


And this data come from the International comparison tables from the World Programme for the Census of Agriculture [1].

Actually, it comes from the WCA 1990 round [2] and  the WCA 2000 round [3]

The data from WCA 2010 round [4] and WCA 2020 round [5] are not available on FAO website.

[1] http://www.fao.org/economic/ess/ess-wca/en/
[2] http://www.fao.org/economic/ess/ess-wca/wca-1990/ess-wca-tables/en/
[3] http://www.fao.org/economic/ess/ess-wca/wca-2000/ess-wca2000-tables/en/
[4] http://www.fao.org/economic/ess/ess-wca/wca-2010/en/
[5] http://www.fao.org/economic/ess/ess-wca/wca-2020/en/