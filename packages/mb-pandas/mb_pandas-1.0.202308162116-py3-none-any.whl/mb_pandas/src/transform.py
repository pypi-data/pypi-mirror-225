##Pandas file checker

import pandas as pd
from .dfload import load_any_df
from mb_utils.src.logging import logger
import numpy as np
import cv2

__all__ = ['check_null','remove_unnamed','rename_columns','check_drop_duplicates','get_dftype','merge_chunk','merge_dask']

def merge_chunk(df1,df2,chunksize=10000,logger=None,**kwargs):
    """
    Merging 2 DataFrames in chunks
    
    Args:
        df1 : First DataFrame
        df2 : Second DataFrame
        chunksize : chunksize to merge
        logger : logger
    Returns:
        df : merged DataFrame
    """
    if df1.shape[0] > df2.shape[0]:
        df1,df2 = df2,df1

    merge_on = set(df1.columns) & set(df2.columns)
    if not merge_on:
        raise ValueError("No common columns to merge on") 
    
    list_df = [df2[i:i+chunksize] for i in range(0, df2.shape[0],chunksize)]
    if logger:
        logger.info(f'Size of chunk: {chunksize}')
        logger.info(f'Number of chunks: {len(list_df)}')
    
    #merged_chunks = []

    # for chunk in list_df:
    #     merged_chunk = pd.merge(df1, chunk, **kwargs)
    #     merged_chunks.append(merged_chunk)

    # res = pd.concat(merged_chunks,ignore_index=True)
    # return res    
    
    for chunk in list_df:
        merged_chunk = pd.merge(df1,chunk,**kwargs)
        res = pd.concat([res, merged_chunk])
    
    res = res.reset_index(drop=True)
    return res
    
 
def merge_dask(df1,df2,logger=None,**kwargs):
    """
    Use dask to merge 2 DataFrames
    
    Args:
        df1 : First DataFrame : pandas DataFrame
        df2 : Second DataFrame :  pandas DataFrame
    Returns:
        df : merged DataFrame : pandas DataFrame
    """
    
    import dask.dataframe as dd
    
    if logger:
        logger.info('Converting pandas DataFrames to Dask DataFrames')
    #Convert pandas DataFrames to Dask DataFrames
    ddf1 = dd.from_pandas(df1, npartitions=2)
    ddf2 = dd.from_pandas(df2, npartitions=2)

    # Merge Dask DataFrames
    merged_ddf = dd.merge(ddf1, ddf2, **kwargs)

    # Compute the result and convert back to a pandas DataFrame
    merged_df = merged_ddf.compute()
    if logger:
        logger.info('Merged DataFrame and converted back to pandas DataFrame')
    return merged_df
    

def check_null(file_path,fillna=False,logger=None) -> pd.DataFrame:
    """
    Pandas file checker. Checks Null values
    Input: 
        file_path (csv): path to csv file
        fillna (bool): fillna with False
    Output:
        df (pd.DataFrame): pandas dataframe
    """
    if logger:
        logger.info('Loading file: {}'.format(file_path))
    df = load_any_df(file_path)
    if logger:
        logger.info(f'Checking file: {file_path}')
        logger.info(f'File shape: {df.shape}')
        logger.info(f'File columns: {df.columns}')
        logger.info(f'File head: {df.head()}')
        logger.info('Checking Null values')
    for df_c in df.columns:
        if df_c.isnull().values.any():
            if logger:
                logger.warning(f'Column {df_c} has null values')
                logger.info(len(df[df[df_c].isnull()]))
            if fillna:
                if df[df_c].dtype == 'int':    
                    if logger:
                        logger.info('Filling null values with 0')
                    df[df_c] = df[df_c].fillna(0)
                elif df[df_c].dtype == 'float':
                    if logger:    
                        logger.info('Filling null values with 0.0')
                    df[df_c] = df[df_c].fillna(0.0)
                else:
                    if logger:
                        logger.info('Going to next column')
    return df

