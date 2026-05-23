
import pandas as pd

df_2024=pd.read_excel(
    "school_income_dataset_2024.xlsx"
)

df_2025=pd.read_excel(
    "school_income_dataset_2025.xlsx"
)

df_2024["Year"]=2024
df_2025["Year"]=2025

merged_df=pd.concat(
    [df_2024,df_2025],
    ignore_index=True
)

merged_df.to_excel(
    r"C:\Users\hp\OneDrive\Desktop\merged_school_dataset.xlsx",
    index=False
)

print("Datasets Merged Successfully")

print(merged_df.head())