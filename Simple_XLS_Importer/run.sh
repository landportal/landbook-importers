./clean.sh # this scripts include to remove all .xml files

#############################
# GENERATE intermediate XML #
#############################


#############
# SDG 2.3.1 #
#############

python main.py -i data/UN-SDG_2.3.1/UN-SDG_2.3.1.xlsx #generate the intermediate XML
mv UN-SDG_2.3.1_1_0.xml  UN-SDG_2.3.1.xml


############################
# Bonn Challenge Barometer #
############################

python main.py -i data/IUCN-BCB/IUCN-BCB.xlsx #generate the intermediate XML
mv IUCN-BCB_1_0.xml IUCN-BCB.xml


#########################
# Afrobarometer Survery #
#########################

python main.py -i data/AFRB-SURV/AFRB-SURV.xlsx #generate the intermediate XML
mv AFRB-SURV_1_0.xml AFRB-SURV.xml


###################
# VGGT endorsment #
###################

python main.py -i data/LS-VGGT/LS-VGGT.xlsx #generate the intermediate XML
mv LS-VGGT_1_0.xml LS-VGGT.xml


###############
# SIGI (2019) #
###############

python main.py -i data/OECD-SIGI2019/OECD-SIGI2019.xlsx #generate the intermediate XML
mv OECD-SIGI2019_1_0.xml OECD-SIGI2019.xml

python main.py -i data/OECD-SIGI2019/OECD-SIGI2019-SALA.xlsx #generate the intermediate XML
mv OECD-SIGI2019_1_0.xml OECD-SIGI2019-SALA.xml


###################
# PRINDEX (2018) #
###################

python main.py -i data/PRINDEX-PRINDEX2018/PRINDEX-PRINDEX2018.xlsx #generate the intermediate XML
mv PRINDEX-PRINDEX2018_1_0.xml PRINDEX-PRINDEX2018.xml

###############################
# FAO - Legal Assessment tool #
###############################

python main.py -i data/FAO-LAT/FAO-LAT.xlsx #generate the intermediate XML
mv FAO-LAT_1_0.xml FAO-LAT.xml


#######################
# WB - Doing Business #
#######################

python main.py -i data/WB-DB/WB-DB.xlsx #generate the intermediate XML
mv WB-DB_1_0.xml WB-DB.xml


############################
# WF - Open Data Barometer #
############################

python main.py -i data/WF-ODB/WF-ODB.xlsx #generate the intermediate XML
mv WF-ODB_1_0.xml WF-ODB.xml


######################
# UNEP-WCMC Drylands #
######################

python main.py -i data/UNEP-WCMC-DRY/UNEP-WCMC-DRY.xlsx #generate the intermediate XML
mv UNEP-WCMC-DRY_1_0.xml UNEP-WCMC-DRY.xml


####################################
# NRGI - Resource Governance Index #
####################################

python main.py -i data/NRGI-RGI/NRGI-RGI.xlsx #generate the intermediate XML
mv NRGI-RGI_1_0.xml NRGI-RGI.xml


################################################################
# FAO/ILRI - Global Livestock Production Systems in Rangelands #
################################################################

python main.py -i data/FAO-GLPSR/FAO-GLPSR.xlsx #generate the intermediate XML
mv FAO-GLPSR_1_0.xml FAO-GLPSR.xml


#############################################
# SEDAC - Anthropogenic Biomes of the World #
#############################################

python main.py -i data/SEDAC-ABW/SEDAC-ABW.xlsx #generate the intermediate XML
mv SEDAC-ABW_1_0.xml SEDAC-ABW.xml


####################################
# TI - Global Corruption Barometer #
####################################

python main.py -i data/TI-GCB/TI-GCB.xlsx #generate the intermediate XML
mv TI-GCB_1_0.xml TI-GCB.xml


#################################################
# OKI - Global Open Data Index - Land Ownership #
#################################################

python main.py -i data/OKI-GODI/2016-OKI-GODI.xlsx #generate the intermediate XML
mv OKI-GODI_1_0.xml OKI-GODI.xml


###################
# PRINDEX (Pilot) #
###################

python main.py -i data/LA-PRI/LA-PRI.xlsx #generate the intermediate XML
mv LA-PRI_1_0.xml LA-PRI.xml


################################
# Land Conflict Watch (India)  #
################################

python main.py -i data/LCW-LCI/LCW-LCI.xlsx #generate the intermediate XML
mv LCW-LCI_1_0.xml LCW-LCI.xml


###############################
# Transparency International  #
###############################

python main.py -i data/TI-CPI/TI-CPI.xlsx #generate the intermediate XML
mv TI-CPI_1_0.xml TI-CPI.xml


############################
# Lao Agricultural Census  #
############################

python main.py -i data/LMAF-LAC/LMAF-LAC.xlsx #generate the intermediate XML
mv LMAF-LAC_1_0.xml LMAF-LAC.xml


#############
# LandMark  #
#############

python main.py -i data/LandMark/LMM-LSIC.xlsx #generate the intermediate XML
mv LMM-LSIC_1_0.xml LMM-LSIC.xml

