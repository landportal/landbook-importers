./clean.sh # this scripts include to remove all .xml files

python main.py -i data/example_c_y_v.xlsx #generate the intermediate XML
mv ORG-DAT-1_1_0.xml DAT-RAW-C_Y_V.xml
python main.py -i data/example_multiple_years.xlsx #generate the intermediate XML
mv ORG-DAT-1_1_0.xml DAT-RAW-MULTIPLE_YEARS.xml

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

