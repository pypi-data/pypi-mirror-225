import t2t

# t2t.cache_ontology_set("/Users/rsgoncalves/Documents/Workspace/text2term/text2term/resources/ontologies.csv")

# Cache a single ontology
# if not t2t.cache_exists("CL2"):
    # t2t.cache_ontology("http://purl.obolibrary.org/obo/cl/releases/2022-09-15/cl.owl", "CL")
# t2t.cache_ontology("/Users/rsgoncalves/Documents/Ontologies/snomedct_owl.owl", "SNOMED")
# t2t.cache_ontology("http://purl.obolibrary.org/obo/hp/releases/2022-06-11/hp.owl", "HPO")
# t2t.cache_ontology("http://purl.obolibrary.org/obo/ecto/releases/2022-12-12/ecto.owl", "ECTO")

# TODO error is due to owl:imports — some FOODON terms are related to imported terms,
#  which are not being collected by term_collector
t2t.cache_ontology("https://raw.githubusercontent.com/FoodOntology/foodon/v0.5.1/foodon.owl", "FOODON")
                   # base_iris=("http://purl.obolibrary.org/obo/FOODON",))

# mappings = t2t.map_terms(source_terms=['basal', 'Club', 'Club (nasal)', 'Club (non-nasal)', 'Classical monocytes',
#                                        'smooth muscle', 'Tuft', 'Non-classical monocytes', 'fibroblasts',
#                                        'fibroblast lineage', 'Mast cells', 'Myofibroblasts'],
#                          target_ontology="http://purl.obolibrary.org/obo/cl/releases/2022-09-15/cl.owl",
#                          max_mappings=3,
#                          base_iris=("http://purl.obolibrary.org/obo/CL",)
#                          )
#
# print(mappings.to_string())
#
# target_ontology="CL2",
# # save_graphs=False,
# use_cache = True,


# Cache all ontologies in a CSV file
# t2t.cache_ontology_set(ontology_registry_path="/Users/rsgoncalves/Documents/Workspace/text2term/text2term/resources/ontologies.csv")

# t2t.clear_cache()


#
# print(len(owlready2.default_world.ontologies))

# mappings = t2t._do_mapping(['heart attack', 'alzeimers'],
#                            ['t1', 't2'],
#                            terms,
#                            Mapper.TFIDF,
#                            max_mappings=3,
#                            min_score=0.2)
# print(mappings)

