#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import time

def getCleanValue(valueInitial):
    if isinstance(valueInitial, float) or isinstance(valueInitial, int):
        return unicode(valueInitial*100)
    else:
        return valueInitial.replace("%","").strip()

input_filename = "Pct_IP_CommunityLands_20170623.xls"
# save to file
timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-LMM-PICL.xlsx"

xls = pd.ExcelFile(input_filename)

sheetPct_IP_CommunityLands = xls.parse(sheet_name="Pct_IP_CommunityLands", header=0)
#head = sheetPct_IP_CommunityLands.head(0)

# add headers
df = pd.DataFrame(columns=["indicator", "country", "year", "value", "comment"])

year = "2017"

for i in sheetPct_IP_CommunityLands.index:
    country = sheetPct_IP_CommunityLands['ISO_Code'][i]
    value1TOT = sheetPct_IP_CommunityLands["IC_T"][i] #PICL-1TOT
    value2FR = sheetPct_IP_CommunityLands["IC_F"][i] #PICL-2FR
    value3NFR = sheetPct_IP_CommunityLands["IC_NF"][i] #PICL-3NFR
    comment = sheetPct_IP_CommunityLands["IC_Notes"][i] #PICL-3NFR

    if not isinstance(comment, float):
        comment = comment.replace('<br>', '\n')

    if value1TOT not in ["No data"]:
        value1TOT= getCleanValue(value1TOT)
        df = df.append({"indicator":"PICL-1TOT", "country":country, "year":year, "value":value1TOT, "comment":comment},ignore_index=True)
    if value2FR not in ["No data"]:
        value2FR= getCleanValue(value2FR)
        df = df.append({"indicator":"PICL-2FR", "country":country, "year":year, "value":value2FR, "comment":comment},ignore_index=True)
    if value3NFR not in ["No data"]:
        value3NFR= getCleanValue(value3NFR)
        df = df.append({"indicator":"PICL-3NFR", "country":country, "year":year, "value":value3NFR, "comment":comment},ignore_index=True)


###############################################################################
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(filename_output, engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='data', index=False)

metadata = pd.DataFrame([["org_acronym", "LMM"], ["dataset_internal_id", "PICL"], ["indicator_internal_id", "not-used"], ["read_as", "indicator_country_year_value"]])

# Convert the dataframe to an XlsxWriter Excel object.
metadata.to_excel(writer, sheet_name='metadata', index=False, header=False)


# Close the Pandas Excel writer and output the Excel file.
writer.save()

