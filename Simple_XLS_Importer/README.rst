Simple XLS data Importer
=========================

Summary
^^^^^^^
An importer to generate intermediate XML from a simple Excel file (XLS) in a concrete shape.


Process
^^^^^^^
The way in which importer works is:

* It reads an input file (passed as argument in the command line) and generate an intermediate matrix. The shape of the input file is commented below
- python main.py -i data/example_c_y_v.xlsx
* It converts the intermediate matrix into an objects of the common model.
* It filters this list of objects, removing all those that:
 - Its value is blank or "-"
* It generates the intermediate XML from the objects of the common model

You may notice that the log of this importers produces warnings.


Shape of the XLS file
^^^^^^^^^^^^^^^^^^^^^
The file MUST contain 2 tabs: data and metadata.

In the metadata tab, it MUST be present, and in that order:
 - cell (0,0) the string "org_acronym"
 - cell (0,1) the value for org_acronym (for instance "FAO")
 - cell (1,0) the string "dataset_internal_id"
 - cell (1,1) the value for dataset_internal_id (for instance "DAT-1")
 - cell (2,0) the string "indicator_internal_id" 
 - cell (2,1) the value for indicator_internal_id" (for instance "IND-1")
 - cell (3,0) the string "read_as"
 - cell (3,1) the value for read_as. The possible values are: "country_multiple_values" and "country_year_value".

In the data tab, there are 2 cases: "country_multiple_values" and "country_year_value".

For "country_multiple_values", the shape is:
 - In the first row, the first cell is a unused title and the next cells are the years (or period of years)
 - In the second and next rows, the first cell is the name of the country in English (or, preferred its ISO3 code), 
   and the next cells are the values of the indicator for each year.

For "country_year_value", the shape is, for each row:
 - The first cell is the name of the country in English (or, preferred its ISO3 code)
 - The second cell is the year (a concrete year or a period of years)
 - The third cell is the value
