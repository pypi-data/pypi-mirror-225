import pandas as pd

# source = "/Users/rsgoncalves/Documents/Workspace/text2term/test/t2t-out-test-manually-after-input-cleaning-whitelist-v3-07-12-2021T19-28-52.csv"
from text2term import onto_utils

source = "/Users/rsgoncalves/Documents/Harvard/gwaslake/mappings/mapping-Jan-25-2022/traits-mapped-feb8-nochebi.csv"

output_writer = open(source + "-converted.csv", "w")

csv = pd.read_csv(source)

last_input_string = ""
for index, row in csv.iterrows():
    # print(row['Source Term'])
    if row['Source Term'] == last_input_string:
        output_writer.write("\"" + row['Mapped Term Label'] + "\"," + row['Mapped Term IRI'] + "," +
                            row['Mapped Ontology IRI'] + "," + str(row['Mapping Score']) + ",")
    else:
        output_writer.write("\n")
        # src_term = row['Source Term']
        src_term = onto_utils.remove_quotes(row['Source Term'])
        output_writer.write('\"' + src_term + '\",\"' + row['Mapped Term Label'] + '\",' + row['Mapped Term IRI'] +
                            ',' + row['Mapped Ontology IRI'] + ',' + str(row['Mapping Score']) + ',')
    last_input_string = row['Source Term']

