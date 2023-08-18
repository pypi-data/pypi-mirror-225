import pandas as pd
from typing import List, Optional, Any


def sort_index(df: pd.DataFrame, index_list: list, axis: int = 1, inplace: bool = False, 
                level=None, sort_remaining=True, kind='mergesort', ignore_index=False) -> pd.DataFrame:
    """
    对DataFrame的行或列进行自定义排序。

    Parameters:
    - df (pd.DataFrame): 要排序的数据框。
    - index_list (list): 作为排序基准的行或列索引列表。
    - axis (int): 0表示对行进行排序，1表示对列进行排序。
    - inplace (bool): 是否在原地修改数据框。
    - level: 如果不为None，则在指定的索引级别上排序。
    - sort_remaining (bool): 如果为True且按级别排序且索引为多级，则在按指定级别排序后按其他级别排序。
    - kind (str): 排序算法的选择。
    - ignore_index (bool): 如果为True，结果轴将被标记为0, 1, …, n - 1。

    Returns:
    - pd.DataFrame: 已排序的数据框或None（如果inplace=True）。
    """
    # 创建一个函数，确定如何排序索引
    def indexer(indices):
        indices_list = indices.tolist()
        return [index_list.index(i) if i in index_list else len(index_list) + indices_list.index(i) for i in indices_list]
    
    return df.sort_index(axis=axis, key=indexer, inplace=inplace, level=level, 
                         sort_remaining=sort_remaining, kind=kind, ignore_index=ignore_index)


def value_counts(df: pd.DataFrame,
                subsets: List[str] = None,
                digits: int = 2, 
                max_bins: int = 5, 
                sort: bool = True, 
                bin_threshold: int = 15) -> pd.DataFrame:
    
    def value_counts_for_column(column: pd.Series) -> pd.Series:
        if pd.api.types.is_numeric_dtype(column) and column.nunique(dropna=True) >= bin_threshold:
            dynamic_bins = min(column.nunique(dropna=True) - 1, max_bins)
            column = pd.cut(column, bins=dynamic_bins, include_lowest=True, right=False).astype(str)

        counts = column.value_counts(dropna=True, sort=sort).to_dict()
        percents = (column.value_counts(normalize=True, dropna=True, sort=sort) * 100).to_dict()
        rounded_percents = {key: round(value, digits) for key, value in percents.items()}

        counts_with_na = column.value_counts(dropna=False, sort=sort).to_dict()
        percents_with_na = (column.value_counts(normalize=True, dropna=False, sort=sort) * 100).to_dict()
        rounded_percents_with_na = {key: round(value, digits) for key, value in percents_with_na.items()}

        return pd.Series([
            counts, percents, rounded_percents, 
            counts_with_na, percents_with_na, rounded_percents_with_na
        ], index=[
            'freq', 'freq_pc', 'freq_pc_round',
            'freq_with_na', 'freq_pc_with_na', 'freq_pc_round_with_na'
        ])

    # 根据subsets决定要操作的列
    if subsets is not None:
        df = df[subsets]

    return df.apply(value_counts_for_column, axis=0).T

def na_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算DataFrame中每列的缺失值数量和百分比。

    Parameters:
    - df (pd.DataFrame): 要计算的DataFrame

    Returns:
    - pd.DataFrame: 包含每列的缺失值数量和百分比的DataFrame。
    """
    missing_data = pd.concat([
        df.isnull().sum().rename('nmissing'),
        (df.isnull().mean() * 100).rename('pcmissing')
    ], axis=1)
    
    return missing_data

def describe(df: pd.DataFrame) -> pd.DataFrame:
    """
    为给定的DataFrame的每个列提供描述性统计。
    
    Parameters:
    - df (pd.DataFrame): 要描述的DataFrame
    
    Returns:
    - pd.DataFrame: 包含描述性统计和值计数的DataFrame
    """
    # 使用pandas的describe函数得到描述性统计
    base = df.describe(include='all').T
    base = base.drop(columns=set(['freq', 'top']) & set(base.columns))
    
    uid = isid(df)

    freq_counts = value_counts(df)
    
    na_data = na_counts(df)  
    dtypes = df.dtypes.rename('column_dtype')

    desc_df = pd.concat([base, dtypes,uid, na_data, freq_counts],axis=1)
    
    desc_df.rename(columns={
        '25%': 'p25',
        '50%': 'p50',
        '75%': 'p75'
    }, inplace=True)
    
    return desc_df


def isid(df: pd.DataFrame) -> pd.Series:
    """
    判断DataFrame中的每列是否可以作为唯一标识符 (ID)。
    
    Parameters:
    - df (pd.DataFrame): 要判断的DataFrame

    Returns:
    - pd.DataFrame: 对于每列是否可以作为ID的布尔结果，列名为'isid'。
    """
    return pd.DataFrame((df.nunique(dropna=True) == df.shape[0]).rename("isid"))


def group_cut(df: pd.DataFrame, 
              usecols: List[str] | str,  
              bins:int, 
              labels: Optional[List[str]]=None , 
              right:bool =False, 
              group_names:Optional[List[str]]=None):
    """
    Function to add new columns to the DataFrame based on value ranges of specified columns.
    
    Parameters:
    - df: DataFrame
    - column_names: The names of the columns to cut. Can be a single column name (string) or a list of column names.
    - bins: A sequence of scalars defining the bin edges.
    - labels: Labels for the resulting bins.
    - right: Indicates whether the bins include the rightmost edge or not. Default is False.
    - group_names: Optional list of names for the new columns. Default is None.
    
    Returns:
    - DataFrame with new columns.
    """
    
    if isinstance(usecols, str):
        usecols = [usecols]  
    
    if group_names is None:
        group_names = [f"{col}_group" for col in usecols]
    
    for col, new_col_name in zip(usecols,group_names):
        df[new_col_name] = pd.cut(df[col], bins=bins, labels=labels, right=right)
    
    return df





@pd.api.extensions.register_dataframe_accessor("ext")
class ExtendedDataFrame:
    def __init__(self, df: pd.DataFrame):
        self._df = df

    def na_counts(self) -> pd.DataFrame:
        return na_counts(self._df)

    def describe(self) -> pd.DataFrame:
        return describe(self._df)

    def isid(self) -> pd.DataFrame:
        return isid(self._df)

    def value_counts(self, subsets: Optional[List[str]] = None, 
                     digits: int = 2, max_bins: int = 5, sort: bool = True, bin_threshold: int = 15) -> pd.DataFrame:
        return value_counts(self._df, subsets, digits, max_bins, sort, bin_threshold)
    
    def group_cut(
        self, 
        usecols: List[str] | str,  
        bins:int, 
        labels: Optional[List[str]]=None , 
        right:bool =False, 
        group_names:Optional[List[str]]=None
        )-> pd.DataFrame:
        
        return group_cut(self._df, usecols, bins, labels, right, group_names)
    
    def sort_index(self, index_list: list, axis: int = 1, inplace: bool = False, 
                level=None, sort_remaining=True, kind='mergesort', ignore_index=False) -> pd.DataFrame:
        return sort_index(self._df, index_list, axis, inplace, level, sort_remaining, kind, ignore_index)