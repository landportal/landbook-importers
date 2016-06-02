./clean.sh # this scripts include to remove all .xml files

python main.py -c config/configuration.ini #generate the intermediate XML
mv FAO-0_1_0.xml DAT-FAO.xml
python main.py -c config/configuration-water.ini #generate the intermediate XML
mv FAO-0_1_0.xml DAT-FAO-water.xml

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

