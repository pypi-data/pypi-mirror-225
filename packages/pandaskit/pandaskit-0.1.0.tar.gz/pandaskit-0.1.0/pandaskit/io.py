from typing import Dict, List, Optional,Tuple, Literal, Any
from pathlib import Path
import pandas as pd
import pyreadstat
import numpy as np
from ._dataframe import ExtendedDataFrame

def _pyreadstat_metadata_to_df(meta: pyreadstat.metadata_container)->pd.DataFrame:
    """转换pyreadstat元数据为df

    Args:
        metadata (pyreadstat.metadata_container): _description_

    Returns:
        pd.DataFrame: _description_
    """
    
    column_info = {
        'column_label': meta.column_names_to_labels,
        'column_pyreadstat_dtype': meta.readstat_variable_types,
        'column_value_labels': meta.variable_value_labels,
        'column_nacodes': meta.missing_user_values, 
        'column_stata_dtype': meta.original_variable_types,
        'column_stata_vlabel': meta.variable_to_label 
        }
    
    df = pd.concat([pd.Series(data, name=name) for name, data in column_info.items()], axis=1)
    
    df.eval('''
            table_name = @meta.table_name
            file_format = @meta.file_format
            file_encoding = @meta.file_encoding
            file_label = @meta.file_label
            file_notes = @meta.notes
            file_ncols = @meta.number_columns
            file_nrows = @meta.number_rows
            file_path = @meta.file_path
        ''', inplace=True)
    
    return df

def read_stata(file_path: str | Path, 
               table_name: Optional[str] = None,
               usecols: Optional[List[str]]=None, 
               nrows: int = 0, 
               nrow_start: int = 0,
               keep_ext_missings: bool = False,
               apply_value_labels: bool = False,
               convert_time: bool = False,
               to_ordered_categoricals: bool = False,
               encoding: str = 'utf-8',
               output: Literal['all','data','meta'] = 'data',
               ) -> pd.DataFrame | Tuple[pd.DataFrame, pd.DataFrame]:
    """
    使用pyreadstat读取dta文件为pandas dataframe
    
    Args:
        file_path (str | Path): dta文件路径，本地路径或远程URL
        table_name (str, optional): 表名
        usecols (List[str], optional): 可选，指定读取列名列表
        nrows (int, optional): 指定读取的行数. 默认0代表读取所有行.
        nrow_start (int, optional): 指定行开始读取的索引号. 默认0从第0行开始.
        keep_ext_missings (bool, optional): 是否保留stata扩展缺失值为值. 默认False.
        convert_value_labels (bool, optional): 是否将变量值标签应用到df作为categorical. 默认False.
        to_ordered_categoricals (bool, optional): 是否转换的categorical是有序的. 默认False.
        encoding (str, optional): 制定读取的编码. 默认'utf-8'.
        convert_time (bool, optional): 是否转换时间变量为pandas datetime类型. 默认False.
        output (Literal['both','data','meta'], optional): 返回类型
            both为数据和元信息，data为仅数据，meta为仅元信息. 默认为both
    Returns:
        pd.DataFrame | Tuple[pd.DataFrame, pd.DataFrame]: 
            DataFrame and metadata that contains the data from the .dta file
    """
    
    file_path = Path(file_path)
    
    df, meta = pyreadstat.read_dta(
        filename_path=file_path, 
        usecols=usecols, 
        row_limit=nrows, 
        row_offset=nrow_start,
        user_missing=keep_ext_missings,
        dates_as_pandas_datetime=convert_time,
        apply_value_formats=apply_value_labels,
        formats_as_category=apply_value_labels,
        formats_as_ordered_category=to_ordered_categoricals,
        encoding=encoding,
        disable_datetime_conversion = convert_time
    )

    # Update meta information
    meta.file_encoding = encoding
    meta.file_path = str(file_path)
    meta.file_label = meta.file_label or np.nan
    meta.notes = ' '.join(meta.notes) if meta.notes else np.nan
    meta.table_name = table_name or file_path.stem

    # Create meta dataframe
    if output in ["all", "meta"]:
        meta_base = _pyreadstat_metadata_to_df(meta)
        meta_desc = df.ext.describe()
        meta_df = pd.concat([meta_base, meta_desc], axis=1).rename_axis('column_name')
        
        meta_df.ext.sort_index(index_list= ['column_label','column_dtype','table_name'], inplace=True)

    if output == "all":
        return df, meta_df
    elif output == "data":
        return df
    elif output == "meta":
        return meta_df