python main.py -i data/LandMark/LMM-PICL.xlsx #generate the intermediate XML
mv LMM-PICL_1_0.xml LMM-PICL.xml


##################
# NKT VGGT 2016  #
##################

python main.py -i data/NKT-VGGT16/2016-NKT-VGGT-16.1.xlsx #generate the intermediate XML
mv NKT-VGGT16_1_0.xml 2016-NKT-VGGT16.1.xml

python main.py -i data/NKT-VGGT16/2017-NKT-VGGT-16.3.xlsx #generate the intermediate XML
mv NKT-VGGT16_1_0.xml NKT-VGGT16.3.xml

python main.py -i data/NKT-VGGT16/2017-NKT-VGGT-16.8-16.9.xlsx #generate the intermediate XML
mv NKT-VGGT16_1_0.xml NKT-VGGT16.8-16.9.xml

python main.py -i data/NKT-VGGT16/2018-NKT-VGGT-16.1.xlsx #generate the intermediate XML
mv NKT-VGGT16_1_0.xml 2018-NKT-VGGT16.1.xml

python main.py -i data/NKT-VGGT16/2018-NKT-VGGT-16.2-16.5.xlsx #generate the intermediate XML
mv NKT-VGGT16_1_0.xml NKT-VGGT16.2-16.5.xml


#################################
# UNDP Human Development Index  #
#################################

python main.py -i data/UNDP-HDI/HDI_for_Ingestion_reduced_consistent_FINAL_HDI_index.xls #generate the intermediate XML
mv UNDP-HDI_1_0.xml UNDP-HDI_index.xml
python main.py -i data/UNDP-HDI/HDI_for_Ingestion_reduced_consistent_FINAL_HDI_ranking.xls #generate the intermediate XML
mv UNDP-HDI_1_0.xml UNDP-HDI_ranking.xml


####################################
# Donor's Platform - Map of Donors #
####################################

for file_path in data/DP-MOD/Map_of_donors*.xlsx
do
  python main.py -i $file_path #generate the intermediate XML

  # obtain the filename and the extension
  file=${file_path#data/DP-MOD/*}
  file_name="${file%.*}"
  file_extension="${file##*.}"

  mv DP-MOD_1_0.xml $file_name.xml
done

python main.py -i data/DP-MOD/2018-DP-MOD.xlsx #generate the intermediate XML
mv DP-MOD_1_0.xml 2018-DP-MOD.xml

###############################
# IFPRI - Global Hunger Index #
###############################

python main.py -i data/IFPRI-GHI/2017-IFPRI-GHI.xlsx
mv IFPRI-GHI_1_0.xml 2017-IFPRI-GHI.xml

#####################
# FAO LAND & GENDER #
#####################

for file_path in data/FAO-LandAndGender/FAO-LandAndGender*.xlsx
do
#  file_path_escaped=$(printf '%q' "$file_path")
  python main.py -i $file_path #generate the intermediate XML

  # obtain the filename and the extension
  file=${file_path#data/FAO-LandAndGender/*}
  file_name="${file%.*}"
  file_extension="${file##*.}"

  mv FAO-LG_1_0.xml $file_name.xml
done


#############
# OECD SIGI #
#############

for file_path in data/OECD-SIGI/OECD-SIGI-*.xlsx
do
  python main.py -i $file_path #generate the intermediate XML

  # obtain the filename and the extension
  file=${file_path#data/OECD-SIGI/*}
  file_name="${file%.*}"
  file_extension="${file##*.}"

  mv OECD-SIGI_1_0.xml $file_name.xml
done


###########
# WB LGAF #
###########

for file_path in data/WB-LGAF/WB-LGAF*.xlsx
do
  python main.py -i $file_path #generate the intermediate XML

  # obtain the filename and the extension
  file=${file_path#data/WB-LGAF/*}
  file_name="${file%.*}"
  file_extension="${file##*.}"

  mv ${file_name}_1_0.xml $file_name.xml
done


###########
# RRI FTD #
###########

for file_path in data/RRI-FTD/RRI-FTD*.xlsx
do
  python main.py -i $file_path #generate the intermediate XML

  # obtain the filename and the extension
  file=${file_path#data/RRI-FTD/*}
  file_name="${file%.*}"
  file_extension="${file##*.}"

  mv ${file_name}_1_0.xml $file_name.xml
done

###################################################################
###################################################################
###################################################################

################
# GENERATE RDF #
################

for file in *.xml
do
  # obtain the filename and the extension
  file_name="${file%.*}"
  file_extension="${file##*.}"

  # pretty print the intermediate XML
  xmllint --format --output $file $file

  # check the indicators added
  grep -n "<indicator id=" $file

  # validate the intermediate XML against the XML Schema
  xmllint --noout --schema ../ModelToXml/landportalDataset.xsd $file

  # generate the RDF (in RDF/XML and Turtle)
  python ../../landbook-receiver/rdf-generator.py  -i $file -o $file_name
done

