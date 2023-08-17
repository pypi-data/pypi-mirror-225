import pandas as pd
import numpy as np
import tqdm
import datetime
import os
from dateutil.parser import parse
from .reader import read_data

    
def is_date(string):
    """
    Return whether the string can be interpreted as a date.

    Parameters:
        string (str): string to check for date
    """

    try:
        if type(string) is not str:
            return False
        parse(string, fuzzy=False)
        return True

    except ValueError:
        return False

def filter_date_only(serie):
    """
    
    """
    filter_dates_only = serie[serie.apply(lambda x: isinstance(x, datetime.datetime) or is_date(x))] 

    filter_dates_only = pd.Series(filter_dates_only.unique()) 

    if np.issubdtype(filter_dates_only.dtype, np.object_):
        try:
            filter_dates_only = pd.to_datetime(filter_dates_only)
        except:
            pass
        
    filter_dates_only = filter_dates_only.sort_values()

    return filter_dates_only

def get_date_columns(df):
    """
    Description
        Automatically determine the date column(s) in the DataFrame.

        The function analyzes the DataFrame columns and attempts to identify the column(s)
        containing date or datetime information. It returns either the name of the single
        date column as a string or a list of column names if multiple date columns are found.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be analyzed.

    Returns:
        Union[str, List[str]]: The name of the date column as a string if only one
        date column is found. If multiple date columns are detected, it returns a
        list of strings containing the names of all identified date columns.

    Raises:
        ValueError: If no date columns are found in the DataFrame.

    Example:
        >>> import pandas as pd
        >>> data = {
        ...     'Date': ['2023-07-01', '2023-07-02', '2023-07-03'],
        ...     'Temperature': [30, 32, 31],
        ...     'Humidity': [60, 65, 70],
        ... }
        >>> df = pd.DataFrame(data)
        >>> get_date_columns(df)
        'Date'

        >>> data = {
        ...     'Start_Date': ['2023-07-01', '2023-07-02', '2023-07-03'],
        ...     'End_Date': ['2023-07-05', '2023-07-06', '2023-07-07'],
        ... }
        >>> df = pd.DataFrame(data)
        >>> get_date_columns(df)
        ['Start_Date', 'End_Date']
    """
         
    # Result list
    date_columns = []
    
    NUMBER_OF_ROWS = df.shape[0]

    NUMBER_ROW_TO_CHECK = min(1000,NUMBER_OF_ROWS)
                    
    for column in df.columns:
        if np.issubdtype(df[column].dtype, np.datetime64):
            date_columns.append(column)
            continue
        elif np.issubdtype(df[column].dtype, np.object_):
            counter = 0
            index_range = np.random.choice(list(df.index),NUMBER_ROW_TO_CHECK,replace=False)
            for index in index_range:
                value = df[column][index]
                try:
                    pd.to_datetime(value)
                    counter += 1
                except:
                    continue
            
            if counter >= int(NUMBER_ROW_TO_CHECK * 0.50):
                date_columns.append(column)

    if len(date_columns) == 0:
        raise ValueError("No date columns found in the DataFrame.")
    if len(date_columns) == 1:
        return date_columns[0]
    else:
        return date_columns
        
