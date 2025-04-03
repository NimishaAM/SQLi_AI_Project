import pandas as pd

# Load your dataset
df = pd.read_csv('../data/sql_injection_data.csv')

# Display first few rows
print("First 5 rows of your dataset:\n")
print(df.head())

# Check dataset shape (rows, columns)
print("\nShape of your dataset (rows, columns):", df.shape)

# Display column names clearly
print("\nColumn names in your dataset:", df.columns.tolist())

# Check label distribution if present
if 'Label' in df.columns:
    print("\nDistribution of labels:\n", df['Label'].value_counts())
elif 'label' in df.columns:
    print("\nDistribution of labels:\n", df['label'].value_counts())
else:
    print("\nNo column named 'Label' or 'label' found. Please manually check column names.")
