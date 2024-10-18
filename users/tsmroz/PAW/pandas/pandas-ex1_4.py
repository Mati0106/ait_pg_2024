# Exercise - using pathlib
from pathlib import Path, PurePath

print(Path.cwd())

path = Path.cwd().parents[1]
print(path)

path = Path.cwd().parents[3].joinpath('datasets/cars.csv')
print(path)


## Example 1: Loading a CSV file into a DataFrame
import pandas as pd

df = pd.read_csv(path)
print(df.head())

pd.set_option('display.max_columns', 9)
print(df.head())

## Example 2: Exploring DataFrame Information
print(df.describe())

print(df.dtypes)

print(df.shape)

## Example 3: Selecting and Filtering Data
df = pd.DataFrame({
    'a':[1,2,3],
    'b':[2,2,2],
    'c':[3,3,3]
})
print(df)

print(df['a'])
print(df[['a','b']])
print(df[df['a']>2])

df['target']=[0,1,0]
df['typ']=['a','a','b']

## Example 4: Grouping and Aggregating Data
print('\n')
print(df)

print(df.groupby('typ').mean())
print(df.groupby('typ').agg('sum', 'mean'))

## Example 4.1: Using parallel computing

from joblib import Parallel, delayed

# Computation per columns
cols=['a', 'b', 'c', 'target']
def calc(col_name: str) -> float:
    return df[col_name].mean()

results_1 = Parallel(n_jobs=-1)(delayed(calc)(c) for c in cols)
print(results_1)

# Computation per rows
def calc2(val: str) -> float:
    return df.query('typ==@val')[['a','b','c']].mean(axis=1)

results_2 = Parallel(n_jobs=-1)(delayed(calc2)(v) for v in df['typ'].unique())
print(results_2)

print(results_2[0])
print(results_2[1])
