import re

from text2term import onto_utils

# string = "somethin like (this) or then [that]   but ALWAYS F#$K"
#
# string = re.sub(r"[\(\[].*?[\)\]]", "", string)
# string = onto_utils.normalize(string)
#
# print(string)

curie = onto_utils.curie_from_iri("http://purl.obolibrary.org/obo/CL_1001036")
print(curie)

curie2 = onto_utils.curie_from_iri("http://www.ebi.ac.uk/efo/EFO_0009661")
print(curie2)

curie3 = onto_utils.curie_from_iri("http://purl.obolibrary.org/obo/NCIT_C83527")
print(curie3)