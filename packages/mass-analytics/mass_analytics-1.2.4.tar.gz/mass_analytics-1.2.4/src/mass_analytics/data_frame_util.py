import pandas as pd
import numpy as np
import datetime
import tqdm
from pandas.api.types import is_string_dtype
from .date import (get_date_columns,
                  is_date,
                  get_periodicity)


def pivot_by_key(df, index_column_names, key_column_names, values_column_names, agg_funcs='sum'):
    """
    Description
        Pivots a DataFrame based on the given keys and performs aggregation on the specified value columns.

    Parameters:
        df (pd.DataFrame): The DataFrame to pivot and perform aggregation on.
        index_column_names (list): List of column names to be used as index during pivoting.
        key_column_names (list): List of column names to be used as keys for pivoting.
        values_column_names (list): List of column names to be used as values for pivoting.
        agg_funcs (dict, optional): Dictionary mapping columns to aggregation functions. The default is {'column_name': 'sum'}.

    Returns:
        pd.DataFrame: The resulting pivoted DataFrame with aggregation.
    
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'Date': ['1/1/2020', '1/2/2020', '1/3/2020'],
        ...                    'col1': ['A', 'B', 'C'],
        ...                    'col2': ['X', 'Y', 'Z'],
        ...                    'price': [10, 11, 15],
        ...                    'nb': [2, 1, 3]})
        >>> result = pivot_by_key(df, index_column_names='Date', key_column_names=['col1', 'col2'],
        ...                       values_column_names=['price', 'nb'], agg_funcs={'price': 'mean', 'nb': 'sum'})
        >>> print(result)
        
             Date          A_X_nb   B_Y_nb   C_Z_nb   A_X_price   B_Y_price   C_Z_price    
        0    1/1/2020        2        0        0        10          0           0
        1    1/2/2020        0        1        0        0           11          0
        2    1/3/2020        0        0        3        0           0           15
    """
    
    df['key'] = df.apply(lambda x: '_'.join([str(x[st]) for st in key_column_names]), axis=1)
    pivot_table = pd.pivot_table(df, values=values_column_names, index=index_column_names, columns='key', aggfunc=agg_funcs, fill_value=0)

    new_df = pd.DataFrame()
    for cols in pivot_table.columns:
       new_df['_'.join(cols[::-1]).strip(" .;,:*-()[]/!?").replace(" ","_")] = pivot_table[cols]
       
    new_df.reset_index(inplace=True)
    
    return new_df

def get_mapping_table(df, date_column_name, column_values, freq='D', start_date=None, end_date=None):
    """
    Description
        Create a mapping table based on the provided DataFrame, date column, and column values.

        The function generates a new DataFrame that contains all unique combinations of the date
        values (within the specified frequency) and the unique values of each column in the 
        'column_values' list.

    Parameters:
        df (pandas.DataFrame): The original DataFrame containing the data.
        date_column_name (str): The name of the column that holds the date values.
        column_values (list): A list of column names for which unique values will be used
                              to create combinations in the mapping table.
        freq (str, optional): The frequency string for date_range(). 
                              Defaults to daily 'D'.
        start_date (str or None, optional): The start date of the mapping table.
                                            If None, the minimum date in the DataFrame's date_column_name
                                            will be used.
                                            Default is None.
        end_date (str or None, optional): The end date of the mapping table.
                                          If None, the maximum date in the DataFrame's date_column_name
                                          will be used.
                                          Default is None.

    Returns:
        pandas.DataFrame: A new DataFrame representing the mapping table with date_column_name 
                          and unique values from each column in column_values.

    Note:
        - Make sure to provide a valid 'freq' frequency string, such as 'D' for daily, 'M' for monthly, 
          'Y' for yearly, etc.
        - The returned DataFrame will have a row for each unique combination of date and column 
          values from the original DataFrame.

    Example:
        >>> import pandas as pd
        >>> data = {
        ...     'Date': ['2023-07-01', '2023-07-02'],
        ...     'Product': ['A', 'B'],
        ...     'Category': ['X', 'Y'],
        ...     'Price': [100, 150],
        ... }
        >>> df = pd.DataFrame(data)
        >>> result = get_mapping_table(df, date_column_name='Date', column_values=['Product', 'Category'], freq='D')
        >>> print(result)
            Product Category    Date
        0      A       X        2023-07-01
        1      A       X        2023-07-02 
        2      B       X        2023-07-01
        3      B       X        2023-07-02
        4      A       Y        2023-07-01
        5      A       Y        2023-07-02
        6      B       Y        2023-07-01
        7      B       Y        2023-07-02
    
    """
    
    new_df = pd.DataFrame()

    if start_date is None:
        start_date = min(df[date_column_name])
    if end_date is None:
        end_date = max(df[date_column_name])
                         
    new_df[date_column_name] = pd.date_range(start=start_date, end=end_date, freq=freq, inclusive='both')

    for col in column_values:
        new_df = pd.DataFrame(df[col].unique()).join(new_df, how='cross')
        new_df.rename(columns={0: col}, inplace=True)
    
    return new_df

