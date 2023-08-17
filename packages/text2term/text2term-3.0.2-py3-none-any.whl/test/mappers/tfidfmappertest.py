import datetime

from tests.utils import onto
from text2term.term_collector import OntologyTermCollector
from tests.data import ukb2efo_sample
from text2term.tfidf_mapper import TFIDFMapper

source_terms = ukb2efo_sample.results.keys()
source_terms_2 = ["Endometrial cancer",  "Drug eruption",  "Gastric cancer",  "Graves' disease",
                  "Esophageal cancer",  "Type 2 diabetes"]
source_terms_3 = ["Doggo", "Doggy", "Elfo", "Elofant", "Cat lady"]

term_collector = OntologyTermCollector(onto.EFO_LOCAL)
onto_terms = term_collector.get_ontology_terms()

mapper = TFIDFMapper(onto_terms)
mappings_df = mapper.map(source_terms_2, max_mappings=5, min_score=0.3)
print(mappings_df)

timestamp = datetime.datetime.now().strftime("%d-%m-%YT%H-%M-%S")
output_file_name = "t2t-out-" + timestamp + ".csv"
mappings_df.to_csv(output_file_name, index=False)
