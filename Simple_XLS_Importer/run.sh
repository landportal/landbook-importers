./clean.sh # this scripts include to remove all .xml files

#############################
# GENERATE intermediate XML #
#############################


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

for file_path in data/IFPRI-GHI/IFPRI-GHI*.xlsx
do
  python main.py -i $file_path #generate the intermediate XML

  # obtain the filename and the extension
  file=${file_path#data/IFPRI-GHI/*}
  file_name="${file%.*}"
  file_extension="${file##*.}"

  mv IFPRI-GHI_1_0.xml $file_name.xml
done


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

