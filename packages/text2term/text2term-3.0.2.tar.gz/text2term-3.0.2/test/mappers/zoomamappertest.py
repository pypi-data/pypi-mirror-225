from tests.data import ukb2efo_sample
from text2term.zooma_mapper import ZoomaMapper

source_terms = ["Heart Attack", "Cardiac arrest"]
# source_terms = ukb2efo_sample.results.keys()

mapper = ZoomaMapper()
ms = mapper.map(source_terms, "EFO,MONDO,DOID,HP", max_mappings=2, api_params={"mykey1": "myvalue1", "mykey2": "myvalue2"})

for m in ms.iterrows():
    print(m)
