import pandas as pd
import re
from ast import literal_eval
from typing import Callable

def extract_at_index_func(i: int) -> Callable:
    """
    :param i: index
    :return: lambda with get list as parameter and return value at i
    """
    return lambda arr: arr[i]

def to_float_cm(text: str) -> float:
    """
    Convert string to height in float. If text is given in meters then convert to cm
    :param text: str to convert
    :return: height in cm
    """
    n = extract_number(text)
    if 'meters' in text:
        n = n * 100
    return n

def to_float_kg(text: str) -> float:
    """
    Convert string to weight in float. If text is given in tons then convert to kg
    :param text: str to convert
    :return: weight in kg
    """
    n = extract_number(text)
    if 'tons' in text:
        n = n * 1000
    return n

def extract_number(text: str) -> float:
    """
    Extract number in float from given text
    :param text:
    :return: number
    """
    findedList = re.findall(r"[-+]?(?:\d*[.,]*\d+)", text)
    finded = findedList[0]
    replaced = finded.replace(',', '')
    return float(replaced)

def extract_from_list_column(df: pd.DataFrame, column_name: str, converter: Callable) -> pd.DataFrame:
    """
    Get list from given column, convert it using given converter and save value in column
    :param df: given DataFrame to process
    :param column_name: column not process
    :param converter:
    :return: DataFrame with converted column
    """
    df.loc[:,['tmp_array']] = df[column_name].apply(literal_eval)
    df = df[~df['tmp_array'].apply(lambda a: len(a) < 2)]
    df.loc[:,['tmp']] = df['tmp_array'].apply(extract_at_index_func(1))
    df.loc[:,[column_name]] = df['tmp'].apply(converter)

    return df.drop(columns=['tmp_array', 'tmp']).astype({column_name: 'float'})