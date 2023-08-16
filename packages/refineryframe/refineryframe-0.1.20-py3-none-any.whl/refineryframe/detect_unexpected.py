"""
detect_unexpected.py - Data Quality Checking Module

This module contains functions to detect unexpected values in a pandas DataFrame,
helping to identify potential data quality issues. The functions cover various aspects
of data validation, including checking for missing values, unexpected data types, duplicates,
incorrect date formats, out-of-range numeric values, and date values outside specified date ranges.

Functions:
1. check_missing_types(dataframe, MISSING_TYPES, independent=True, logger=logging):
    Check for instances of missing types in each column of the DataFrame.
    Logs warning messages if any missing values are found.

2. check_missing_values(dataframe, logger=logging):
    Count the number of NaN, None, and NaT values in each column of the DataFrame.
    Logs warning messages if any missing values are found.

3. check_inf_values(dataframe, independent=True, logger=logging):
    Count the infinite (INF) values in each numeric column of the DataFrame.
    Logs warning messages if any INF values are found.

4. check_date_format(dataframe, expected_date_format='%Y-%m-%d', independent=True, logger=logging):
    Check if the values in datetime columns of the DataFrame have the expected format.
    Logs warning messages for columns with non-date values or unexpected date formats.

5. check_duplicates(dataframe, subset=None, independent=True, logger=logging):
    Check for duplicates in the DataFrame.
    Logs warning messages if any duplicates are found based on specified columns.

6. check_col_names_types(dataframe, types_dict_str, independent=True, logger=logging):
    Check if the DataFrame has the same column names as specified in the dictionary
    and if those columns have the expected data types as values in the dictionary.
    Logs warning messages for columns with incorrect names or data types.

7. check_numeric_range(dataframe, numeric_cols=None, lower_bound=-float('inf'),
                       upper_bound=float('inf'), independent=True, ignore_values=[],
                       logger=logging):
    Check if numeric values in the DataFrame are within specified ranges.
    Logs warning messages for numeric values outside the specified range.

8. check_date_range(dataframe, earliest_date='1900-01-01', latest_date='2100-12-31',
                    independent=True, ignore_dates=[], logger=logging):
    Check if date values in the DataFrame are within specified date ranges.
    Logs warning messages for date values outside the specified range.

9. detect_unexpected_values(dataframe, MISSING_TYPES=MISSING_TYPES,
                            unexpected_exceptions={"col_names_types": "NONE",
                                                  "missing_values": "NONE",
                                                  "missing_types": "NONE",
                                                  "inf_values": "NONE",
                                                  "date_format": "NONE",
                                                  "duplicates": "NONE",
                                                  "date_range": "NONE",
                                                  "numeric_range": "NONE"},
                            unexpected_conditions=None, ids_for_dup=None,
                            TEST_DUV_FLAGS_PATH=None, types_dict_str=None,
                            expected_date_format='%Y-%m-%d',
                            earliest_date='1900-01-01', latest_date='2100-12-31',
                            numeric_lower_bound=0, numeric_upper_bound=float('inf'),
                            print_score=True, logger=logging):
    Detect unexpected values in a pandas DataFrame by running a series of data quality checks.
    The function returns the "duv_score," representing the percentage of passed tests.

Note:
- Some functions use the `logger` parameter for logging warning messages instead of printing.
- Users can specify exceptions for certain checks using the `unexpected_exceptions` dictionary.
- Users can define additional conditions to check for unexpected values using the `unexpected_conditions` dictionary.

"""

import logging
from datetime import datetime
import pandas as pd
import numpy as np
from refineryframe.other import get_type_dict, treat_unexpected_cond

