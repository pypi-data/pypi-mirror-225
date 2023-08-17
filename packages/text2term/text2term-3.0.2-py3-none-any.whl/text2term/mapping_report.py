from owlready2 import *
from text2term import onto_utils
import pandas as pd

__version__ = "0.2.0"


class MappingReportGenerator:

    def __init__(self):
        pass

    def get_mapping_counts(self, mappings_df, ontology_iri, ontology_name):
        print("Generating report for " + ontology_name + " mappings")
        print("...loading ontology " + ontology_iri + "...")
        ontology = get_ontology(ontology_iri).load()
        self.create_instances(ontology, ontology_name, mappings_df=mappings_df, use_reasoning=False)
        term_iri_column = "Mapped Term IRI"
        output = []
        for term in ontology.classes():
            if "BFO_" not in term.iri and "PATO_" not in term.iri:
                term_df = mappings_df[mappings_df[term_iri_column] == term.iri]
                direct_mappings = term_df.shape[0]
                instances = term.instances()
                local_instances = []
                for instance in instances:
                    if onto_utils.BASE_IRI in instance.iri:
                        local_instances.append(instance)
                inferred_mappings = len(local_instances)
                # mappings_df.loc[mappings_df[term_iri_column] == term.iri, 'Direct Mappings'] = direct_mappings
                # mappings_df.loc[mappings_df[term_iri_column] == term.iri, 'Inferred Mappings'] = inferred_mappings

                output.append((term.iri, direct_mappings, inferred_mappings))
        output_df = pd.DataFrame(data=output, columns=['IRI', 'Direct Mappings', 'Inferred Mappings'])
        return output_df

    def  create_instances(self, ontology, ontology_name, mappings_df, save_ontology=False, use_reasoning=False):
        print("...adding mappings to ontology...")
        with ontology:
            class table_id(Thing >> str):
                pass
            class resource_id(Thing >> str):
                pass
        for index, row in mappings_df.iterrows():
            # table_id = row['Table']
            # term_id = row['Variable']  # TODO: NHANES-specific
            term = row['Source Term']
            term_id = row['Source Term ID']
            class_iri = row['Mapped Term IRI']
            ontology_class = IRIS[class_iri]

            # term_iri = onto_utils.BASE_IRI + table_id + "_" + variable_id  # TODO: NHANES-specific
            term_iri = onto_utils.BASE_IRI + term_id
            if IRIS[term_iri] is not None:
                labels = IRIS[term_iri].label
                if term not in labels:
                    labels.append(term)
            else:
                try:
                    new_instance = ontology_class(label=term, iri=term_iri)  # create OWL instance to represent mapping
                    new_instance.resource_id.append(term_id)
                except TypeError as e:
                    print("term: " + str(term))
                    print("iri: " + str(term_iri))
                    print("onto class" + str(ontology_class))
                    print(e)
                # new_instance.table_id.append(table_id)  # TODO: NHANES-specific
        if save_ontology:
            ontology.save(ontology_name + "_mappings.owl")

        if use_reasoning:
            print("...reasoning over ontology...")
            owlready2.reasoning.JAVA_MEMORY = 20000
            with ontology:
                sync_reasoner()


if __name__ == "__main__":
    ontology_label = "EFO"
    ontology_file = "https://github.com/EBISPOT/efo/releases/download/v3.46.0/efo.owl"
    mappings_file = pd.read_csv("/Users/rsgoncalves/Documents/Harvard/Workspace/opengwas-search/resources/opengwas_efo_mappings.csv", skiprows=8)

    mappings_with_counts = MappingReportGenerator().get_mapping_counts(mappings_df=mappings_file,
                                                                       ontology_iri=ontology_file,
                                                                       ontology_name=ontology_label)
    mappings_with_counts["Ontology"] = ontology_label
    mappings_with_counts.to_csv("mappings_report_efo_opengwas_separate.csv", index=False)
