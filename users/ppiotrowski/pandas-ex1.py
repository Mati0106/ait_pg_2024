import os
from time import time
from pathlib import Path
from typing import Any, List

import pandas
import pandas as pd
from joblib import Parallel, delayed
from pandas.core.dtypes.common import is_numeric_dtype
from pandas.core.interchange.dataframe_protocol import DataFrame
from ydata_profiling import ProfileReport
from ydata_profiling.config import Dataset

PROJECT_NAME = 'machine-learning'
USER_DIR = 'ppiotrowski'

def getPathToRoot(start: Path):
    idx = 0
    for el in reversed(str(start).split(os.sep)):
        if el == PROJECT_NAME:
            break
        idx+=1
    if idx==0: raise FileNotFoundError()
    return Path(start.parents[idx-1])

def getPathToDatasetFile(fileName: str) -> Path:
    return Path(getPathToRoot(Path.cwd()), "datasets", fileName)

def getPathToUserDir(user: str):
    return Path(getPathToRoot(Path.cwd()), "users", user)

# Load a CSV file into a DataFrame
df = pd.read_csv(getPathToDatasetFile("cars.csv"))

# Display the first few rows of the DataFrame
print(df.head())
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

# define some constants
# add new column with values 'a' 'b' 'c'
newVals = ['a', 'b', 'c']
newColName = 'target'
dfLength = df.shape[0]
subrange = int(round(dfLength / len(newVals)))

print(f"-----\tEX1: adding new column '{newColName}' with vaules '{newVals}'\t-----")
df[newColName] = sorted([el for el in newVals] * subrange)[0:dfLength]
print(f"new shape: {df.describe}")

dfAllHeaders = df.columns.values
dfNumericHeaders = [ h for h in dfAllHeaders if is_numeric_dtype(df[h]) ]

print("-----\tEX2: parallel + delayed\t-----")
def countMean(df:pandas.DataFrame, firstCol: str, secondCol:str) -> Any:
    print(f"Calculating mean for cols: {firstCol} and {secondCol}")
    return df.groupby([df[firstCol], df[secondCol]]).mean(numeric_only=True)

def sequentialMeanCount(df: DataFrame) -> List[DataFrame]:
    return [countMean(df, newColName, header) for header in dfNumericHeaders]

# colsForMean = 'cylinders'
# print(f"mean of columns '{colsForMean}' is \n{countMean(df, newColName, colsForMean)}")

startTime = time()
print("starting sequential mean count for all columns")
sequentialMeanCount(df)
stopTime = time()
sequentialDuration = stopTime - startTime
print(f"Sequential Execution Time: {sequentialDuration:.4f} seconds")


startTime = time()
print("\n\nstarting parallel mean count for all columns")
Parallel(n_jobs=-1)(delayed(countMean)(df, newColName, header) for header in dfNumericHeaders)
stopTime = time()
parallelDuration = stopTime - startTime
print(f"Parallel Execution Time: {parallelDuration:.4f} seconds")


print("-----\tEX3: profiling reports\t-----")
def generateReport(df: DataFrame, title: str):
    report = ProfileReport(df, title=title,correlations = {
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "kendall": {"calculate": True}
    })
    reportName = "report_"+title
    path = Path(getPathToUserDir(USER_DIR), reportName+".html")
    print(f"saving report {title} to {str(path)}")
    report.to_file(path)

ex3DataSets: List[tuple[str, Dataset]] = []
for t in newVals:
    newDf = df[df[newColName]==t]
    ex3DataSets.append((t, newDf))
    print(f"filtering dataframe by {newColName} == {t}"
          f" new shape is: {newDf.shape}")
    # print(numpy.unique(newDf[dfAllHeaders].values))
    # no one seems to understand if the three datasets need to be filtered out of duplicates or not...
    # skipping as it is not stated by which column duplicates need to be removed...

Parallel(n_jobs=-1)(delayed(generateReport)
                    (df, title) for (title, df) in ex3DataSets)