def check_missing_types(dataframe : pd.DataFrame,
                        MISSING_TYPES : dict,
                        independent : bool = True,
                        logger : logging.Logger = logging):

    """
    The function takes a DataFrame and a dictionary of missing types as input, and
    searches for any instances of these missing types in each column of the DataFrame.
    If any instances are found, a warning message is logged containing the column name,
    the missing value, and the count of missing values found.

    Parameters
    ----------
    dataframe : pandas DataFrame
                The DataFrame to search for missing values.
    MISSING_TYPES : dict
        A dictionary of missing types to search for. The keys represent the missing type
        and the values are the corresponding values to search for.

    Returns
    -------
    None
        The function does not return anything, but logs a warning message for each
        instance of a missing value found in the DataFrame.
    """

    try:

        DATE_MISS_TYPES_TEST_LIST = []
        NUMERIC_MISS_TYPES_TEST_LIST = []
        CHARACTER_MISS_TYPES_TEST_LIST = []

        counts = {}
        for col in dataframe.columns:
            dtype = str(dataframe[col].dtype)

            if dtype.startswith('int') or dtype.startswith('float'):
                for k, v in MISSING_TYPES.items():
                    if (dataframe[col] == v).any():
                    #if v in dataframe[col].values:
                        counts[k] = len(dataframe[dataframe[col] == v])
                        if counts[k] > 0:
                            logger.warning(f"Column {col}: ({v}) : {counts[k]} : {(counts[k]/dataframe.shape[0])*100:.2f}%")

                        NUMERIC_MISS_TYPES_TEST_LIST.append(False)
                    else:
                        NUMERIC_MISS_TYPES_TEST_LIST.append(True)
            elif dtype.startswith('datetime') or dtype.startswith('datetime64'):
                for k, v in MISSING_TYPES.items():
                    if pd.to_datetime(v, errors='coerce') is not pd.NaT:
                        if dataframe[col].isin([pd.to_datetime(v, errors='coerce')]).sum() > 0:
                            counts[k] = (dataframe[col] == pd.to_datetime(v, errors='coerce')).sum()
                            if counts[k] > 0:
                                logger.warning(f"Column {col}: ({v}) : {counts[k]} : {(counts[k]/dataframe.shape[0])*100:.2f}%")
                            DATE_MISS_TYPES_TEST_LIST.append(False)
                        else:
                            DATE_MISS_TYPES_TEST_LIST.append(True)
                    else:
                        DATE_MISS_TYPES_TEST_LIST.append(True)

            elif dtype.startswith('object'):
                for k, v in MISSING_TYPES.items():
                    if dataframe[col].isin([v]).sum() > 0:
                        counts[k] = (dataframe[col] == v).sum()
                        if counts[k] > 0:
                            logger.warning(f"Column {col}: ({v}) : {counts[k]} : {(counts[k]/dataframe.shape[0])*100:.2f}%")
                        CHARACTER_MISS_TYPES_TEST_LIST.append(False)

                    else:
                        CHARACTER_MISS_TYPES_TEST_LIST.append(True)
    except Exception as e:

        logger.error("Error occured while checking missing types!")
        print("The error:", e)
        DATE_MISS_TYPES_TEST_LIST = [False]
        NUMERIC_MISS_TYPES_TEST_LIST = [False]
        CHARACTER_MISS_TYPES_TEST_LIST = [False]

    if independent:

        return all([all(DATE_MISS_TYPES_TEST_LIST),
                    all(NUMERIC_MISS_TYPES_TEST_LIST),
                    all(CHARACTER_MISS_TYPES_TEST_LIST)])
    else:
        return (all(DATE_MISS_TYPES_TEST_LIST),
               all(NUMERIC_MISS_TYPES_TEST_LIST),
               all(CHARACTER_MISS_TYPES_TEST_LIST))



