import pandas as pd
from numpy import average, median


def compare_with_opengwas(tool_mappings_file, gold_standard_mappings_file):
    tool_mappings = pd.read_csv(tool_mappings_file)
    opengwas_mappings = pd.read_csv(gold_standard_mappings_file)
    correct_mapping_count = 0
    correct_mapping_scores = []
    for index, row in tool_mappings.iterrows():
        src_term = row['Source Term']
        tgt_term_id = row['Mapped Term IRI']
        mapping_score = round(row['Mapping Score'], 1)

        # get source and mapped term from gold standard mappings
        manual_mappings = opengwas_mappings[opengwas_mappings['trait'] == src_term]
        manual_mapping_id = manual_mappings['mapping_id'].values
        if len(manual_mapping_id) > 0:
            manual_mapping_id = manual_mapping_id[0]
            if tgt_term_id == manual_mapping_id:
                correct_mapping_count += 1
                correct_mapping_scores.append(mapping_score)

                # for debugging
                # manual_mapping = row['Mapped Term Label']
                # print("(" + str(mapping_score) + ") " + src_term + " -> " + manual_mapping)

    manual_mapping_count = opengwas_mappings.shape[0]
    percent = round((correct_mapping_count/manual_mapping_count)*100, 2)
    print()
    print("# correct mappings: " + str(correct_mapping_count) + " (" + str(percent) + "%)")
    print("Minimum score: " + str(min(correct_mapping_scores)))
    print("Average score: " + str(round(average(correct_mapping_scores), 1)))
    print("Median score: " + str(median(correct_mapping_scores)))


mappings_file = "/Users/rsgoncalves/Documents/Harvard/gwaslake/mappings/mapping-Jan-25-2022/traits-mapped-feb8-nochebi.csv"
gold_standard_file = "//tests/data/opengwas_manual.csv"

compare_with_opengwas(mappings_file, gold_standard_file)
