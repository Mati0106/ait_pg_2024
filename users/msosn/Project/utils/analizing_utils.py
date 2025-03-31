import pandas as pd
import numpy as np
import scipy.stats as stats


def print_nan_stat_in_row(data_frame: pd.DataFrame):
    """
    Function print number of rows with n columns with NaN
    n is a number from 0 to column number in given DataFrame
    :param data_frame: DataFrame to analyze
    """
    for i in range(0, data_frame.shape[1]):
        nan_rows = data_frame[data_frame.isna().sum(axis=1) == i].shape[0]
        all_rows = data_frame.shape[0]
        print(f"Column number with NaN: {i}, Rows number: {all_rows}, Rows number with NaN: {nan_rows}, percent: {nan_rows / all_rows * 100}")

def calc_outliers(data_frame: pd.DataFrame, column_name: str) -> int :
    """
    Function return number of outliers in given column
    :param data_frame: DataFrame to analyze
    :param column_name: given column
    :return: number of outliers in given column
    """
    return data_frame[~(np.abs(stats.zscore(data_frame[column_name])) < 3)].shape[0]

def remove_outliers(data_frame: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Function remove outliers from given DataFrame
    :param data_frame: given DataFrame
    :param column_name: given column
    :return: DataFrame without outliers
    """
    return data_frame[(np.abs(stats.zscore(data_frame[column_name])) < 3)]