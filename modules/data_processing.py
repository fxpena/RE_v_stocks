import os 
import pandas as pd

from datetime import datetime


def load_state_data(directory):
    """
    Load and merge state house price index (HPI) data from CSV files in the 
    specified directory.

    Parameters:
    directory (str): Path to the directory containing state HPI CSV files.

    Returns:
    pd.DataFrame: HPI data for all states. Index is datetime.
    """
    frames = []
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(directory, file), index_col=0)
            frames.append(df)
    merged = pd.concat(frames, axis=1)
    merged.index = pd.to_datetime(merged.index)

    merged.columns = merged.columns.str.replace('STHPI','', regex=True).str.strip()
    return merged


def total_return(df, start_date, final_date):
    """ 
    Calculate the annualized total return for each column in the DataFrame
    between start_date and final_date.

    Parameters:
    df (pd.DataFrame): DataFrame with datetime index and columns representing 
        different investments.
    start_date (str or datetime): Start date for the return calculation.
    final_date (str or datetime): End date for the return calculation.

    Returns:
    pd.Series: Annualized total return for each investment. 
        If dates are invalid, returns -1.
    """
    if not(isinstance(start_date, datetime)): 
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            return -1
    if not(isinstance(final_date, datetime)):
        if isinstance(final_date, str):
            final_date = datetime.strptime(final_date, '%Y-%m-%d')
        else:
            return -1

    # swap dates if in wrong order    
    if start_date > final_date:
        start_date, final_date = final_date, start_date
    
    num_years = (final_date - start_date).days / 365.25

    # select the closest rows to the given dates
    start_val = df[df.index >= start_date].iloc[0]
    stop_val = df[df.index >= final_date].iloc[0]
    # calculate total return and annualize it
    changes = (stop_val - start_val) / start_val
    changes = changes.squeeze(axis=0) * 100 / num_years

    changes.sort_values(inplace=True, ascending=False)
    return changes