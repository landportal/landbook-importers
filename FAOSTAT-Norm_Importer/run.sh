./clean.sh # this scripts include to remove all .xml files

python main.py -c config/configuration-land.ini #generate the intermediate XML
mv FAO-LU_1_0.xml FAO-Land.xml
python main.py -c config/configuration-LU-forestry.ini #generate the intermediate XML
mv FAO-LU_1_0.xml FAO-LU-forestry.xml
python main.py -c config/configuration-LU-water.ini #generate the intermediate XML
mv FAO-LU_1_0.xml FAO-LU-water.xml
python main.py -c config/configuration-LU-irrigation.ini #generate the intermediate XML
mv FAO-LU_1_0.xml FAO-LU-irrigation.xml
python main.py -c config/configuration-LU-agripractices.ini #generate the intermediate XML
mv FAO-LU_1_0.xml FAO-LU-agripractices.xml
python main.py -c config/configuration-LU-aquaculture.ini #generate the intermediate XML
mv FAO-LU_1_0.xml FAO-LU-aquaculture.xml

#python main.py -c config/configuration-ASTI_Researchers.ini #generate the intermediate XML
#mv FAO-ASTI_1_0.xml FAO-ASTI-Researchers.xml
#python main.py -c config/configuration-ASTI_Research_Spending.ini #generate the intermediate XML
#mv FAO-ASTI_1_0.xml FAO-ASTI-Research_Spending.xml
#python main.py -c config/configuration-Food_security.ini #generate the intermediate XML
#mv FAO-FS_1_0.xml FAO-FS-Food_security.xml

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

