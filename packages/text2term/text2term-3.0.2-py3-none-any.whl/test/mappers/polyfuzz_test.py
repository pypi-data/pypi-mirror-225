from polyfuzz import PolyFuzz
from polyfuzz.models import Embeddings
from flair.embeddings import TransformerWordEmbeddings

from_list = ["apple", "apples", "appl", "recal", "house", "similarity"]
to_list = ["apple", "apples", "mouse"]

model = PolyFuzz("TF-IDF").match(from_list, to_list)

print(model.get_matches())

bert = TransformerWordEmbeddings('bert-base-multilingual-cased')
bert_matcher = Embeddings(bert, min_similarity=0)

bert_model = PolyFuzz(bert_matcher).match(from_list, to_list)

print(bert_model.get_matches())
