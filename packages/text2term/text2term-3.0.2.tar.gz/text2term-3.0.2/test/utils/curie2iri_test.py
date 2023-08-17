import datetime
import sys

from text2term.term_tag2iri import TermTag2Iri

tag2iri = TermTag2Iri()
if len(sys.argv) > 1:
    input_tag_list_file = sys.argv[1]
    output_file = "tag2iri-" + datetime.datetime.now().strftime("%d-%m-%YT%H-%M-%S") + ".csv"
    output_df = tag2iri.get_iris_df_for_file(input_tag_list_file, resolve_iri=True)
    output_df.to_csv(output_file, index=False)
else:
    print("Provide input file with tags to convert to IRIs")