def check_missing_values(dataframe : pd.DataFrame,
                        logger : logging.Logger = logging):
    """
    Count the number of NaN, None, and NaT values in each column of a pandas DataFrame.

    Parameters
    ----------
    dataframe : pandas DataFrame
                The DataFrame to count missing values in.

    Returns
    -------
    None
    """

    try:

        MISSING_COUNT_TEST = False

        # Define the missing values to check for
        missing_values = [np.nan, None, pd.NaT]

        # Count the number of missing values in each column
        missing_counts = (dataframe.isna() | dataframe.isin(missing_values)).sum()

        missing_counts_filtered = missing_counts[missing_counts > 0]

        if len(missing_counts_filtered) > 0:
            for col, count in zip(missing_counts_filtered.index.to_list(), list(missing_counts_filtered.values)):
                logger.warning(f"Column {col}: (NA) : {count} : {count/dataframe.shape[0]*100:.2f}%")
        else:
            MISSING_COUNT_TEST = True

    except Exception as e:

        logger.error("Error occured while counting missing values!")
        print("The error:", e)

    return MISSING_COUNT_TEST



def check_inf_values(dataframe : pd.DataFrame,
                     independent : bool = True,
                     logger : logging.Logger = logging):
    """
    Count the inf values in each column of a pandas DataFrame.

    Parameters
    ----------
    dataframe : pandas DataFrame
                The DataFrame to count inf values in.

    Returns
    -------
    None
    """

    try:

        NUM_INF_TEST_LIST = []

        # Count the number of INF values
        for col in dataframe.columns:

            if independent:

                col_missing_counts = sum(dataframe[col].apply(lambda x: np.isinf(x)
                                                              if isinstance(x, (int, float)) else False))
            else:

                col_missing_counts = sum(dataframe[col].apply(lambda x: np.isinf(x)))

            if col_missing_counts > 0:
                logger.warning(f"Column {col}: (INF) : {col_missing_counts} : {col_missing_counts/dataframe.shape[0]*100:.2f}%")
                NUM_INF_TEST_LIST.append(False)
            else:
                NUM_INF_TEST_LIST.append(True)
    except Exception as e:
        logger.error("Error occured while checking inf values!")
        print("The error:", e)
        NUM_INF_TEST_LIST = [False]

    return all(NUM_INF_TEST_LIST)

def check_date_format(dataframe : pd.DataFrame,
                      expected_date_format : str = '%Y-%m-%d',
                      independent : bool = True,
                      logger : logging.Logger = logging) -> bool:

    """
    Check if the values in the datetime columns of the input dataframe
    have the expected 'YYYY-MM-DD' format.

    Parameters:
    -----------
    dataframe: pandas.DataFrame
        The dataframe to be checked for date format.

    Returns:
    --------
    None
    """

    try:

        DATE_FORMAT_TEST_LIST = []

        for col in dataframe.columns:
            dtype = str(dataframe[col].dtype)

            if dtype.startswith('date'):
                date_vals = dataframe[col].astype(str).apply(lambda x: datetime.strptime(x, expected_date_format).date()
                                                      if x != 'NaT' else None)
                if any(date_vals.isna()):
                    logger.warning(f"Column {col} has non-date values or unexpected format.")
                    DATE_FORMAT_TEST_LIST.append(False)
                else:
                    DATE_FORMAT_TEST_LIST.append(True)

    except Exception as e:
        logger.error("Error occured while checking date format!")
        print("The error:", e)
        DATE_FORMAT_TEST_LIST = [False]

    return all(DATE_FORMAT_TEST_LIST)



