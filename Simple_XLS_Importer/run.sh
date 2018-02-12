./clean.sh # this scripts include to remove all .xml files

#############################
# GENERATE intermediate XML #
#############################


#############################################
# SEDAC - Anthropogenic Biomes of the World #
#############################################

python main.py -i data/SEDAC-ABW/SEDAC-ABW.xlsx #generate the intermediate XML
mv SEDAC-ABW_1_0.xml SEDAC-ABW.xml


####################################
# TI - Global Corruption Barometer #
####################################

python main.py -i data/TI-GCB/TI-GCB.xlsx #generate the intermediate XML
mv TI-GCB.xml TI-GCB.xml


#################################################
# OKI - Global Open Data Index - Land Ownership #
#################################################

python main.py -i data/OKI-GODI/2016-OKI-GODI.xlsx #generate the intermediate XML
mv OKI-GODI_1_0.xml OKI-GODI.xml


############
# PRINDEX  #
############

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
mv NKT-VGGT16_1_0.xml NKT-VGGT16.1.xml

python main.py -i data/NKT-VGGT16/2017-NKT-VGGT-16.3.xlsx #generate the intermediate XML
mv NKT-VGGT16_1_0.xml NKT-VGGT16.3.xml

python main.py -i data/NKT-VGGT16/2017-NKT-VGGT-16.8-16.9.xlsx #generate the intermediate XML
mv NKT-VGGT16_1_0.xml NKT-VGGT16.8-16.9.xml


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

###############################
# IFPRI - Global Hunger Index #
###############################

python main.py -i data/IFPRI-GHI/2016-IFPRI-GHI.xlsx
mv IFPRI-GHI_1_0.xml 2016-IFPRI-GHI.xml

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

