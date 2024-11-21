import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def scale(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Scale given columns in df using StandardScaler and replace values in DataFrame
    :param df: DataFrame
    :param columns: columns to scale
    :return: DataFrame
    """
    columns_filter = df.columns.isin(columns)
    for column in df.iloc[:, columns_filter].columns:
        df[column] = df[column].astype(float)

    df.loc[:, columns_filter] = StandardScaler().fit_transform(df.loc[:, columns_filter])
    return df

def replace_by_pca(df:pd.DataFrame, n_components: int, columns: list) -> pd.DataFrame:
    """
    Replace given column with n_components new column calculated by PCA
    :param df: DataFrame
    :param n_components: number of columns to calculate
    :param columns: columns to replace by new n_component
    :return: DataFrame with replace columns
    """
    columns_label = []
    for i in  range(n_components):
        columns_label.append(f'pca{i}')
    pca = PCA(n_components=n_components)
    pca_val = pca.fit_transform(df.loc[:, columns])
    pca_df = pd.DataFrame(data=pca_val, columns=columns_label)

    val_df = df.copy()
    pca_df = pca_df.set_index(val_df.index)
    for col in columns_label:
        val_df[col] = pca_df[col]

    val_df = val_df.drop(columns=columns)

    print(pca.explained_variance_ratio_.sum())
    return val_df