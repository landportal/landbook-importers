./clean.sh & python main.py
xmllint --format --output pretty.xml DATFAOSTAT0_1_0.xml
grep -n "<indicator id=" pretty.xml
xmllint --noout --schema ../ModelToXml/landportalDataset.xsd pretty.xml
