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

python main.py -i data/DP-MOD/Map_of_donors_Concluded_Final_number.xlsx #generate the intermediate XML
mv DP-MOD_1_0.xml map-of-donors-concluded-number.xml
python main.py -i data/DP-MOD/Map_of_donors_Concluded_Final_funding.xlsx #generate the intermediate XML
mv DP-MOD_1_0.xml map-of-donors-concluded-funding.xml

python main.py -i data/DP-MOD/Map_of_donors_Ongoing_Final_number.xlsx #generate the intermediate XML
mv DP-MOD_1_0.xml map-of-donors-ongoing-number.xml
python main.py -i data/DP-MOD/Map_of_donors_Ongoing_Final_funding.xlsx #generate the intermediate XML
mv DP-MOD_1_0.xml map-of-donors-ongoing-funding.xml

###############################
# IFPRI - Global Hunger Index #
###############################

python main.py -i data/IFPRI-GHI/IFPRI-GHI-Child_Mortality.xlsx #generate the intermediate XML
mv IFPRI-DAT-0_1_0.xml IFPRI-GHI-Child_Mortality.xml

python main.py -i data/IFPRI-GHI/IFPRI-GHI-Child_Stunting.xlsx #generate the intermediate XML
mv IFPRI-DAT-0_1_0.xml IFPRI-GHI-Child_Stunting.xml

python main.py -i data/IFPRI-GHI/IFPRI-GHI-Child_Wasting.xlsx #generate the intermediate XML
mv IFPRI-DAT-0_1_0.xml IFPRI-GHI-Child_Wasting.xml

python main.py -i data/IFPRI-GHI/IFPRI-GHI.xlsx #generate the intermediate XML
mv IFPRI-DAT-0_1_0.xml IFPRI-GHI.xml

python main.py -i data/IFPRI-GHI/IFPRI-GHI-Undernourishment.xlsx #generate the intermediate XML
mv IFPRI-DAT-0_1_0.xml IFPRI-GHI-Undernourishment.xml


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

  mv FAO-LANDANDGENDER_1_0.xml $file_name.xml
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

