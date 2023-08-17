from tests.utils import onto
from text2term.term_collector import OntologyTermCollector

target_ontology = onto.TEST

efo_base_iri = "http://www.ebi.ac.uk/efo/"
test_base_iri = "http://rsgoncalves.com/ontologies/onto"
chebi_base_iri = "http://purl.obolibrary.org/obo/CHEBI"
mesh_base_iri = "http://id.nlm.nih.gov/mesh/"

collector = OntologyTermCollector(target_ontology)
terms = collector.get_ontology_terms(use_reasoning=True, include_individuals=True)
