import datetime
import json

from tests.utils import onto
from text2term import onto_utils
from text2term.term_collector import OntologyTermCollector
from text2term.tfidf_mapper import TFIDFMapper

source_terms = "/Users/rsgoncalves/Documents/Workspace/text2term/test/term-list-test.txt"
source_terms_23 = "/Users/rsgoncalves/Documents/Harvard/23andme/unstruct_phenotypes_sep24.txt"
source_terms_panukbb = "/Users/rsgoncalves/Documents/Harvard/23andme/panukbb/panukbb_traits.txt"
source_terms_opengwas = "/Users/rsgoncalves/Documents/Harvard/gwaslake/mappings/mapping-unmapped-traits-again/unmapped-traits-vs-manual-cleaned.txt"
target_ontology = onto.TEST

# desc = "opengwas-unmapped"
desc = "test-manually-after-input-cleaning-whitelist-v3"

timestamp = datetime.datetime.now().strftime("%d-%m-%YT%H-%M-%S")
output_file_name = "t2t-out-" + desc + "-" + timestamp + ".csv"

efo_base_iri = "http://www.ebi.ac.uk/efo/"
# uberon_base_iri = "http://purl.obolibrary.org/obo/UBERON"
mondo_base_iri = "http://purl.obolibrary.org/obo/MONDO"
hp_base_iri = "http://purl.obolibrary.org/obo/HP"
ncit_base_iri = "http://purl.obolibrary.org/obo/NCIT"
ordo = "http://www.orpha.net/ORDO/Orphanet"
pato_iri = "http://purl.obolibrary.org/obo/PATO"
go_iri = "http://purl.obolibrary.org/obo/GO"

iri_white_list = (efo_base_iri, mondo_base_iri, hp_base_iri, ncit_base_iri, ordo, pato_iri, go_iri)

onto_terms = OntologyTermCollector(target_ontology).get_ontology_terms(use_reasoning=True)
mapper = TFIDFMapper(onto_terms)
mappings_df, term_graphs = mapper.map(onto_utils.parse_list_file(source_terms), min_score=0.2)
# mappings_df = mapper.map(["Drive faster than motorway speed limit"], min_score=0)
# print(mappings_df)
mappings_df.to_csv(output_file_name, index=False)

with open(output_file_name + "-term-graphs.json", 'w') as json_file:
    json.dump(term_graphs, json_file, indent=2)
    # for graph in term_graphs:
    #     json_file.write(graph + "\n")