def remove_unnamed(df,logger=None):
    """
    Remove unnamed columns
    Input:
        df (pd.DataFrame): pandas dataframe
    Output:
        df (pd.DataFrame): pandas dataframe
    """
    if logger:
        logger.info('Removing unnamed columns')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if logger:
        logger.info(f'Columns : {df.columns}')
    return df

def rename_columns(df,new_column,old_column,logger=None):
    """
    Rename columns
    Input:
        df (pd.DataFrame): pandas dataframe
        new_column (list): new column names
        old_column (list): old column names
    Output:
        df (pd.DataFrame): pandas dataframe
    """
    if old_column not in df.columns:
        if logger:
            logger.warning(f'Column {old_column} not in dataframe')
            assert old_column in df.columns, f'Column {old_column} not in dataframe'
        return df
    df = df.rename(columns={old_column:new_column})
    if logger:
        logger.info(f'Column {old_column} renamed to {new_column}')
    return df

def check_drop_duplicates(df,columns,drop=False,logger=None):
    """
    Drop duplicates
    Input:
        df (pd.DataFrame): pandas dataframe
        columns (list): columns to drop duplicates
        drop (bool): drop duplicates
    Output:
        df (pd.DataFrame): pandas dataframe
    """
    if logger:
        logger.info('Checking duplicates for the columns: {}'.format(columns))
    df_warn = df[df.duplicated(columns,keep=False)]
    if len(df_warn)> 0 and drop==True:
        if logger:
            logger.warning('Duplicates found')
            logger.info(f'Dropping duplicates from columns: {columns}')
        df = df.drop_duplicates(columns)
        if logger:
            logger.info('Duplicates dropped')
    elif len(df_warn)> 0 and drop==False:
        if logger:
            logger.warning('Duplicates found')
            logger.info(f'Not dropping duplicates from columns: {columns}')
    else:
        if logger:
            logger.info('No duplicates found')
    return df

def get_dftype(s):
    '''Detects the dftype of the series.
    Determine whether a series is an ndarray series, a sparse ndarray series, an Image series or a
    normal series.
    Parameters
    ----------
    s : pandas.Series
        the series to investigate
    Returns
    -------
    {'json', 'ndarray', 'SparseNdarray', 'Image', 'str', 'Timestamp','Timedelta', 'object', 'none', etc}
        the type of the series. If it is a normal series, the string representing the dtype
        attribute of the series is returned
    '''
    if len(s) == 0:
        return 'object'

    dftype = None
    for x in list(s):
        if isinstance(x, str):
            if dftype is None:
                dftype = 'str'
            elif dftype != 'str':
                break
            continue
        if isinstance(x, (list, dict)):
            if dftype is None:
                dftype = 'json'
            elif dftype != 'json':
                break
            continue
        if isinstance(x, np.ndarray):
            if dftype is None:
                dftype = 'ndarray'
            elif dftype != 'ndarray':
                break
            continue
        if isinstance(x, np.SparseNdarray):
            if dftype is None:
                dftype = 'SparseNdarray'
            elif dftype != 'SparseNdarray':
                break
            continue
        if isinstance(x, cv2.Image):
            if dftype is None:
                dftype = 'Image'
            elif dftype != 'Image':
                break
            continue
        if isinstance(x, pd.Timestamp):
            if dftype is None:
                dftype = 'Timestamp'
            elif dftype != 'Timestamp':
                break
            continue
        if isinstance(x, pd.Timedelta):
            if dftype is None:
                dftype = 'Timedelta'
            elif dftype != 'Timedelta':
                break
            continue
        dftype = 'object'
        break

    if dftype is None:
        return 'none'

    if dftype != 'object':
        return dftype

    dftype = str(s.dtype)
    if dftype != 'object':
        return dftype

    # one last attempt
    types = s.apply(type).unique()
    is_numeric = True
    for x in types:
        if not pd.api.types.is_numeric_dtype(x):
            is_numeric = False
            break
    return 'float64' if is_numeric else 'object'