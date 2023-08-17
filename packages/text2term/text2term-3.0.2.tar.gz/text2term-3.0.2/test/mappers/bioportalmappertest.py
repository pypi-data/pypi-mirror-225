import sys
from text2term.bioportal_mapper import BioPortalAnnotatorMapper
from text2term.onto_utils import BioPortalOntologyName

# input_file = ontoutils.parse_list_file(sys.argv[1])  # a list of terms, one term per line
# output_file = sys.argv[2]  # the output file where the details of ontology term mappings
# bioportal_apikey = sys.argv[3]  # BioPortal API key
bioportal_apikey = "b0363744-e6d9-4cd5-a7a8-f3a118ee3049"

onto = BioPortalOntologyName.ALL.value
ontos = BioPortalOntologyName.DOID.value + "," + BioPortalOntologyName.MONDO.value

if len(sys.argv) > 4:
    onto = sys.argv[4]  # comma-separated list of ontologies

annotator = BioPortalAnnotatorMapper(bioportal_apikey)
source_terms = ["Heart Attack", "Cardiac arrest"]
ms = annotator.map(source_terms, ontos, max_mappings=3)
print(ms)
# for m in ms.iterrows():
#     print(m)
