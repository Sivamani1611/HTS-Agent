import pandas as pd
import os
import glob

input_folder = "data/hts_csvs"
output_file = os.path.join(input_folder, "section_i.csv")

# Get all CSV files matching pattern 'htsdata*.csv'
csv_files = glob.glob(os.path.join(input_folder, "htsdata*.csv"))

dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv(output_file, index=False)

print(f"Combined Section I CSV saved to {output_file}")