def map_table(df, mapping_table):
    """
    Description
        The map_table function is designed to map data from the original DataFrame to the provided mapping table. 
        It performs a left merge between the mapping_table and the original DataFrame (df) based on their common date column(s). 
        The function then fills in missing values in the merged DataFrame with 0.

    Parameters:
        df (pandas.DataFrame): The original DataFrame containing the data to be mapped.
        mapping_table (pandas.DataFrame): The mapping table containing unique combinations of 
                                          data and columns to which the original data will be 
                                          mapped.

    Returns:
        pandas.DataFrame: A new DataFrame resulting from the left merge of the mapping_table and 
                          the original DataFrame (df), with missing values filled in with 0.
    
    Note:
        - The merge is performed based on the common columns between the mapping_table and the 
          original DataFrame. Make sure that the mapping_table and the df have at least one 
          common column.
        - Any missing values in the merged DataFrame are filled with 0.
        - The returned DataFrame will have the same number of rows as the mapping_table and will 
          include the additional columns from the original DataFrame (df) that matched the 
          common columns in the mapping_table.
    
    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'Date': ['2023-08-01', '2023-08-02', '2023-08-03', '2023-08-04', '2023-08-05'],
        ...     'Value': [10, 20, 30, 40, 50]
        ... })
        >>> mapping_table = pd.DataFrame({
        ...     'Date': ['2023-08-01', '2023-08-03'],
        ...     'Label': ['Label A', 'Label B']
        ... })
        >>> result_df = map_table(df, mapping_table)
        >>> print(result_df)

            Date        Value    Label
        0 2023-08-01     10     Label A
        1 2023-08-03     30     Label B
    """

    # Cast Object type to datetime (df)
    date_cols = get_date_columns(df)
    
    if type(date_cols) is str:
        date_cols = [date_cols]
    
    
    for col in date_cols:
        df = df.drop(df[df.apply(lambda x: not(is_date(x[col]) or isinstance(x[col], datetime.datetime)), axis=1)].index)
        if np.issubdtype(df[col].dtype, np.object_):
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                print("Can\'t cast object to datetime type")
    
    # Cast Object type to datetime (mapping_table)
    date_cols = get_date_columns(mapping_table)
    if type(date_cols) is str:
        date_cols = [date_cols]
    
    for col in date_cols:
        mapping_table = mapping_table.drop(mapping_table[mapping_table.apply(lambda x: not(is_date(x[col]) or isinstance(x[col], datetime.datetime)), axis=1)].index)
        if np.issubdtype(mapping_table[col].dtype, np.object_):
            try:
                mapping_table[col] = pd.to_datetime(mapping_table[col])
            except:
                print("Can\'t cast object to datetime type")
    
    map_table = mapping_table.merge(df, how='left').fillna(0)
    
    return map_table

def split_value_by_day(df, start_date_col, end_date_col, value_col, additive=True, Region=None):
    """
    Split the values in the 'value_col' column based on the daily or average allocation
    between the 'start_date_col' and 'end_date_col' period.

    Parameters:
        df (DataFrame): The input DataFrame containing the data.
        start_date_col (str): The name of the column in the DataFrame where the campaign starts.
        end_date_col (str): The name of the column in the DataFrame where the campaign ends.
        value_col (str): The name of the column in the DataFrame that contains the cost or price
                         between the start date and end date of the campaign.
        additive (bool, optional): If True, the costs will be split equally for each day within the campaign period.
                                   If False, the average value for the whole campaign period will be assigned to each day.
        region (str or None, optional): If region is None (default), the function will group the values based on the date only.
                                        If region is a valid column name in the DataFrame, the function will group the values
                                        based on both the region and date.

    Returns:
        DataFrame: A new DataFrame with the following columns:
            - 'region': The region from the input DataFrame (if 'region' parameter is not None).
            - 'Date': The date within the campaign period.
            - 'Value': The allocated value for each day in the campaign period.

    Example:
        >>> import pandas as pd
        >>> data = {
        ...     'start_date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-02']),
        ...     'end_date': pd.to_datetime(['2023-01-02', '2023-01-04', '2023-01-05']),
        ...     'val': [200, 800, 900],
        ...     'region': ['DC', 'DC', 'TX']
        ... }
        >>> df = pd.DataFrame(data)
        >>> result_df = split_value_by_day(df, 'start_date', 'end_date', 'val', additive=True, region='region')
        >>> print(result_df)

           region       Date       Value
         0     DC 2023-01-01  100.000000
         1     DC 2023-01-02  366.666667
         2     DC 2023-01-03  266.666667
         3     DC 2023-01-04  266.666667
         4     TX 2023-01-02  225.000000
         5     TX 2023-01-03  225.000000
         6     TX 2023-01-04  225.000000
         7     TX 2023-01-05  225.000000
    """
    
    # Create a new dataframe to store the split cost rows
    new_rows = []

    for _, row in df.iterrows():
        start_date = row[start_date_col]
        end_date = row[end_date_col]+  datetime.timedelta(days=1)
        num_days = (end_date - start_date).days   # Calculate the number of days

        # Calculate the split cost per day
        if additive:
            split_cost = row[value_col] / num_days
        else:
            split_cost = row[value_col]

        # Create new rows for each day with the split cost
        for day in pd.date_range(start_date, end_date, inclusive='left'):
            data = {
                #'Region': row['Region'],
                'Date': day,
                'Value': split_cost,
            }
            if Region is not None:
                data[Region] = row[Region]
            new_rows.append(data)

    # Create a new dataframe from the new rows
    if Region is None:
        new_df = pd.DataFrame(new_rows).groupby(['Date'])
    else:
        new_df = pd.DataFrame(new_rows).groupby([Region, 'Date'])
    
    if additive:
        return new_df.sum().reset_index()
    else:
        return new_df.mean().reset_index()

