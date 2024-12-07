# Example 1: Loading a CSV file into a DataFrame

import pandas as pd

"""  Adding automated link from git

from pathlib import Path
print(Path.cwd().parents[1])
"""

# Load a CSV file into a DataFrame
df = pd.read_csv('datasets/cars.csv')

# Display the first few rows of the DataFrame
print(df.head())
pd.set_option('display.max_columns', 9)
# In this example, we use the read_csv function from Pandas to load a CSV file named data.csv into a DataFrame.

# Example 2: Exploring DataFrame Information

# Display the column names and data types
print("Column Names and Data Types:")
print(df.dtypes)

# Display summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Display the shape of the DataFrame
print("\nDataFrame Shape:", df.shape)
# Here, we explore information about the DataFrame, such as column names, data types, summary statistics, and the shape of the DataFrame.

# Example 3: Selecting and Filtering Data

# Select a single column
column_data = df['weight']

# Select multiple columns
multiple_columns = df[['weight', 'acceleration']]

# Filter rows based on a condition
filtered_data = df[df['acceleration'] > 10]
print(filtered_data)
# In this example, we demonstrate how to select specific columns and filter rows based on conditions in the DataFrame.

# Example 4: Grouping and Aggregating Data

# Group data by a column and calculate mean
##mean_by_group = df.groupby('acceleration').mean()


# Perform multiple aggregations
########agg_results = df.groupby('Column_Name').agg({'Column1': 'mean', 'Column2': 'sum'})
# Here, we group the data by a column and perform aggregations such as mean calculation and summing across multiple columns.

# Example 5: Handling Missing Values

# Drop rows with missing values
#######df_dropna = df.dropna()

# Fill missing values with a specified value
######df_fillna = df.fillna(0)
# In this example, we demonstrate how to handle missing values by either dropping rows with missing values or filling them with a specified value.

############# ZADANKO NA ZAJECIACH

# new column target  EX1
val_target = ['a', 'b', 'c']
list_len = int(len(val_target))
df_nb_row = int(df.weight.count())
parts = int(round(df_nb_row / list_len, 0))
# print(parts)
list_target_v2 = sorted(list(n for n in val_target) * parts)
list_target_v3 = list_target_v2[0: df_nb_row]
# list_target = ["a" for n in range(0, parts)] + ["b" for n in range(parts, parts*2)] + ["c" for n in range(parts*2, df_nb_row)]
new_df = df.copy()
target = 'target'
new_df[target] = list_target_v3
# print(new_df.head())


from time import time
from joblib import Parallel, delayed


def mean_for_all(column1: str, column2: str):
    print(f"Fix column {column1} and {column2}")
    return new_df.groupby([new_df[column1], new_df[column2]]).mean(numeric_only=True)


## EX2 dla kazdej kolumny mean zrobic
start_time = time()
mean_all = [mean_for_all(i, target) for i in new_df.columns if i != target]
# print(mean_all)
sequential_duration = time() - start_time
print(f"Sequential Execution Time: {sequential_duration:.4f} seconds")

# mean_all_paraller = new_df.groupby(['mpg','target']).mean(numeric_only=True)

## EX2 z PARALLEL i DELAYED
start_time = time()
squares_parallel = Parallel(n_jobs=-1)(delayed(mean_for_all)(i, target) for i in new_df.columns if i != target)
parallel_duration = time() - start_time
print(f"Parallel Execution Time: {parallel_duration:.4f} seconds ")

speedup = sequential_duration / parallel_duration
print(f"Speedup using Parallel: {speedup:.2f}x faster")

##  dla kazdego z target zrobic srednie

target_mean = new_df.groupby(target).mean(numeric_only=True)
print(target_mean)




## EX 3
import sklearn.datasets
import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

"""

target_df1 = new_df[new_df[target] == val_target[0]]
target_df2 = new_df[new_df[target] == 'b']
target_df3 = new_df[new_df[target] == 'c']

for n in range(0, list_len):
    n = (new_df[new_df[target] == str(val_target[i])] for i in range(1, list_len))
    print(n)
 ##print(val_target[0])
 """
from pathlib import Path

print(Path(Path.cwd(),"users","karakrzyz",f"my_report_1.html"))

def part_df(grouping_val):
    return new_df[new_df[target] == val_target[grouping_val]]


def report_creation(data_target):
    report = ProfileReport(part_df(data_target), title='My Data', correlations={
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "kendall": {"calculate": True}
    })
    report.to_file(Path(Path.cwd(),"users","karakrzyz",f"my_report_{data_target}.html"))



## Without paraller
start_time = time()
reports_ = [report_creation(i) for i in range(0, list_len)]
# print(mean_all)
diff_without = time() - start_time
print(f"Sequential Execution Time: {diff_without:.4f} seconds")

# mean_all_paraller = new_df.groupby(['mpg','target']).mean(numeric_only=True)

## PARALLEL i DELAYED
start_time = time()
reports_paraller = Parallel(n_jobs=-1)(delayed(report_creation)(i) for i in range(0, list_len))
diff_with = time() - start_time
print(f"Parallel Execution Time: {diff_with:.4f} seconds ")

speedup = diff_without / diff_with
print(f"Speedup using Parallel: {speedup:.2f}x faster")
