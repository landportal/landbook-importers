./clean.sh # this scripts include to remove all .xml files

python main.py -c config/configuration-WB-DEM.ini #generate the intermediate XML
python main.py -c config/configuration-WB-HN.ini #generate the intermediate XML
python main.py -c config/configuration-WB-RD.ini #generate the intermediate XML
python main.py -c config/configuration-WB-SE.ini #generate the intermediate XML
python main.py -c config/configuration-WB-WGI.ini #generate the intermediate XML

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

