# Example 1: Loading a CSV file into a DataFrame

import pandas as pd
from joblib import Parallel, delayed
import numpy as np

# Load a CSV file into a DataFrame
df = pd.read_csv('datasets/cars.csv')

# Display the first few rows of the DataFrame
print(df.head())
# In this example, we use the read_csv function from Pandas to load a CSV file named data.csv into a DataFrame.


#PARALLEL
length = len(df)

df['target'] = ['a' if i < length / 3 else 'b' if i < 2 * length / 3 else 'c' for i in range(length)]

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

def calculate_mean(col, target):
    mean_val = col.mean()
    return mean_val


results = Parallel(n_jobs=-1)(delayed(calculate_mean)(df[col], df['target']) for col in numeric_cols if col != 'target')

mean_dict = dict(zip(numeric_cols, results))