def get_periodicity(df, *columns):
    """
    Description
        Determine the periodicity of the given DataFrame or specified columns.

        The function analyzes the DataFrame or specified columns and attempts to identify
        the data's periodicity, such as daily ('D'), weekly on Monday ('W-MON') or Saturday ('W-SAT'),
        or monthly ('M'). The function calculates the time interval between consecutive
        data points in the specified columns and returns the most likely periodicity based
        on the time differences.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be analyzed.
        *columns (str, optional): Names of the columns to consider when determining the periodicity.
                                If not provided, the entire DataFrame will be analyzed.

    Returns:
        dict: The periodicity identified in the DataFrame or specified columns.
            The returned value will be one of the following strings: 'D', 'W-MON', 'W-SAT', or 'M'.

    Raises:
        ValueError: If the specified column(s) do not exist in the DataFrame.

    Example:
        >>> import pandas as pd
        >>> data = {
        ...     'Date': ['2023-07-01', '2023-07-02', '2023-07-03'],
        ...     'Temperature': [30, 32, 31],
        ... }
        >>> df = pd.DataFrame(data)
        >>> get_periodicity(df, 'Date')
        {'Date': 'D'}

        >>> data = {
        ...     'Date': ['2023-07-01', '2023-07-08', '2023-07-15'],
        ...     'Temperature': [30, 32, 31],
        ... }
        >>> df = pd.DataFrame(data)
        >>> get_periodicity(df, 'Date')
        {'Date': 'W-SAT'}
    """

    if columns:
        for col in columns:
            if col not in df.columns:
                raise ValueError("The specified column(s) do not exist in the DataFrame.")
    else:
        columns = get_date_columns(df)
        if type(columns) is str:
            columns = [columns]

    periodicity = {} # Result variable

    for col in columns:
        col_serie = df[col]
            
        filter_dates_only = filter_date_only(col_serie)
        
        if filter_dates_only.size < 1000:
            range_slice = int(filter_dates_only.size / 3)
        else:
            range_slice = 333 
            
        periodicity_paterns = []
        start = 0
        len_to_check = 3
        for index in range(range_slice):
            try:
                periodicity_paterns.append(pd.infer_freq(filter_dates_only[start:start + len_to_check]))
            except:
                pass
            start += len_to_check
        
        if len(periodicity_paterns) > 0:
            periodicity[col] = max(set(periodicity_paterns), key = periodicity_paterns.count)
        else:
            periodicity[col] = 'None'

    return periodicity

def date_summary(path):
    """
    Description
        Generate a data frame summarizing the date-related information for each CSV, XLS, or XLSX file in the given path.

        Parameters:
        path (str): The directory path containing CSV, XLS, or XLSX files.

    Returns:
    pandas.DataFrame: A data frame with the following columns:
        - file_name (str): The name of the file.
        - date_columns (str): The column name that contain date-related data.
        - periodicity (str): The frequency of the date-related data (e.g., 'daily', 'monthly', 'yearly').
        - start_date : The earliest date found in the date-related columns.
        - end_date : The latest date found in the date-related columns.
        - prop_null % : The proportion of missing values (NaNs) in the date-related columns.
    Note:
       This function will only consider CSV, XLS, and XLSX files in the specified path.

    Example:
        >>> print(date_summary('.'))
          file_name date_columns periodicity  start_date    end_date  prop_null %
        0  data.csv        Date       daily  2023-07-01  2023-07-03          0.0
    """

    if os.path.isdir(path):
        for (dirpath, dirnames, filenames) in os.walk(path):
            break
    else:
        filenames = [os.path.basename(path).split('/')[-1]]

    new_df = {'file_name': [],
              'date_columns': [],
              'periodicity': [],
              'start_date': [],
              'end_date': [],
              'prop_null%': []
            }

    for file in tqdm.tqdm(filenames):
        try:
            if os.path.isdir(path):
                df = read_data(path+'/'+file)
            else:
                df = read_data(path)
        except Exception as e:
            print(e, file)
            continue  
        
        try:
            columns = get_date_columns(df)
        except Exception as e:
            print(e, file)
            continue
        
        if type(columns) is str:
            columns = [columns]

        #periodicity = get_periodicity(df)
        for col in columns:
            new_df['file_name'].append(file)
            new_df['date_columns'].append(col)
            new_df['periodicity'].append(get_periodicity(df,col)[col])
            col_serie = df[col]
            
            if np.issubdtype(df[col].dtype, np.object_):
                col_serie = col_serie[col_serie.apply(lambda x: isinstance(x, datetime.datetime) or is_date(x))]
                #col_serie = col_serie.astype('datetime64[ns]')
                col_serie = pd.to_datetime(pd.Series(col_serie), errors = 'coerce')
            
            new_df['prop_null%'].append("{:.2f}".format((1 - (col_serie.count() / df.shape[0])) * 100))
            try:
                new_df['start_date'].append(min(col_serie)._date_repr)
                new_df['end_date'].append(max(col_serie)._date_repr)
            except:
                new_df['start_date'].append('None')
                new_df['end_date'].append('None')

    return pd.DataFrame(new_df)