def get_nb_categories_overtime(df, date_col, categorical_col, division_col=None):
    """
    Calculate the number of unique categories over time.

    This function calculates the number of unique categories in the specified categorical column
    for each time point in the specified date column. It is useful for visualizing how the number
    of categories changes over time.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing the data.
        date_col (str): The name of the column in the DataFrame representing dates or timestamps.
        categorical_col (str): The name of the column in the DataFrame representing categories or groups.

    Raises:
        ValueError: If the provided `date_col` is not found in the DataFrame or is not a date column,
                    or if the `categorical_col` is not found in the DataFrame or is not a categorical column.

    Returns:
        pandas.DataFrame: A new DataFrame containing two columns: the time points from `date_col`, and
                          the corresponding number of unique categories from `categorical_col` at each time point.

    Example:
        # Assuming df is a DataFrame containing columns 'date_column' and 'category_column'
        result_df = get_nb_categories_overtime(df, date_col='date_column', categorical_col='category_column')
        print(result_df)
        
        
            date_column  nb_category_column
         0   2021-01-01                   1
         1   2021-01-02                   2
         2   2021-01-03                   2
         3   2021-01-04                   3
    """

    # Check date_col
    date_columns = get_date_columns(df)
    if date_columns is str:
        date_columns = [date_columns]

    if date_col not in date_columns:
        raise ValueError(date_col+" is not a date column")
    
    # Check categorical_col
    cat_columns = []
    for col in df.columns:
        if is_string_dtype(df[col].dropna()):
            cat_columns.append(col)
    if categorical_col not in cat_columns:
        raise ValueError(categorical_col+" is not a categorical column")
    
    # Check division_col
    if division_col is not None:
        if division_col not in cat_columns:
            raise ValueError(division_col+" is not a categorical column")
    
    if np.issubdtype(df[date_col].dtype, np.object_):
        df[date_col] = pd.to_datetime(df[date_col])
        dates = df[date_col]
    else:
        dates = df[date_col]
    
    periodicity = get_periodicity(df, date_col)[date_col] 
    min_date = min(dates)
    max_date = max(dates)
    

    new_dates = pd.date_range(start=min_date, end=max_date, freq=periodicity)

    if division_col is None:
        new_df = {date_col: new_dates,
                    "nb_"+categorical_col: []}
        
        all_cat = [np.nan]
        counter = 0
        df.set_index(date_col, inplace=True)
        for date in tqdm.tqdm(new_df[date_col]):
            if date in df.index:
                group_cols = df.loc[date][categorical_col]
                if group_cols is str:
                    group_cols = [group_cols]
                for val in set(group_cols):
                    if val not in all_cat: 
                        all_cat.append(val)
                        counter += 1
                new_df["nb_"+categorical_col].append(counter)
            else:
                new_df["nb_"+categorical_col].append(counter)
        return pd.DataFrame(new_df)
    else:
        new_df = pd.DataFrame()
        new_df[date_col] = new_dates
        div_uq_vals =  df[division_col].dropna().unique()
        for date in tqdm.tqdm(new_dates):
            for d_u in div_uq_vals:
                new_df.loc[new_df[date_col]==date, categorical_col+"_"+d_u] = df.loc[(df[date_col]<=date)&(df[division_col]==d_u), categorical_col].nunique()
        return new_df