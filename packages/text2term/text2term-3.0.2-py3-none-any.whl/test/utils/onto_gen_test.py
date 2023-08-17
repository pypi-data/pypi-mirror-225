from text2term import onto_utils

strings = ["John", "Jane", "Pluto", "Mickey"]

ontology = onto_utils.get_ontology_from_labels(strings)

ontology.save(file="/test/auto-gen-onto-test.owl")
