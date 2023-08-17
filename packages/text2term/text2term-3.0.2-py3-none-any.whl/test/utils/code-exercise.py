from owlready2 import *

#
# def get_ancestors(onto, input_term):
#     # my_term = IRIS[input_term]
#
#     for child in input_term.INDIRECT_is_a:  # .subclasses():  # onto.get_children_of(input_term):
#         # if child is ThingClass:
#         try:
#             print(child.label)
#         except AttributeError:
#             print("no label")
#             # do nothing


# ontology_iri = "/Users/rsgoncalves/Documents/Harvard/hiring/coding-exercise/coding-exercise-ontology.owl"
ontology_iri = "/Users/rsgoncalves/Documents/Ontologies/hp.owl"
ontology = get_ontology(ontology_iri).load()

# Coding exercise 1 = intermediate
# for c in ontology.classes():
#     print(c.label)
#     print(c.definition)
#     for child in ontology.search(subclass_of=c):
#         if child is not c:
#             print("Child: " + str(child.label))
#
#     print()

hpo2icd = []
count = 0
for c in ontology.classes():
    try:
        for db_xref in c.hasDbXref:
            if "ICD-9" in db_xref:
                print(c.label)
                print(db_xref)
                count += 1
                # hpo2icd.append((c.iri, c.label, db_xref))
    except Exception:
        pass
print("Total mappings: " + str(count))  #len(hpo2icd)))
