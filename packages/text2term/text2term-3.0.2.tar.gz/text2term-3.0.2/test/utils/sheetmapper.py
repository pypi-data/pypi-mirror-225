import numpy as np
import pandas as pd

input_spreadsheet = "/Users/rsgoncalves/Documents/Harvard/23andme/OpenGWAS-Phenotype-Mappings-v2.xlsx"

opengwas_sheet = pd.read_excel(input_spreadsheet, sheet_name=0)
panukbb_sheet = pd.read_excel(input_spreadsheet, sheet_name=2)

unmatched = []
mappings = []
for index, row in opengwas_sheet.iterrows():
    ogwas_id = row['GWAS Identifier']
    if "ukb-e" in str(ogwas_id):  # Only look at PanUK Biobank traits (listed in OpenGWAS spreadsheet)
        trait = row['Trait']
        match_row = panukbb_sheet.loc[panukbb_sheet['description'] == trait]
        if not match_row.empty:
            trait_description = match_row['description'].values[0]
            phenocode = match_row['phenocode'].values[0]
            trait_type = match_row['trait_type'].values[0]
            coding_description = match_row['coding_description'].values[0]
            description_more = match_row['description_more'].values[0]
            mappings.append((ogwas_id, trait, description_more, coding_description, phenocode, trait_type))
        else:
            unmatched.append(trait)

print("Mapped traits:", str(len(mappings)))
print("Unmatched traits in source spreadsheet: " + str(len(unmatched)))

col_names = ['opengwas_id', 'opengwas_panukbb_description', 'panukbb_description_more', 'panukbb_coding_description',
             'phenocode', 'panukbb_trait_type']
out_df = pd.DataFrame(mappings, columns=col_names)
out_df.to_csv("/Users/rsgoncalves/Documents/Harvard/23andme/panukbb/opengwas2panukbb.csv", index=False)
