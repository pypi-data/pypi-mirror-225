import pandas as pd
import t2t

MAX_MAPPINGS = 1
MIN_SCORE = 0.35
EXCLUDE_DEPRECATED = True
SAVE_MAPPINGS = True
MAPPINGS_OUTPUT_FOLDER = "nhanes/"
NHANES_TABLE = "/Users/rsgoncalves/Documents/Harvard/Workspace/NHANES-variable-metadata/metadata/nhanes_variables.csv"
NHANES_TABLE_COLUMNS = ("SAS Label", "Variable Name")


def map_to_ontology(ontology_name, base_iris=()):
    mappings_df = t2t.map_file(
        input_file=NHANES_TABLE,
        target_ontology=ontology_name,
        output_file=get_output_file_name(ontology_name),
        csv_columns=NHANES_TABLE_COLUMNS,
        max_mappings=MAX_MAPPINGS,
        min_score=MIN_SCORE,
        base_iris=base_iris,
        excl_deprecated=EXCLUDE_DEPRECATED,
        save_mappings=SAVE_MAPPINGS,
        use_cache=True
    )
    return add_ontology_source(mappings_df, ontology_name)


def map_to_hpo():
    return map_to_ontology('HPO', base_iris=("http://purl.obolibrary.org/obo/HP",))


def map_to_efo():
    return map_to_ontology('EFO', base_iris=("http://www.ebi.ac.uk/efo/EFO",))


def map_to_mondo():
    return map_to_ontology("MONDO", base_iris=("http://purl.obolibrary.org/obo/MONDO",))


def map_to_uberon():
    return map_to_ontology("UBERON", base_iris=("http://purl.obolibrary.org/obo/UBERON",))


def map_to_nci_thesaurus():
    return map_to_ontology("NCIT")


def map_to_ecto():
    return map_to_ontology("ECTO", base_iris=("http://purl.obolibrary.org/obo/ECTO",))


def map_to_uo():
    return map_to_ontology("UO", base_iris=("http://purl.obolibrary.org/obo/UO",))


# TODO map to more recent version of SNOMED — conversion script is failing for 2022 releases
def map_to_snomed():
    return map_to_ontology("SNOMED")


def map_to_chebi():
    # TODO implement
    pass


def map_to_foodon():
    # TODO implement
    pass


def get_output_file_name(ontology_name):
    return MAPPINGS_OUTPUT_FOLDER + "mappings_" + ontology_name + ".csv"


def add_ontology_source(data_frame, ontology_name):
    data_frame["Ontology"] = ontology_name
    return data_frame


def get_best_mappings(mappings_df):
    nhanes_table = pd.read_csv(NHANES_TABLE)
    all_best_mappings = pd.DataFrame()
    for index, row in nhanes_table.iterrows():
        variable_label = row['SAS Label']
        mappings = mappings_df[mappings_df['Source Term'] == variable_label]
        best_mapping = mappings[mappings['Mapping Score'] == mappings['Mapping Score'].max()]
        # best_mapping = best_mapping.drop_duplicates()
        all_best_mappings = pd.concat([all_best_mappings, best_mapping])
    all_best_mappings.to_csv(get_output_file_name("BEST"), index=False)


def map_to_ontologies():
    efo_mappings = map_to_efo()
    hpo_mappings = map_to_hpo()
    mondo_mappings = map_to_mondo()
    uberon_mappings = map_to_uberon()
    ncit_mappings = map_to_nci_thesaurus()
    snomed_mappings = map_to_snomed()
    uo_mappings = map_to_uo()

    # ecto_mappings = map_to_ecto()
    """
    throws TypeError: 'http://purl.obolibrary.org/obo/RO_0000052' belongs to more than one entity types
    (cannot be both a property and a class/an individual)!
    GitHub ticket: https://github.com/EnvironmentOntology/environmental-exposure-ontology/issues/244
    """

    all_mappings = pd.concat([efo_mappings, hpo_mappings, mondo_mappings, uberon_mappings, snomed_mappings,
                              ncit_mappings, uo_mappings], axis=0)
    all_mappings.drop_duplicates()
    all_mappings.to_csv(get_output_file_name("ALL"), index=False)
    get_best_mappings(all_mappings)


if __name__ == "__main__":
    # t2t.cache_ontology_set("/Users/rsgoncalves/Documents/Workspace/text2term/text2term/resources/ontologies.csv")
    map_to_ontologies()
