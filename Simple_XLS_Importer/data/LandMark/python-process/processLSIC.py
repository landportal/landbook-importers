#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import time
import math
import datetime

def getComment(justification, lawsProvisions):
    comment = ""
    #filter out value NaN = float:
    if isinstance(justification, unicode) and justification!="<Null>":
        comment+=justification
    if isinstance(lawsProvisions, unicode) and lawsProvisions!="<Null>" and lawsProvisions!="Not applicable":
        comment+="\n"+lawsProvisions
    return comment

input_filename = "LegalSecurityIndicators_2018_04_09.xls"
# save to file
timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-LMM-LSIC.xlsx"

xls = pd.ExcelFile(input_filename)

sheetCommunity = xls.parse(sheet_name="Community", header=0, keep_default_na=False, na_values=["N/A"])
#head = sheetCommunity.head(0)

sheetIndigenousPeople = xls.parse(sheet_name="IP", header=0, keep_default_na=False, na_values=["N/A"])

# add headers
df = pd.DataFrame(columns=["indicator", "country", "year", "value", "comment"])

for i in sheetCommunity.index:
    country = sheetCommunity['ISO_Code'][i]
    for x in range(1,11,1):
        indicator = "LSIC-"+str(x)+"CL"
        labelValue="I"+str(x)+"_Scr"
        labelYear="I"+str(x)+"_Year"
        labelJustification="I"+str(x)+"_Com"
        labelLawsProvisions="I"+str(x)+"_LaP"
        labelAddtionalNotes="I"+str(x)+"_AddInfo"
        value = sheetCommunity[labelValue][i]
        year = sheetCommunity[labelYear][i]
        justification = sheetCommunity[labelJustification][i]
        lawsProvisions = sheetCommunity[labelLawsProvisions][i]
        addtionalNotes = sheetCommunity[labelAddtionalNotes][i]

        comment = getComment(justification,lawsProvisions)
        
        # IMPORTANT: Read NA Values http://pandas.pydata.org/pandas-docs/stable/io.html#na-values
        if isinstance(value, unicode):
            if value and value!="<Null>":
                # Create a Pandas dataframe from some data.
                if math.isnan(year):
                    pass
                else:
                    year = int(year)
                df = df.append({"indicator":indicator, "country":country, "year":year, "value":value, "comment":comment},ignore_index=True)
            else:
                pass # unicode + value == null
        else:
            df = df.append({"indicator":indicator, "country":country, "year":year, "value":"N/A", "comment":comment},ignore_index=True)

    value = sheetCommunity["Avg_Scr"][i]
    year = sheetCommunity["Upl_Date"][i]
    if isinstance(year, datetime.datetime):
        year = year.year
    #filter out value NaN = float:
    if isinstance(value, unicode) and value and value!="<Null>":
        df = df.append({"indicator":"LSIC-11AVCL", "country":country, "year":year, "value":value},ignore_index=True)
    elif isinstance(value, float) and math.isnan(value):
        df = df.append({"indicator":"LSIC-11AVCL", "country":country, "year":year, "value":"N/A"},ignore_index=True)




###############################################################################

for i in sheetIndigenousPeople.index:
    country = sheetIndigenousPeople['ISO_Code'][i]
    for x in range(1,11,1):
        indicator = "LSIC-"+str(x)+"IP"
        labelValue="I"+str(x)+"_Scr"
        labelYear="I"+str(x)+"_Year"
        labelJustification="I"+str(x)+"_Com"
        labelLawsProvisions="I"+str(x)+"_LaP"
        labelAddtionalNotes="I"+str(x)+"_AddInfo"
        value = sheetIndigenousPeople[labelValue][i]
        year = sheetIndigenousPeople[labelYear][i]
        justification = sheetIndigenousPeople[labelJustification][i]
        lawsProvisions = sheetIndigenousPeople[labelLawsProvisions][i]
        addtionalNotes = sheetIndigenousPeople[labelAddtionalNotes][i]

        comment = getComment(justification,lawsProvisions)

        #filter out value NaN = float:
        if isinstance(value, unicode):
            if value and value!="<Null>":
                # Create a Pandas dataframe from some data.
                if math.isnan(year):
                    pass
                else:
                    year = int(year)
                df = df.append({"indicator":indicator, "country":country, "year":year, "value":value, "comment":comment},ignore_index=True)
            else:
                pass # unicode + value == null
        else:
            df = df.append({"indicator":indicator, "country":country, "year":year, "value":"N/A", "comment":comment},ignore_index=True)
                

    value = sheetIndigenousPeople["Avg_Scr"][i]
    year = sheetIndigenousPeople["Upl_Date"][i]
    if isinstance(year, datetime.datetime):
        year = year.year
    # all values have the same type: numpy.float64
    # filter out value NaN
    if isinstance(value, unicode) and value and value!="<Null>":
        df = df.append({"indicator":"LSIC-11AVIP", "country":country, "year":year, "value":value},ignore_index=True)
    elif isinstance(value, float) and math.isnan(value):
        df = df.append({"indicator":"LSIC-11AVIP", "country":country, "year":year, "value":"N/A"},ignore_index=True)


###############################################################################
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(filename_output, engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='data', index=False)

metadata = pd.DataFrame([["org_acronym", "LMM"], ["dataset_internal_id", "LSIC"], ["indicator_internal_id", "not-used"], ["read_as", "indicator_country_year_value"]])

# Convert the dataframe to an XlsxWriter Excel object.
metadata.to_excel(writer, sheet_name='metadata', index=False, header=False)


# Close the Pandas Excel writer and output the Excel file.
writer.save()