def check_duplicates(dataframe  : pd.DataFrame,
                     subset : list = None,
                     independent : bool = True,
                    logger : logging.Logger = logging) -> bool:
    """
    Check for duplicates in a pandas DataFrame.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to check for duplicates.
    subset : list of str, optional
        A list of column names to consider when identifying duplicates.
        If not specified, all columnsare used to identify duplicates.

    Returns:
    --------
    int
        The number of duplicates found.
    """

    try:

        ROW_DUPLICATES = False
        KEY_DUPLICATES = False

        duplicates = dataframe.duplicated()
        n_duplicates = duplicates.sum()

        if (subset is not None) and (subset != "ALL") and (subset in list(dataframe.columns)):
            subset_duplicates = dataframe.duplicated(subset=subset)
            n_subset_duplicates = subset_duplicates.sum()

            if n_subset_duplicates > 0:
                logger.warning(f"There are {n_subset_duplicates} duplicate keys : {n_subset_duplicates/dataframe.shape[0]*100:.2f}%")

                n_true_dup = n_subset_duplicates - n_duplicates

                if n_true_dup > 0 & n_duplicates > 0:

                    logger.warning("** Deduplication keys do not form the super key!")
                    logger.warning(f"There are {n_true_dup} duplicates beyond keys : {n_true_dup/dataframe.shape[0]*100:.2f}%")
                else:
                    ROW_DUPLICATES = False
                    KEY_DUPLICATES = True

            else:
                ROW_DUPLICATES = True
                KEY_DUPLICATES = True
        else:
            if n_duplicates > 0:
                logger.warning(f"There are {n_duplicates} duplicates : {n_duplicates/dataframe.shape[0]*100:.2f}%")
            else:
                ROW_DUPLICATES = True
                KEY_DUPLICATES = True

    except Exception as e:
        logger.error("Error occured while checking duplicates!")
        print("The error:", e)


    if independent:
        return all([ROW_DUPLICATES, KEY_DUPLICATES])
    else:
        return ROW_DUPLICATES, KEY_DUPLICATES



def check_col_names_types(dataframe : pd.DataFrame,
                          types_dict_str : dict,
                          independent : bool = True,
                          logger : logging.Logger = logging) -> bool:
    """
    Checks if a given dataframe has the same column names as keys in a given dictionary
    and those columns have the same types as items in the dictionary.

    Args:
    - dataframe: pandas DataFrame
    - column_dict: dictionary with column names as keys and expected data types as values

    Returns:
    - Boolean indicating whether the dataframe has the same columns and types as specified in the dictionary
    """

    try:

        if isinstance(types_dict_str, str):

            # Convert the string representation to a dictionary
            dtypes_dict = eval(types_dict_str)

            # Convert the data type objects to string representations
            dtypes_str_dict = {col: str(dtype) for col, dtype in dtypes_dict.items()}

        else:

            dtypes_str_dict = types_dict_str

        COL_NAMES_TEST = False
        COL_TYPES_TEST = False

        # Check if dataframe has all the columns in the dictionary
        missing_cols = set(dtypes_str_dict.keys()) - set(dataframe.columns)
        if missing_cols:
            logger.warning("** Columns in the dataframe are not the same as in the provided dictionary")
            logger.warning(f"Missing columns: {', '.join(missing_cols)}")
        else:
            COL_NAMES_TEST = True

        # Check if data types of columns in the dataframe match the expected data types in the dictionary
        incorrect_dtypes = []
        for col, dtype in dtypes_str_dict.items():
            if dataframe[col].dtype.name != dtype:
                incorrect_dtypes.append((col, dataframe[col].dtype.name, dtype))
        if incorrect_dtypes:
            logger.warning("Incorrect data types:")
            for col, actual_dtype, expected_dtype in incorrect_dtypes:
                logger.warning(f"Column {col}: actual dtype is {actual_dtype}, expected dtype is {expected_dtype}")
        else:
            COL_TYPES_TEST = True


    except Exception as e:
        logger.error("Error occured while checking column names and types")
        print("The error:", e)
        COL_NAMES_TEST = False
        COL_TYPES_TEST = False


    if independent:
        return all([COL_NAMES_TEST, COL_TYPES_TEST])
    else:
        return COL_NAMES_TEST, COL_TYPES_TEST

