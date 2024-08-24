import pandas as pd
import os

# List of XPT file names
xpt_files = [
    'P_DEMO', 'P_DR1TOT', 'P_DSQIDS', 'P_DSQTOT', 'P_BMX', 'P_BPXO', 'P_BIOPRO',
    'P_ALB_CR', 'P_UCFLOW', 'P_GLU', 'P_UM', 'P_BPQ', 'P_DIQ', 'P_DBQ', 'P_KIQ_U',
    'P_MCQ', 'P_PAQ', 'P_SMQ', 'P_SMQFAM', 'P_ALQ', 'P_SLQ', 'P_RXQ_RX'
]

# Read all XPT files
dataframes = {}
for file in xpt_files:
    file_path = f"{file}.XPT"
    if os.path.exists(file_path):
        try:
            dataframes[file] = pd.read_sas(file_path, format='xport')
            print(f"Successfully read {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    else:
        print(f"File not found: {file_path}")

# Merge all dataframes on SEQN column
merged_df = None
for name, df in dataframes.items():
    if 'SEQN' in df.columns:
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on='SEQN', how='outer')
    else:
        print(f"SEQN column not found in {name}")

# Check the result
if merged_df is not None:
    print("Merged dataframe shape:", merged_df.shape)
    print("Columns in merged dataframe:", merged_df.columns)
else:
    print("No dataframes were merged. Check if SEQN column exists in the files.")

# Save the merged dataframe to a CSV file (optional)
if merged_df is not None:
    print("Merged data saved to 'merged_data.csv'")


# Define the variables to keep
variables_to_keep = [
    # demographic
    "SEQN", "RIAGENDR", "RIDAGEYR", "RIDRETH3", "INDFMPIR", "DMDEDUC2", "DMDMARTZ",
    
    # dietary
    "DBQ095Z", "DBD100", "DRQSPREP",
    "DR1TKCAL", "DR1TP226",
    "DR1_320Z", "DR1TWSZ",
    "DSDANTA", "DSD128V", "DSD128FF",
    "DSQTKCAL",
    
    # examination
    "BMXBMI",
    "BPXOSY1", "BPXOSY2", "BPXOSY3", "BPXODI1", "BPXODI2", "BPXODI3", "BPXOPLS1", "BPXOPLS2", "BPXOPLS3",
    
    # laboratory
    "LBXSBU", "LBXSCA", "LBXSUA",
    "URDACT",
    "URDFLOW1", "URDFLOW2", "URDFLOW3",
    "LBXGLU",
    "URXUPB",
    
    # questionnaire
    "BPQ020", "BPQ080", "BPQ050A",
    "DIQ010", "DIQ050", "DIQ070", "DIQ160",
    "DBD895", "DBD900", "DBD905", "DBD910", "DBQ700",
    "KIQ022", "KIQ026", "KIQ005", "KIQ010", "KIQ042", "KIQ044", "KIQ046", "KIQ480",
    "MCQ080", "MCQ160M", "MCQ520", "MCQ550", "MCQ366A", "MCQ366B", "MCQ366C", "MCQ366D", "MCQ160L", "MCQ300C",
    "PAQ605", "PAQ620", "PAQ635", "PAQ650", "PAQ665", "PAD680",
    "SMQ020", "SMQ040",
    "SMD460", "SMD470",
    "ALQ130",
    "SLQ050",
    "RXDDAYS", "RXDCOUNT"
]

# Select only the variables we want to keep
selected_df = merged_df[variables_to_keep]

# Check the shape of the new dataframe
print("Shape of selected dataframe:", selected_df.shape)

# Display the first few rows of the selected dataframe
print(selected_df.head())

# Check for any missing columns
missing_columns = set(variables_to_keep) - set(selected_df.columns)
if missing_columns:
    print("Warning: The following columns were not found in the merged dataset:")
    for col in missing_columns:
        print(f"- {col}")

# Save the selected dataframe to a CSV file (optional)
selected_df.to_csv('selected_nhanes_data.csv', index=False)
print("Selected data saved to 'selected_nhanes_data.csv'")


#remove duplicates based only on the 'SEQN' column:
selected_df = selected_df.drop_duplicates(subset=['SEQN'], keep='first')

# Print the shape of the dataframe after removing duplicates
print("Shape of dataframe after removing duplicates:", selected_df.shape)
original_shape = selected_df.shape
# Save the deduplicated dataframe to a CSV file
output_file = 'deduplicated_nhanes_data.csv'
selected_df.to_csv(output_file, index=False)
print(f"Deduplicated data saved to '{output_file}'")

# Optionally, you can also save information about the deduplication process
with open('deduplication_log.txt', 'w') as f:
    f.write(f"Original shape: {original_shape}\n")
    f.write(f"Shape after deduplication: {selected_df.shape}\n")
    f.write(f"Number of duplicates removed: {original_shape[0] - selected_df.shape[0]}\n")


print("Number of NA values in KIQ026:", selected_df['KIQ026'].isna().sum())
