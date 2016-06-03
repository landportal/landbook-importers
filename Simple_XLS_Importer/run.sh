./clean.sh # this scripts include to remove all .xml files

python main.py -i data/HDI_for_Ingestion_reduced_consistent_FINAL_HDI_index.xls #generate the intermediate XML
mv UNDP-HDI_1_0.xml UNDP-HDI_index.xml
python main.py -i data/HDI_for_Ingestion_reduced_consistent_FINAL_HDI_ranking.xls #generate the intermediate XML
mv UNDP-HDI_1_0.xml UNDP-HDI_ranking.xml

python main.py -i data/Map_of_donors_Concluded_Final_number.xlsx #generate the intermediate XML
#mv DP-MOD-1_1_0.xml map-of-donors-concluded-number.xml
python main.py -i data/Map_of_donors_Concluded_Final_funding.xlsx #generate the intermediate XML
#mv DP-MOD-1_1_0.xml map-of-donors-concluded-funding.xml

python main.py -i data/Map_of_donors_Ongoing_Final_number.xlsx #generate the intermediate XML
#mv DP-MOD-1_1_0.xml map-of-donors-ongoing-number.xml
python main.py -i data/Map_of_donors_Ongoing_Final_funding.xlsx #generate the intermediate XML
#mv DP-MOD-1_1_0.xml map-of-donors-ongoing-funding.xml



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