def check_numeric_range(dataframe : pd.DataFrame,
                        numeric_cols : list = None,
                        lower_bound : float = -float("inf"),
                        upper_bound : float = float("inf"),
                        independent : bool = True,
                        ignore_values : list = [],
                        logger : logging.Logger = logging) -> bool:
    """
    Check if numeric values are in expected ranges

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to check for numeric values.
    lower_bound : float, optional
        The lower bound allowed for numeric values. Defaults to -infinity.
    upper_bound : float, optional
        The upper bound allowed for numeric values. Defaults to infinity.
    independent : bool, optional
        Whether to check the range of each column independently or not. Defaults to True.
    ignore_values : list, optional
        A list of values to ignore when checking for values outside the specified range. Defaults to empty list.

    Returns:
    --------
    bool or tuple
        Returns True if all numeric values in the DataFrame are within the specified range, False otherwise.
        If `independent` is False, returns a tuple of two bools, the first indicating
            if all lower bounds are met and the second if all upper bounds are met.
    """

    try:

        LOW_NUMERIC_TEST_LIST = []
        HIGH_NUMERIC_TEST_LIST = []

        if independent:
            # Select only numeric columns
            if numeric_cols is None:
                numeric_cols = dataframe.select_dtypes(include=['float', 'int']).columns
        else:
            numeric_cols = dataframe.columns

        # Check if all values in each numeric column are within range
        for col in numeric_cols:
            #outside_lower_bound = (dataframe[col] < lower_bound).sum()
            #outside_upper_bound = (dataframe[col] > upper_bound).sum()

            outside_lower_bound = ((dataframe[col] < lower_bound) & (~dataframe[col].isin(ignore_values))).sum()
            outside_upper_bound = ((dataframe[col] > upper_bound) & (~dataframe[col].isin(ignore_values))).sum()


            # Check if all values in the column are > lower_bound
            if outside_lower_bound > 0:

                min_values = (dataframe[col] < lower_bound) & (~dataframe[col].isin(ignore_values))

                min_values_n = sum(min_values)

                min_value = min(dataframe[col][min_values])

                logger.warning(f"** Not all values in {col} are higher than {lower_bound}")
                logger.warning(f"Column {col}: unexpected low values : {min_value} : {min_values_n/dataframe.shape[0]*100:.2f} %")
                LOW_NUMERIC_TEST_LIST.append(False)
            else:
                LOW_NUMERIC_TEST_LIST.append(True)

            # Check if all values in the column are < upper_bound
            if outside_upper_bound > 0:
                max_values = (dataframe[col] > upper_bound) & (~dataframe[col].isin(ignore_values))

                max_vales_n = sum(max_values)

                max_value = max(dataframe[col][max_values])
                logger.warning(f"** Not all values in {col} are lower than {upper_bound}")
                logger.warning(f"Column {col}: unexpected high values : {max_value} : {max_values_n/dataframe.shape[0]*100:.2f} %")
                HIGH_NUMERIC_TEST_LIST.append(False)
            else:
                HIGH_NUMERIC_TEST_LIST.append(True)

    except Exception as e:
        logger.error("Error occurred while checking numeric ranges!")
        logger.error(f"The error: {e}")
        LOW_NUMERIC_TEST_LIST = [False]
        HIGH_NUMERIC_TEST_LIST = [False]


    if independent:
        return all([all(LOW_NUMERIC_TEST_LIST), all(HIGH_NUMERIC_TEST_LIST)])
    else:
        return all(LOW_NUMERIC_TEST_LIST), all(HIGH_NUMERIC_TEST_LIST)


