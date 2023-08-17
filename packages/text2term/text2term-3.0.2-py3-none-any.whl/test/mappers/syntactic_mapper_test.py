import datetime

from tests.utils import onto
from text2term.syntactic_mapper import SyntacticMapper
from text2term.similarity_metric import SimilarityMetric
from text2term.term_collector import OntologyTermCollector

source_terms_1 = ["Dog", "Catto", "Elfo", "Elofant"]
source_terms_2 = ["Endometrial cancer",  "Drug eruption",  "Gastric cancer",  "Graves' disease",
                  "Esophageal cancer",  "Type 2 diabetes"]
term_collector = OntologyTermCollector(onto.TEST)
onto_terms = term_collector.get_ontology_terms()

mapper = SyntacticMapper(onto_terms)
mappings_df = mapper.map(source_terms_1, similarity_metric=SimilarityMetric.FUZZY_WEIGHTED, max_mappings=3)

print(mappings_df)

timestamp = datetime.datetime.now().strftime("%d-%m-%YT%H-%M-%S")
output_file_name = "t2t-out-" + timestamp + ".csv"
mappings_df.to_csv(output_file_name, index=False)