def check_date_range(dataframe : pd.DataFrame,
                     earliest_date : str = "1900-08-25",
                     latest_date : str = "2100-01-01",
                     independent : bool = True,
                     ignore_dates : list = [],
                    logger : logging.Logger = logging) -> bool:
    """
    Check if dates are in expected ranges

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to check for dates.
    earliest_date : str, optional
        The earliest date allowed in the DataFrame. Defaults to '1900-08-25'.
    latest_date : str, optional
        The latest date allowed in the DataFrame. Defaults to '2100-01-01'.

    Returns:
    --------
    None
        This function does not return anything, but logs warning messages if any dates are outside
        the specified range.
    """

    try:

        ANCIENT_DATE_TEST_LIST = []
        FUTURE_DATE_TEST_LIST = []

        if independent:
            df = dataframe.select_dtypes(include=['datetime']).columns
        else:
            df = dataframe.columns



        for col in df:

            ignore_mask = dataframe[col].isin(ignore_dates)

            if sum(df == earliest_date):
                early_dates = ((dataframe[col] < dataframe[earliest_date]) & (~ignore_mask)).sum()
            else:
                early_dates = ((dataframe[col] < datetime.strptime(earliest_date, "%Y-%m-%d")) & (~ignore_mask)).sum()

            if sum(df == latest_date):
                future_dates = ((dataframe[col] > dataframe[latest_date]) & (~ignore_mask)).sum()
            else:
                future_dates = ((dataframe[col] > datetime.strptime(latest_date, "%Y-%m-%d")) & (~ignore_mask)).sum()

            # Check if all dates are later than earliest_date
            if early_dates > 0:
                logger.warning(f"** Not all dates in {col} are later than {earliest_date}")
                logger.warning(f"Column {col} : ancient date : {early_dates} : {early_dates/dataframe.shape[0]*100:.2f}%")
                ANCIENT_DATE_TEST_LIST.append(False)
            else:
                ANCIENT_DATE_TEST_LIST.append(True)

            # Check if all dates are not later than latest_date
            if future_dates > 0:

                logger.warning(f"** Not all dates in {col} are later than {latest_date}")
                logger.warning(f"Column {col} : future date : {future_dates} : {future_dates/dataframe.shape[0]*100:.2f}%")
                FUTURE_DATE_TEST_LIST.append(False)
            else:
                FUTURE_DATE_TEST_LIST.append(True)

    except Exception as e:
        logger.error("Error occured while checking date ranges!")
        print("The error:", e)
        ANCIENT_DATE_TEST_LIST = [False]
        FUTURE_DATE_TEST_LIST = [False]

    if independent:
        return all([all(ANCIENT_DATE_TEST_LIST), all(FUTURE_DATE_TEST_LIST)])
    else:
        return (all(ANCIENT_DATE_TEST_LIST), all(FUTURE_DATE_TEST_LIST))


def detect_unexpected_values(dataframe : pd.DataFrame,
                             MISSING_TYPES : dict = {'date_not_delivered': '1850-01-09',
                                                    'numeric_not_delivered': -999,
                                                    'character_not_delivered': 'missing'},
                             unexpected_exceptions : dict = {"col_names_types": "NONE",
                                                      "missing_values": "NONE",
                                                      "missing_types": "NONE",
                                                      "inf_values": "NONE",
                                                      "date_format": "NONE",
                                                      "duplicates": "NONE",
                                                      "date_range": "NONE",
                                                      "numeric_range": "NONE"},
                             unexpected_conditions : dict = None,
                             ids_for_dedup : list = None,
                             TEST_DUV_FLAGS_PATH : str = None,
                             types_dict_str : dict = None,
                             expected_date_format : str = '%Y-%m-%d',
                             earliest_date : str = "1900-08-25",
                             latest_date : str = "2100-01-01",
                             numeric_lower_bound : float = 0,
                             numeric_upper_bound : float = float("inf"),
                             print_score : bool = True,
                            logger : logging.Logger = logging) -> dict:

    """
    Detect unexpected values in a pandas DataFrame.

    Parameters:
    -----------

    dataframe (pandas DataFrame): The DataFrame to be checked.
    MISSING_TYPES (dict): Dictionary that maps column names to the values considered as missing
                              for that column.
    unexpected_exceptions (dict): Dictionary that lists column exceptions for each of the
                                      following checks: col_names_types, missing_values, missing_types,
                                      inf_values, date_format, duplicates, date_range, and numeric_range.
    ids_for_dedup (list): List of columns to identify duplicates (default is None).
    TEST_DUV_FLAGS_PATH (str): Path for checking unexpected values (default is None).
    types_dict_str (str): String that describes the expected types of the columns (default is None).
    expected_date_format (str): The expected date format (default is '%Y-%m-%d').
    earliest_date (str): The earliest acceptable date (default is "1900-08-25").
    latest_date (str): The latest acceptable date (default is "2100-01-01").
    numeric_lower_bound (float): The lowest acceptable value for numeric columns (default is 0).
    numeric_upper_bound (float): The highest acceptable value for numeric columns
                                    (default is infinity).

    Returns:
        duv_score (float) - number between 0 and 1 that means what percentage of tests have passed
        unexpected_exceptions_scaned - unexpected_exceptions based on detected unexpected values
    """


    try:


        # Separate column names by major types

        column_types = get_type_dict(dataframe,
                                     explicit = False,
                                     stringout = False)

        all_columns = column_types.items()

        index_cols = [k for k, v in all_columns if v == 'index']
        category_cols = [k for k, v in all_columns if v == 'category']
        date_cols = [k for k, v in all_columns if v == 'date']
        numeric_cols = [k for k, v in all_columns if v == 'numeric']

        all_columns = index_cols + category_cols + date_cols + numeric_cols

        # Limit columns based on exceptions

        cols_check_missing_types = [x for x in all_columns
                                    if x not in unexpected_exceptions["missing_types"]]
        cols_check_missing_values = [x for x in all_columns
                                    if x not in unexpected_exceptions["missing_values"]]
        cols_check_duplicates = [x for x in all_columns
                                    if x not in unexpected_exceptions["duplicates"]]
        cols_check_col_names_types = [x for x in all_columns
                                    if x not in unexpected_exceptions["col_names_types"]]
        cols_check_date_format = [x for x in date_cols
                                    if x not in unexpected_exceptions["date_format"]]
        cols_check_date_range = [x for x in date_cols
                                    if x not in unexpected_exceptions["date_range"]]
        cols_check_inf_values = [x for x in numeric_cols
                                    if x not in unexpected_exceptions["inf_values"]]
        cols_check_numeric_range = [x for x in numeric_cols
                                    if x not in unexpected_exceptions["numeric_range"]]


        # Check if all columns are exceptions

        run_check_missing_types = (unexpected_exceptions["missing_types"] != "ALL") & (len(cols_check_missing_types) > 0)
        run_check_missing_values = (unexpected_exceptions["missing_values"] != "ALL") & (len(cols_check_missing_values) > 0)
        run_check_duplicates = (unexpected_exceptions["duplicates"] != "ALL") & (len(cols_check_duplicates) > 0)
        run_check_col_names_types = (unexpected_exceptions["col_names_types"] != "ALL") \
            & (types_dict_str is not None) \
                & (len(cols_check_col_names_types) > 0)
        run_check_date_format = (unexpected_exceptions["date_format"] != "ALL") & (len(cols_check_date_format) > 0)
        run_check_date_range = (unexpected_exceptions["date_range"] != "ALL") & (len(cols_check_date_range) > 0)
        run_check_inf_values = (unexpected_exceptions["inf_values"] != "ALL") & (len(cols_check_inf_values) > 0)
        run_check_numeric_range = (unexpected_exceptions["numeric_range"] != "ALL") & (len(cols_check_numeric_range) > 0)

        if unexpected_conditions:
            run_check_additional_cons = sum([unexpected_conditions[i]['warning'] for i in unexpected_conditions]) > 0
        else:
            run_check_additional_cons = False


        if ((ids_for_dedup is None) or (ids_for_dedup == "ALL")):

            if (len(index_cols) > 0) and (list(index_cols) in list(dataframe.columns)):
                ids_for_dedup = list(index_cols)
            else:
                ids_for_dedup = list(dataframe.columns)


        # Checks scan
        unexpected_exceptions_scaned = {
            "col_names_types": "NONE",
            "missing_values": "NONE",
            "missing_types": "NONE",
            "inf_values": "NONE",
            "date_format": "NONE",
            "duplicates": "NONE",
            "date_range": "NONE",
            "numeric_range": "NONE"
        }

        # Run checks
        checks_list = []


        if run_check_col_names_types:

            logger.debug(f"=== checking column names and types")

            checks_list.extend(check_col_names_types(dataframe = dataframe[cols_check_col_names_types],
                                                       types_dict_str = types_dict_str,
                                                       independent = False,
                                                       logger = logger))

            if not checks_list[-1]:
                unexpected_exceptions_scaned["col_names_types"] = "ALL"

        if run_check_missing_values:

            logger.debug("=== checking for presence of missing values")

            checks_list.extend([check_missing_values(dataframe = dataframe[cols_check_missing_values],
                                                     logger = logger)])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["missing_values"] = "ALL"

        if run_check_missing_types:

            logger.debug("=== checking for presence of missing types")

            checks_list.extend(check_missing_types(dataframe = dataframe[cols_check_missing_types],
                                                    MISSING_TYPES = MISSING_TYPES,
                                                    independent = False,
                                                    logger = logger))

            if not checks_list[-1]:
                unexpected_exceptions_scaned["missing_types"] = "ALL"

        if run_check_date_format:

            logger.debug("=== checking propper date format")

            checks_list.extend([check_date_format(dataframe = dataframe[cols_check_date_format],
                                                  expected_date_format = expected_date_format,
                                                  independent = False,
                                                  logger = logger)])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["date_format"] = "ALL"


        if run_check_date_range:

            logger.debug("=== checking expected date range")

            checks_list.extend(check_date_range(dataframe = dataframe[cols_check_date_range],
                                                 earliest_date = earliest_date,
                                                 latest_date = latest_date,
                                                 independent = False,
                                                 ignore_dates = [v for k, v in MISSING_TYPES.items()
                                                                 if k.startswith("date_")],
                                                 logger = logger))

            if not checks_list[-1]:
                unexpected_exceptions_scaned["date_range"] = "ALL"

        if run_check_duplicates:

            logger.debug("=== checking for duplicates")

            checks_list.extend(check_duplicates(dataframe = dataframe[cols_check_duplicates],
                             subset = ids_for_dedup,
                             independent = False,
                             logger = logger))

            if not checks_list[-1]:
                unexpected_exceptions_scaned["duplicates"] = "ALL"


        if run_check_inf_values:

            logger.debug("=== checking for presense of inf values in numeric colums")

            checks_list.extend([check_inf_values(dataframe = dataframe[cols_check_inf_values],
                                                 independent = False,
                                                 logger = logger)])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["inf_values"] = "ALL"

        if run_check_numeric_range:

            logger.debug("=== checking expected numeric range")

            checks_list.extend(check_numeric_range(dataframe = dataframe[cols_check_numeric_range],
                                                    lower_bound = numeric_lower_bound,
                                                    upper_bound = numeric_upper_bound,
                                                    independent = False,
                                                    ignore_values = [v for k, v in MISSING_TYPES.items()
                                                                     if k.startswith("numeric_")],
                                                    logger = logger))

            if not checks_list[-1]:
                unexpected_exceptions_scaned["numeric_range"] = "ALL"


        if run_check_additional_cons:

            logger.debug("=== checking additional cons")

            conds = [i for i in unexpected_conditions if unexpected_conditions[i]['warning']]

            for cond in conds:

                unexpected_condition = unexpected_conditions[cond]

                treat_unexpected_cond(df = dataframe,
                                      description = unexpected_condition['description'],
                                      group = unexpected_condition['group'],
                                      features = unexpected_condition['features'],
                                      query = unexpected_condition['query'],
                                      warning = unexpected_condition['warning'],
                                      replace = None,
                                      logger=logger)



        duv_score = sum(checks_list)/max(len(checks_list),1)

        if print_score and duv_score != 1:

            logger.warning(f"Percentage of passed tests: {(duv_score) * 100:.2f}%")

        if TEST_DUV_FLAGS_PATH is not None:

            with open(TEST_DUV_FLAGS_PATH, "w", encoding="utf8") as f:
                f.write(str(duv_score))

        else:

            return {'duv_score' : duv_score,
                    'unexpected_exceptions_scaned' : unexpected_exceptions_scaned}


    except Exception as e:
        logger.error("Error occured during duv score calculation!")
        print("The error:", e)
