"""
detect_unexpected.py - Data Quality Checking Module

This module contains functions to detect unexpected values in a pandas DataFrame,
helping to identify potential data quality issues. The functions cover various aspects
of data validation, including checking for missing values, unexpected data types, duplicates,
incorrect date formats, out-of-range numeric values, and date values outside specified date ranges.

Functions:
-----------
1. check_missing_types(dataframe, MISSING_TYPES, independent=True, throw_error, thresholds, logger):
    ...
2. check_missing_values(dataframe, throw_error, thresholds, logger):
    ...
3. check_inf_values(dataframe, independent=True, throw_error, thresholds, logger):
    ...
4. check_date_format(dataframe, expected_date_format='%Y-%m-%d', independent=True, throw_error, thresholds, logger):
    ...
5. check_duplicates(dataframe, subset=None, independent=True, throw_error, thresholds, logger):
    ...
6. check_col_names_types(dataframe, types_dict_str, independent=True, throw_error, thresholds, logger):
    ...
7. check_numeric_range(dataframe, numeric_cols=None, lower_bound=-float('inf'), upper_bound=float('inf'),\
    independent=True, ignore_values=[], throw_error, thresholds, logger):
    ...
8. check_date_range(dataframe, earliest_date='1900-01-01', latest_date='2100-12-31',\
    independent=True, ignore_dates=[], throw_error, thresholds, logger):
    ...
9. check_duplicate_col_names(dataframe, throw_error, logger) -> dict:
    ...
10. detect_unexpected_values(dataframe, MISSING_TYPES, unexpected_exceptions,\
                            unexpected_exceptions_error, unexpected_conditions, thresholds,\
                            ids_for_dedup, TEST_DUV_FLAGS_PATH, types_dict_str,\
                            expected_date_format, earliest_date, latest_date,\
                            numeric_lower_bound, numeric_upper_bound, print_score,\
                            logger) -> dict:
    ...

Note:
-----------
- Some functions use the `logger` parameter for logging warning messages instead of printing.

- Users can specify exceptions for certain checks using the `unexpected_exceptions` dictionary.

- Users can define additional conditions to check for unexpected values using the `unexpected_conditions` dictionary.

- The `thresholds` parameter in the `detect_unexpected_values` function allows users to set threshold scores for different checks.

- Each function returns relevant information about detected issues or scores.

"""



import logging
from datetime import datetime
import pandas as pd
import numpy as np
from refineryframe.other import get_type_dict, treat_unexpected_cond, add_index_to_duplicate_columns

def check_missing_types(dataframe : pd.DataFrame,
                        MISSING_TYPES : dict,
                        independent : bool = True,
                        silent : bool = False,
                        throw_error : bool = False,
                        thresholds : dict = {'numeric_score' : 100,
                                             'date_score' : 100,
                                             'cat_score' : 100},
                        logger : logging.Logger = None) -> dict:

    """
    Checks for instances of missing types in each column of a DataFrame and log warning messages for any found.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to search for missing values.
    MISSING_TYPES : dict
        A dictionary of missing types to search for.
        Keys represent the missing type, and values are the corresponding values to search for.
    independent : bool, optional
        If True, return a boolean indicating whether all checks passed. Default is True.
    silent : bool, optional
        If True, suppress log warnings. Default is False.
    throw_error : bool, optional
        If True, raise an error if issues are found. Default is False.
    thresholds : dict, optional
        Dictionary containing thresholds for numeric_score, date_score, and cat_score.
        Default is {'numeric_score': 100, 'date_score': 100, 'cat_score': 100}.
    logger : logging.Logger, optional
        Logger object for log messages. If not provided, a new logger will be created.

    Returns:
    --------
    bool or dict
        If independent is True, return a boolean indicating whether all checks passed.
        If independent is False, return a dictionary containing scores and checks information.

    Raises:
    -------
    ValueError
        If throw_error is True and missing type checks fail.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        if (not independent) and (not silent):
            logger.debug("=== checking for presence of missing types")

        DATE_MISS_TYPES_TEST_LIST = []
        NUMERIC_MISS_TYPES_TEST_LIST = []
        CHARACTER_MISS_TYPES_TEST_LIST = []

        DATE_MISS_TYPES_SCORE_LIST = [100]
        NUMERIC_MISS_TYPES_SCORE_LIST = [100]
        CHARACTER_MISS_TYPES_SCORE_LIST = [100]

        counts = {}

        for col in dataframe.columns:
            dtype = str(dataframe[col].dtype)

            if dtype.startswith('int') or dtype.startswith('float'):
                for k, v in MISSING_TYPES.items():
                    if (dataframe[col] == v).any():
                    #if v in dataframe[col].values:
                        counts[k] = len(dataframe[dataframe[col] == v])
                        numeric_score = (counts[k]/dataframe.shape[0])*100

                        if (counts[k] > 0) and (not silent):
                            logger.warning(f"Column {col}: ({v}) : {counts[k]} : {numeric_score:.2f}%")

                        NUMERIC_MISS_TYPES_TEST_LIST.append(False)
                        NUMERIC_MISS_TYPES_SCORE_LIST.append(100-numeric_score)

                        if throw_error:
                            raise ValueError("Resolve issues before proceesing any further!")
                    else:
                        NUMERIC_MISS_TYPES_TEST_LIST.append(True)
                        NUMERIC_MISS_TYPES_SCORE_LIST.append(100)

            elif dtype.startswith('datetime') or dtype.startswith('datetime64'):
                for k, v in MISSING_TYPES.items():
                    if pd.to_datetime(v, errors='coerce') is not pd.NaT:
                        if dataframe[col].isin([pd.to_datetime(v, errors='coerce')]).sum() > 0:
                            counts[k] = (dataframe[col] == pd.to_datetime(v, errors='coerce')).sum()
                            date_score = (counts[k]/dataframe.shape[0])*100

                            if (counts[k] > 0) and (not silent):
                                logger.warning(f"Column {col}: ({v}) : {counts[k]} : {date_score:.2f}%")

                            DATE_MISS_TYPES_TEST_LIST.append(False)
                            DATE_MISS_TYPES_SCORE_LIST.append(100-date_score)

                            if throw_error:
                                raise ValueError("Resolve issues before proceesing any further!")
                        else:
                            DATE_MISS_TYPES_TEST_LIST.append(True)
                            DATE_MISS_TYPES_SCORE_LIST.append(100)
                    else:
                        DATE_MISS_TYPES_TEST_LIST.append(True)
                        DATE_MISS_TYPES_SCORE_LIST.append(100)

            elif dtype.startswith('object'):
                for k, v in MISSING_TYPES.items():
                    if dataframe[col].isin([v]).sum() > 0:
                        counts[k] = (dataframe[col] == v).sum()
                        cat_score = (counts[k]/dataframe.shape[0])*100

                        if (counts[k] > 0) and (not silent):
                            logger.warning(f"Column {col}: ({v}) : {counts[k]} : {cat_score:.2f}%")

                        CHARACTER_MISS_TYPES_TEST_LIST.append(False)
                        CHARACTER_MISS_TYPES_SCORE_LIST.append(100-cat_score)

                        if throw_error:
                            raise ValueError("Resolve issues before proceesing any further!")

                    else:
                        CHARACTER_MISS_TYPES_TEST_LIST.append(True)
                        CHARACTER_MISS_TYPES_SCORE_LIST.append(100)

        numeric_score = np.round(np.mean(NUMERIC_MISS_TYPES_SCORE_LIST),2)
        date_score = np.round(np.mean(DATE_MISS_TYPES_SCORE_LIST),2)
        cat_score = np.round(np.mean(CHARACTER_MISS_TYPES_SCORE_LIST),2)


        if numeric_score < thresholds['numeric_score']:

            if not silent:
                logger.warning(f"Numeric score was lower then expected: {numeric_score} < {thresholds['numeric_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")

        if date_score < thresholds['date_score']:

            if not silent:
                logger.warning(f"Date score was lower then expected: {date_score} < {thresholds['date_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")

        if cat_score < thresholds['cat_score']:

            if not silent:
                logger.warning(f"Character score was lower then expected: {cat_score} < {thresholds['cat_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")


    except Exception as e:

        logger.error("Error occured while checking missing types!")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        DATE_MISS_TYPES_TEST_LIST = [False]
        NUMERIC_MISS_TYPES_TEST_LIST = [False]
        CHARACTER_MISS_TYPES_TEST_LIST = [False]

        numeric_score = 0
        date_score = 0
        cat_score = 0

    if independent:

        return all([all(DATE_MISS_TYPES_TEST_LIST),
                    all(NUMERIC_MISS_TYPES_TEST_LIST),
                    all(CHARACTER_MISS_TYPES_TEST_LIST)])
    else:

        output_dict = {'scores': {'cmt_scores': {'numeric_score' : numeric_score,
                                                'date_score' : date_score,
                                                'cat_score' : cat_score}},
                       'checks': (all(DATE_MISS_TYPES_TEST_LIST),
                                  all(NUMERIC_MISS_TYPES_TEST_LIST),
                                  all(CHARACTER_MISS_TYPES_TEST_LIST))}

        return output_dict



def check_missing_values(dataframe : pd.DataFrame,
                         independent : bool = True,
                         silent : bool = False,
                         throw_error : bool = False,
                         thresholds : dict = {'missing_values_score' : 100},
                        logger : logging.Logger = None) -> dict:
    """
    Counts the number of NaN, None, and NaT values in each column of a pandas DataFrame.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to count missing values in.
    independent : bool, optional
        If True, consider only columns with missing values as defined by NaN, None, and NaT.
        If False, count missing values in all columns. Default is True.
    silent : bool, optional
        If True, suppress warning messages. Default is False.
    throw_error : bool, optional
        If True, raise a ValueError for failed missing value checks. Default is False.
    thresholds : dict, optional
        A dictionary containing thresholds for scoring missing value checks.
        Default is {'missing_values_score': 100}.
    logger : logging.Logger, optional
        A logger instance for logging messages. If not provided, a new logger will be created.

    Returns:
    --------
    dict
        A dictionary containing scores and checks for missing value checks.

    Raises:
    -------
    ValueError
        If throw_error is True and missing value checks fail.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        if (not independent) and (not silent):
            logger.debug("=== checking for presence of missing values")

        MISSING_COUNT_TEST = False
        MISSING_COUNT_SCORE_LIST = [100]

        # Define the missing values to check for
        missing_values = [np.nan, None, pd.NaT]

        # Count the number of missing values in each column
        missing_counts = (dataframe.isna() | dataframe.isin(missing_values)).sum()

        missing_counts_filtered = missing_counts[missing_counts > 0]

        if len(missing_counts_filtered) > 0:
            for col, count in zip(missing_counts_filtered.index.to_list(), list(missing_counts_filtered.values)):

                count_score = count/dataframe.shape[0]*100
                if not silent:
                    logger.warning(f"Column {col}: (NA) : {count} : {count_score:.2f}%")

                MISSING_COUNT_SCORE_LIST.append(100-count_score)



            if throw_error:
                    raise ValueError("Resolve issues before proceesing any further!")
        else:
            MISSING_COUNT_TEST = True

        missing_values_score = np.round(np.mean(MISSING_COUNT_SCORE_LIST),2)

        if missing_values_score < thresholds['missing_values_score']:

            if not silent:
                logger.warning(f"Missing values score was lower then expected: {missing_values_score} < {thresholds['missing_values_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")

    except Exception as e:

        logger.error("Error occured while counting missing values!")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        missing_values_score = 0
        MISSING_COUNT_TEST = False

    output_dict = {'scores': {'cmv_scores': {'missing_values_score' : missing_values_score}},
                   'checks': [MISSING_COUNT_TEST]}

    return output_dict



def check_inf_values(dataframe : pd.DataFrame,
                     independent : bool = True,
                     silent : bool = False,
                     throw_error : bool = False,
                     thresholds : dict = {'inf_score' : 100},
                     logger : logging.Logger = None) -> dict:
    """
    Counts the infinite (inf) values in each column of a pandas DataFrame.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to count infinite values in.
    independent : bool, optional
        If True, consider only numeric columns when counting inf values.
        If False, count inf values in all columns. Default is True.
    silent : bool, optional
        If True, suppress warning messages. Default is False.
    throw_error : bool, optional
        If True, raise a ValueError for failed inf value checks. Default is False.
    thresholds : dict, optional
        A dictionary containing thresholds for scoring inf value checks.
        Default is {'inf_score': 100}.
    logger : logging.Logger, optional
        A logger instance for logging messages. If not provided, a new logger will be created.

    Returns:
    --------
    dict
        A dictionary containing scores and checks for inf value checks.

    Raises:
    -------
    ValueError
        If throw_error is True and inf value checks fail.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        if (not independent) and (not silent):
            logger.debug("=== checking for presense of inf values in numeric colums")

        NUM_INF_TEST_LIST = []
        NUM_INF_SCORE_LIST = [100]

        # Count the number of INF values
        for col in dataframe.columns:

            if independent:
                col_missing_counts = sum(dataframe[col].apply(lambda x: np.isinf(x)
                                                              if isinstance(x, (int, float)) else False))
            else:
                col_missing_counts = sum(dataframe[col].apply(lambda x: np.isinf(x)))

            if col_missing_counts > 0:

                inf_score = col_missing_counts/dataframe.shape[0]*100

                if not silent:
                    logger.warning(f"Column {col}: (INF) : {col_missing_counts} : {inf_score:.2f}%")

                NUM_INF_TEST_LIST.append(False)
                NUM_INF_SCORE_LIST.append(100-inf_score)

                if throw_error:
                    raise ValueError("Resolve issues before proceesing any further!")
            else:
                NUM_INF_TEST_LIST.append(True)
                NUM_INF_SCORE_LIST.append(100)

        inf_score = np.round(np.mean(NUM_INF_SCORE_LIST),2)

        if inf_score < thresholds['inf_score']:

            if not silent:
                logger.warning(f"Inf score was lower then expected: {inf_score} < {thresholds['inf_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")

    except Exception as e:
        logger.error("Error occured while checking inf values!")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        NUM_INF_TEST_LIST = [False]
        inf_score = 0

    output_dict = {'scores': {'inf_scores': {'inf_score' : inf_score}},
                   'checks': [all(NUM_INF_TEST_LIST)]}

    return output_dict

def check_date_format(dataframe : pd.DataFrame,
                      expected_date_format : str = '%Y-%m-%d',
                      independent : bool = True,
                      silent : bool = False,
                      throw_error : bool = False,
                      thresholds : dict = {'date_format_score' : 100},
                      logger : logging.Logger = None) -> dict:

    """
    Checks if the values in the datetime columns of the input DataFrame
    have the expected 'YYYY-MM-DD' format.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to be checked for date format.
    expected_date_format : str, optional
        The expected date format. Default is '%Y-%m-%d'.
    independent : bool, optional
        If True, return a Boolean indicating if date format checks passed.
        If False, return a dictionary containing scores and checks. Default is True.
    silent : bool, optional
        If True, suppress warning messages. Default is False.
    throw_error : bool, optional
        If True, raise a ValueError for failed date format checks. Default is False.
    thresholds : dict, optional
        A dictionary containing thresholds for scoring date format checks.
        Default is {'date_format_score': 100}.
    logger : logging.Logger, optional
        A logger instance for logging messages. If not provided, a new logger will be created.

    Returns:
    --------
    bool or dict
        If independent is True, return a Boolean indicating if date format checks passed.
        If independent is False, return a dictionary containing scores and checks.

    Raises:
    -------
    ValueError
        If throw_error is True and date format checks fail.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        if (not independent) and (not silent):
            logger.debug("=== checking propper date format")

        DATE_FORMAT_TEST_LIST = []

        for col in dataframe.columns:
            dtype = str(dataframe[col].dtype)

            if dtype.startswith('datetime'):
                date_vals = pd.to_datetime(dataframe[col],
                                           errors='coerce',
                                           format=expected_date_format).dt.date
                non_date_mask = date_vals.isna()

                if any(non_date_mask):

                    if not silent:
                        logger.warning(f"Column {col} has non-date values or unexpected format.")

                    DATE_FORMAT_TEST_LIST.append(False)

                    if throw_error:
                        raise ValueError("Resolve issues before proceesing any further!")
                else:
                    DATE_FORMAT_TEST_LIST.append(True)

        date_format_score = np.round((sum(DATE_FORMAT_TEST_LIST)/len(DATE_FORMAT_TEST_LIST))*100,2)

        if not independent:
            if any(DATE_FORMAT_TEST_LIST):
                DATE_FORMAT_TEST_LIST = [all(DATE_FORMAT_TEST_LIST)]

        if date_format_score < thresholds['date_format_score']:

            if not silent:
                logger.warning(f"Date format score was lower then expected: {date_format_score} < {thresholds['date_format_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")


    except Exception as e:
        logger.error("Error occurred while checking date format!")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        DATE_FORMAT_TEST_LIST = [False]
        date_format_score = 0


    output_dict = {'scores': {'cdf_scores': {'date_format_score' : date_format_score}},
                                             'checks': [all(DATE_FORMAT_TEST_LIST)]}

    if independent:
        return all(DATE_FORMAT_TEST_LIST)
    else:
        return output_dict


def check_duplicates(dataframe  : pd.DataFrame,
                     subset : list = None,
                     independent : bool = True,
                     silent : bool = False,
                     throw_error : bool = False,
                     thresholds : dict = {'row_dup_score' : 100,
                                          'key_dup_score' : 100},
                    logger : logging.Logger = None) -> dict:
    """
    Checks for duplicates in a pandas DataFrame.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to check for duplicates.
    subset : list of str or None, optional
        A list of column names to consider when identifying duplicates.
        If not specified or None, all columns are used to identify duplicates.
    independent : bool, optional
        If True, return a Boolean indicating if duplicate checks passed.
        If False, return a dictionary containing scores and checks. Default is True.
    silent : bool, optional
        If True, suppress warning messages. Default is False.
    throw_error : bool, optional
        If True, raise a ValueError for failed duplicate checks. Default is False.
    thresholds : dict, optional
        A dictionary containing thresholds for scoring duplicate checks.
        Default is {'row_dup_score': 100, 'key_dup_score': 100}.
    logger : logging.Logger or None, optional
        A logger instance for logging messages. If not provided, a new logger will be created.

    Returns:
    --------
    bool or dict
        If independent is True, return a Boolean indicating if duplicate checks passed.
        If independent is False, return a dictionary containing scores and checks.

    Raises:
    -------
    ValueError
        If throw_error is True and duplicate checks fail.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        if (not independent) and (not silent):
            logger.debug("=== checking for duplicates")

        ROW_DUPLICATES = False

        duplicates = dataframe.duplicated()
        n_duplicates = duplicates.sum()

        if (subset is not None) and (subset != "ALL") and all(col in dataframe.columns for col in subset):
            subset_duplicates = dataframe.duplicated(subset=subset)
            n_subset_duplicates = subset_duplicates.sum()

            if n_subset_duplicates > 0:

                key_dup_score = n_subset_duplicates/dataframe.shape[0]*100

                if not silent:
                    logger.warning(f"There are {n_subset_duplicates} duplicate keys : {key_dup_score:.2f}%")

                n_duplicates = dataframe.drop(columns=subset).duplicated().sum()
                n_true_dup = n_subset_duplicates - n_duplicates

                if n_true_dup > 0:

                    row_dup_score = n_true_dup/dataframe.shape[0]*100

                    if not silent:
                        logger.warning("** Deduplication keys do not form the super key!")
                        logger.warning(f"There are {n_true_dup} duplicates beyond keys : {row_dup_score:.2f}%")

                    if throw_error:
                        raise ValueError("Resolve issues before proceesing any further!")

                    KEY_DUPLICATES = False


                else:
                    ROW_DUPLICATES = False
                    KEY_DUPLICATES = True

                    row_dup_score = n_subset_duplicates/dataframe.shape[0]*100

                    if throw_error:
                        raise ValueError("Resolve issue with row duplicates before proceesing any further!")

            else:
                ROW_DUPLICATES = True
                KEY_DUPLICATES = True

                row_dup_score = 0
                key_dup_score = 0


        else:
            if n_duplicates > 0:

                KEY_DUPLICATES = True

                row_dup_score = n_duplicates/dataframe.shape[0]*100
                key_dup_score = 0

                if not silent:
                    logger.warning(f"There are {n_duplicates} duplicates : {row_dup_score:.2f}%")

                if throw_error:
                    raise ValueError("Resolve issue with row duplicates before proceesing any further!")
            else:
                ROW_DUPLICATES = True
                KEY_DUPLICATES = True

                row_dup_score = 0
                key_dup_score = 0

        row_dup_score = np.round(100 - row_dup_score, 2)
        key_dup_score = np.round(100 - key_dup_score, 2)

        if row_dup_score < thresholds['row_dup_score']:

            if not silent:
                logger.warning(f"Row duplicates score was lower then expected: {row_dup_score} < {thresholds['row_dup_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")

        if key_dup_score < thresholds['key_dup_score']:

            if not silent:
                logger.warning(f"Key duplicates score was lower then expected: {key_dup_score} < {thresholds['key_dup_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")



    except Exception as e:
        logger.error("Error occured while checking duplicates!")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        row_dup_score = 0
        key_dup_score = 0

    output_dict = {'scores': {'dup_scores': {'row_dup_score' : row_dup_score,
                                             'key_dup_score' : key_dup_score}},
                                             'checks': [ROW_DUPLICATES, KEY_DUPLICATES]}


    if independent:
        return all([ROW_DUPLICATES, KEY_DUPLICATES])
    else:
        return output_dict



def check_col_names_types(dataframe : pd.DataFrame,
                          types_dict_str : dict,
                          silent : bool = False,
                          independent : bool = True,
                          throw_error : bool = False,
                          thresholds : dict = {'missing_score' : 100,
                                               'incorrect_dtypes_score' : 100},
                          logger : logging.Logger = None) -> dict:
    """
    Checks if a given DataFrame has the same column names as keys in a provided dictionary
    and if those columns have the same data types as the corresponding values in the dictionary.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to be checked.
    types_dict_str : dict or str
        A dictionary with column names as keys and expected data types as values,
        or a string representation of such a dictionary.
    silent : bool, optional
        If True, suppress warning messages. Default is False.
    independent : bool, optional
        If True, return a Boolean indicating if checks passed. If False, return a dictionary
        containing scores and checks. Default is True.
    throw_error : bool, optional
        If True, raise a ValueError for failed checks. Default is False.
    thresholds : dict, optional
        A dictionary containing thresholds for scoring. Default is {'missing_score': 100, 'incorrect_dtypes_score': 100}.
    logger : logging.Logger, optional
        A logger instance for logging messages. If not provided, a new logger will be created.

    Returns:
    --------
    dict or bool
        If independent is True, return a Boolean indicating if checks passed.
        If independent is False, return a dictionary containing scores and checks.

    Raises:
    -------
    ValueError
        If throw_error is True and any checks fail.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        if (not independent) and (not silent):
            logger.debug(f"=== checking column names and types")

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

        # Calculate missing score
        if dtypes_str_dict == {}:
            missing_score = 100
        else:
            missing_score = np.round((1 - len(missing_cols)/len(set(dtypes_str_dict.keys())))*100,2)

        if missing_cols:

            if not silent:
                logger.warning("** Columns in the dataframe are not the same as in the provided dictionary")
                logger.warning(f"Missing columns: {', '.join(missing_cols)}")

            if throw_error:
                    raise ValueError("Resolve issues before proceesing any further!")
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
                if not silent:
                    logger.warning(f"Column {col}: actual dtype is {actual_dtype}, expected dtype is {expected_dtype}")

            if throw_error:
                    raise ValueError("Resolve issues before proceesing any further!")
        else:
            COL_TYPES_TEST = True


        if dtypes_str_dict == {}:
            incorrect_dtypes_score = 100
        else:
            incorrect_dtypes_score = np.round((1 - len(incorrect_dtypes)/len(set(dtypes_str_dict.keys())))*100,2)

        if missing_score < thresholds['missing_score']:

                if not silent:
                    logger.warning(f"Missing col score was lower then expected: {missing_score} < {thresholds['missing_score']}")

                if throw_error:
                    raise ValueError("Resolve issues before proceesing any further!")


        if incorrect_dtypes_score < thresholds['incorrect_dtypes_score']:

                if not silent:
                    logger.warning(f"Dtypes score was lower then expected: {incorrect_dtypes_score} < {thresholds['incorrect_dtypes_score']}")

                if throw_error:
                    raise ValueError("Resolve issues before proceesing any further!")


    except Exception as e:
        logger.error("Error occured while checking column names and types")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        COL_NAMES_TEST = False
        COL_TYPES_TEST = False

        missing_score = 0
        incorrect_dtypes_score = 0


    if independent:
        return all([COL_NAMES_TEST, COL_TYPES_TEST])
    else:

        output_dict = {'scores': {'ccnt_scores': {'missing_score' : missing_score,
                                              'incorrect_dtypes_score' : incorrect_dtypes_score}},
                       'checks': (COL_NAMES_TEST, COL_TYPES_TEST)}

        return output_dict

def check_numeric_range(dataframe : pd.DataFrame,
                        numeric_cols : list = None,
                        lower_bound : float = -float("inf"),
                        upper_bound : float = float("inf"),
                        independent : bool = True,
                        silent : bool = False,
                        ignore_values : list = [],
                        throw_error : bool = False,
                        thresholds : dict = {'low_numeric_score' : 100,
                                             'upper_numeric_score' : 100},
                        logger : logging.Logger = None) -> dict:
    """
    Checks if numeric values are within expected ranges in each column of a DataFrame.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to check for numeric values.
    numeric_cols : list of str, optional
        A list of column names to consider. If None, all numeric columns are checked.
    lower_bound : float, optional
        The lower bound allowed for numeric values. Default is -infinity.
    upper_bound : float, optional
        The upper bound allowed for numeric values. Default is infinity.
    independent : bool, optional
        If True, return a boolean indicating whether all checks passed. Default is True.
    silent : bool, optional
        If True, suppress log warnings. Default is False.
    ignore_values : list, optional
        A list of values to ignore when checking for values outside the specified range. Default is empty list.
    throw_error : bool, optional
        If True, raise an error if issues are found. Default is False.
    thresholds : dict, optional
        Dictionary containing thresholds for low_numeric_score and upper_numeric_score.
        Default is {'low_numeric_score': 100, 'upper_numeric_score': 100}.
    logger : logging.Logger, optional
        Logger object for log messages. If not provided, a new logger will be created.

    Returns:
    --------
    bool or dict
        If independent is True, return a boolean indicating whether all checks passed.
        If independent is False, return a dictionary containing scores and checks information.

    Raises:
    -------
    ValueError
        If throw_error is True and numeric range checks fail.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        if (not independent) and (not silent):
            logger.debug("=== checking expected numeric range")

        LOW_NUMERIC_TEST_LIST = []
        HIGH_NUMERIC_TEST_LIST = []

        LOW_NUMERIC_SCORES_LIST = [100]
        HIGH_NUMERIC_SCORES_LIST = [100]

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

                low_numeric_score = min_values_n/dataframe.shape[0]*100

                if not silent:
                    logger.warning(f"** Not all values in {col} are higher than {lower_bound}")
                    logger.warning(f"Column {col}: unexpected low values : {min_value} : {low_numeric_score:.2f} %")


                LOW_NUMERIC_TEST_LIST.append(False)
                LOW_NUMERIC_SCORES_LIST.append(100 - low_numeric_score)

                if throw_error:

                    raise ValueError("Resolve issue with numeric values being lower the acceptable lower bound before proceesing any further!")

            else:
                LOW_NUMERIC_TEST_LIST.append(True)
                LOW_NUMERIC_SCORES_LIST.append(100)

            # Check if all values in the column are < upper_bound
            if outside_upper_bound > 0:
                max_values = (dataframe[col] > upper_bound) & (~dataframe[col].isin(ignore_values))

                max_values_n = sum(max_values)
                max_value = max(dataframe[col][max_values])

                upper_numeric_score = max_values_n/dataframe.shape[0]*100

                if not silent:
                    logger.warning(f"** Not all values in {col} are lower than {upper_bound}")
                    logger.warning(f"Column {col}: unexpected high values : {max_value} : {upper_numeric_score:.2f} %")

                HIGH_NUMERIC_TEST_LIST.append(False)
                HIGH_NUMERIC_SCORES_LIST.append(100-upper_numeric_score)

                if throw_error:

                    raise ValueError("Resolve issue with numeric values exceeding upper bound before proceesing any further!")
            else:
                HIGH_NUMERIC_TEST_LIST.append(True)
                HIGH_NUMERIC_SCORES_LIST.append(100)


        low_numeric_score = np.round(np.mean(LOW_NUMERIC_SCORES_LIST),2)
        upper_numeric_score = np.round(np.mean(HIGH_NUMERIC_SCORES_LIST),2)

        if low_numeric_score < thresholds['low_numeric_score']:

            if not silent:
                logger.warning(f"Lower numeric score was lower then expected: {low_numeric_score} < {thresholds['low_numeric_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")

        if upper_numeric_score < thresholds['upper_numeric_score']:

            if not silent:
                logger.warning(f"Upper numeric score was lower then expected: {upper_numeric_score} < {thresholds['upper_numeric_score']}")

            if throw_error:
                raise ValueError("Resolve issues before proceesing any further!")

    except Exception as e:
        logger.error("Error occurred while checking numeric ranges!")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        LOW_NUMERIC_TEST_LIST = [False]
        HIGH_NUMERIC_TEST_LIST = [False]

        low_numeric_score = 0
        upper_numeric_score = 0


    if independent:
        return all([all(LOW_NUMERIC_TEST_LIST), all(HIGH_NUMERIC_TEST_LIST)])
    else:

        output_dict = {'scores': {'cnr_scores': {'low_numeric_score' : low_numeric_score,
                                                'upper_numeric_score' : upper_numeric_score}},
                       'checks': [all(LOW_NUMERIC_TEST_LIST), all(HIGH_NUMERIC_TEST_LIST)]}

        return output_dict


def check_date_range(dataframe : pd.DataFrame,
                     earliest_date : str = "1900-08-25",
                     latest_date : str = "2100-01-01",
                     independent : bool = True,
                     silent : bool = False,
                     ignore_dates : list = [],
                     throw_error : bool = False,
                     thresholds : dict = {'early_dates_score' : 100,
                                          'future_dates_score' : 100},
                    logger : logging.Logger = None) -> dict:
    """
    Checks if date values are within expected date ranges in each column of a DataFrame.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to check for date values.
    earliest_date : str, optional
        The earliest date allowed in the DataFrame. Default is '1900-08-25'.
    latest_date : str, optional
        The latest date allowed in the DataFrame. Default is '2100-01-01'.
    independent : bool, optional
        If True, return a boolean indicating whether all checks passed. Default is True.
    silent : bool, optional
        If True, suppress log warnings. Default is False.
    ignore_dates : list, optional
        A list of dates to ignore when checking for dates outside the specified range. Default is an empty list.
    throw_error : bool, optional
        If True, raise an error if issues are found. Default is False.
    thresholds : dict, optional
        Dictionary containing thresholds for early_dates_score and future_dates_score.
        Default is {'early_dates_score': 100, 'future_dates_score': 100}.
    logger : logging.Logger, optional
        Logger object for log messages. If not provided, a new logger will be created.

    Returns:
    --------
    bool or dict
        If independent is True, return a boolean indicating whether all checks passed.
        If independent is False, return a dictionary containing scores and checks information.

    Raises:
    -------
    ValueError
        If throw_error is True and date range checks fail.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        if (not independent) and (not silent):
            logger.debug("=== checking expected date range")

        ANCIENT_DATE_TEST_LIST = []
        FUTURE_DATE_TEST_LIST = []

        ANCIENT_DATE_SCORES_LIST = [100]
        FUTURE_DATE_SCORES_LIST = [100]

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

                early_dates_score = early_dates/dataframe.shape[0]*100

                if not silent:
                    logger.warning(f"** Not all dates in {col} are later than {earliest_date}")
                    logger.warning(f"Column {col} : ancient date : {early_dates} : {early_dates_score:.2f}%")

                ANCIENT_DATE_TEST_LIST.append(False)
                ANCIENT_DATE_SCORES_LIST.append(100-early_dates_score)

                if throw_error:
                    raise ValueError("Resolve issue with ancient dates before proceesing any further!")
            else:
                ANCIENT_DATE_TEST_LIST.append(True)
                ANCIENT_DATE_SCORES_LIST.append(100)

            # Check if all dates are not later than latest_date
            if future_dates > 0:

                future_dates_score = future_dates/dataframe.shape[0]*100

                if not silent:
                    logger.warning(f"** Not all dates in {col} are later than {latest_date}")
                    logger.warning(f"Column {col} : future date : {future_dates} : {future_dates_score:.2f}%")

                FUTURE_DATE_TEST_LIST.append(False)
                FUTURE_DATE_SCORES_LIST.append(100-future_dates_score)

                if throw_error:
                    raise ValueError("Resolve issue with future dates before proceesing any further!")
            else:
                FUTURE_DATE_TEST_LIST.append(True)
                FUTURE_DATE_SCORES_LIST.append(100)

        early_dates_score = np.round(np.mean(ANCIENT_DATE_SCORES_LIST),2)
        future_dates_score = np.round(np.mean(FUTURE_DATE_SCORES_LIST),2)

        if early_dates_score < thresholds['early_dates_score']:

                if not silent:
                    logger.warning(f"Early dates score was lower then expected: {early_dates_score} < {thresholds['early_dates_score']}")

                if throw_error:
                    raise ValueError("Resolve issues before proceesing any further!")

        if future_dates_score < thresholds['future_dates_score']:

                if not silent:
                    logger.warning(f"Future dates score was lower then expected: {future_dates_score} < {thresholds['future_dates_score']}")

                if throw_error:
                    raise ValueError("Resolve issues before proceesing any further!")

    except Exception as e:
        logger.error("Error occured while checking date ranges!")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        ANCIENT_DATE_TEST_LIST = [False]
        FUTURE_DATE_TEST_LIST = [False]

        early_dates_score = 0
        future_dates_score = 0


    if independent:
        return all([all(ANCIENT_DATE_TEST_LIST), all(FUTURE_DATE_TEST_LIST)])
    else:

        output_dict = {'scores': {'cdr_scores': {'early_dates_score' : early_dates_score,
                                                 'future_dates_score' : future_dates_score}},
                       'checks': [all(ANCIENT_DATE_TEST_LIST), all(FUTURE_DATE_TEST_LIST)]}

        return output_dict

def check_duplicate_col_names(dataframe  : pd.DataFrame,
                              throw_error : bool = False,
                              logger : logging.Logger = None) -> dict:

    """
    Checks for duplicate column names in a pandas DataFrame.

    Parameters:
    -----------
    dataframe : pandas DataFrame
        The DataFrame to check for duplicate column names.
    throw_error : bool, optional
        If True, raise a ValueError when duplicate column names are found.
        If False, print a warning message and continue execution.
        Default is False.
    logger : logging.Logger, optional
        The logger object to use for logging warning and error messages.
        Default is the root logger.

    Returns:
    --------
    dict
        A dictionary containing information about the duplicates.
        'column_name_freq': dict
            A dictionary where keys are duplicate column names, and values are the number of occurrences.
        'COLUMN_NAMES_DUPLICATES_TEST': bool
            True if duplicate column names are found, False otherwise.

    Raises:
    -------
    ValueError
        If throw_error is True and duplicate column names are found.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        dataframe = dataframe.copy()

        dataframe_u_columns = dataframe.columns.unique()

        column_name_freq = {col : pd.DataFrame(dataframe[col]).shape[1] for col in dataframe.columns.unique()}

        if len(dataframe.columns) != len(dataframe_u_columns):

            logger.warning("There are duplicate column names")

            [logger.warning(f"Column {col} : duplicate column names : {n_dup}")  for col,n_dup in column_name_freq.items()]

            if throw_error:

                raise ValueError("Resolve issue with duplicate column names before proceesing any further!")


            COLUMN_NAMES_DUPLICATES_TEST = False

        else:

            COLUMN_NAMES_DUPLICATES_TEST = True

            column_name_freq = None


    except Exception as e:

        logger.error("Error occured while checking duplicates!")

        if throw_error:
            raise e
        else:
            print("The error:", e)

        column_name_freq = {}
        COLUMN_NAMES_DUPLICATES_TEST = False

    return {'column_name_freq' : column_name_freq,
            'COLUMN_NAMES_DUPLICATES_TEST' : [COLUMN_NAMES_DUPLICATES_TEST]}



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
                             unexpected_exceptions_error = {"col_name_duplicates": False,
                                                   "col_names_types": False,
                                                    "missing_values": False,
                                                    "missing_types": False,
                                                    "inf_values": False,
                                                    "date_format": False,
                                                    "duplicates": False,
                                                    "date_range": False,
                                                    "numeric_range": False},
                             unexpected_conditions : dict = None,
                             thresholds : dict = {'cmt_scores' : {'numeric_score' : 100,
                                                                  'date_score' : 100,
                                                                  'cat_score' : 100},
                                                  'cmv_scores' : {'missing_values_score' : 100},
                                                  'ccnt_scores' : {'missing_score' : 100,
                                                                   'incorrect_dtypes_score' : 100},
                                                  'inf_scores' : {'inf_score' : 100},
                                                  'cdf_scores' : {'date_format_score' : 100},
                                                  'dup_scores' : {'row_dup_score' : 100,
                                                                  'key_dup_score' : 100},
                                                  'cnr_scores' : {'low_numeric_score' : 100,
                                                                  'upper_numeric_score' : 100},
                                                  'cdr_scores' : {'early_dates_score' : 100,
                                                                  'future_dates_score' : 100}},
                             ids_for_dedup : list = None,
                             TEST_DUV_FLAGS_PATH : str = None,
                             types_dict_str : dict = None,
                             expected_date_format : str = '%Y-%m-%d',
                             earliest_date : str = "1900-08-25",
                             latest_date : str = "2100-01-01",
                             numeric_lower_bound : float = 0,
                             numeric_upper_bound : float = float("inf"),
                             print_score : bool = True,
                            logger : logging.Logger = None) -> dict:

    """
    Detects unexpected values in a pandas DataFrame.

    Parameters:
    -----------
    dataframe (pandas DataFrame): The DataFrame to be checked.
    MISSING_TYPES (dict): Dictionary that maps column names to the values considered as missing
                         for that column.
    unexpected_exceptions (dict): Dictionary that lists column exceptions for each of the
                                 following checks: col_names_types, missing_values, missing_types,
                                 inf_values, date_format, duplicates, date_range, and numeric_range.
    unexpected_exceptions_error (dict): Dictionary indicating whether to throw errors for each type of unexpected exception.
    unexpected_conditions (dict): Dictionary containing additional conditions to check for unexpected values.
    thresholds (dict): Dictionary containing threshold scores for different checks.
    ids_for_dedup (list): List of columns to identify duplicates (default is None).
    TEST_DUV_FLAGS_PATH (str): Path for checking unexpected values (default is None).
    types_dict_str (str): String that describes the expected types of the columns (default is None).
    expected_date_format (str): The expected date format (default is '%Y-%m-%d').
    earliest_date (str): The earliest acceptable date (default is "1900-08-25").
    latest_date (str): The latest acceptable date (default is "2100-01-01").
    numeric_lower_bound (float): The lowest acceptable value for numeric columns (default is 0).
    numeric_upper_bound (float): The highest acceptable value for numeric columns (default is infinity).
    print_score (bool): Whether to print the duv score (default is True).
    logger (logging.Logger): Logger object for logging messages (default is logging).

    Returns:
    -------
    dict:
        duv_score (float): Number between 0 and 1 representing the percentage of passed tests.
        check_scores (dict): Scores for each check.
        unexpected_exceptions_scaned (dict): Unexpected exceptions based on detected unexpected values.

    Raises:
    -------
    Exception:
        If any errors occur during the detection process.
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        dataframe = dataframe.copy()

        # Checks for duv score
        checks_list = []

        # Check scores dict
        check_score_dict = {}

        # Check of column names are not duplicated

        logger.debug("=== checking for column name duplicates")

        cdcn_obj = check_duplicate_col_names(dataframe = dataframe,
                                                    throw_error = unexpected_exceptions_error['col_name_duplicates'],
                                                    logger = logger)

        checks_list.extend(cdcn_obj['COLUMN_NAMES_DUPLICATES_TEST'])



        if not checks_list[-1]:

            dataframe = add_index_to_duplicate_columns(dataframe = dataframe,
                                                        column_name_freq = cdcn_obj['column_name_freq'],
                                                        logger = logger)

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

        run_silent_check_missing_types = (unexpected_exceptions["missing_types"] != "IGNORE") & (len(cols_check_missing_types) > 0)
        run_silent_check_missing_values = (unexpected_exceptions["missing_values"] != "IGNORE") & (len(cols_check_missing_values) > 0)
        run_silent_check_duplicates = (unexpected_exceptions["duplicates"] != "IGNORE") & (len(cols_check_duplicates) > 0)
        run_silent_check_col_names_types = (unexpected_exceptions["col_names_types"] != "IGNORE") \
            & (types_dict_str is not None) \
                & (len(cols_check_col_names_types) > 0)
        run_silent_check_date_format = (unexpected_exceptions["date_format"] != "IGNORE") & (len(cols_check_date_format) > 0)
        run_silent_check_date_range = (unexpected_exceptions["date_range"] != "IGNORE") & (len(cols_check_date_range) > 0)
        run_silent_check_inf_values = (unexpected_exceptions["inf_values"] != "IGNORE") & (len(cols_check_inf_values) > 0)
        run_silent_check_numeric_range = (unexpected_exceptions["numeric_range"] != "IGNORE") & (len(cols_check_numeric_range) > 0)

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

        ##
        if run_silent_check_col_names_types:

            ccnt_obj = check_col_names_types(dataframe = dataframe[cols_check_col_names_types],
                                                       types_dict_str = types_dict_str,
                                                       independent = False,
                                                       silent = not run_check_col_names_types,
                                                       throw_error = unexpected_exceptions_error['col_names_types'],
                                                       thresholds = thresholds['ccnt_scores'],
                                                       logger = logger)

            check_score_dict.update(ccnt_obj['scores'])


        if run_check_col_names_types:

            checks_list.extend(ccnt_obj['checks'])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["col_names_types"] = "ALL"
        ##
        if run_silent_check_missing_values:

            cmv_obj = check_missing_values(dataframe = dataframe[cols_check_missing_values],
                                                     independent = False,
                                                     silent = not run_check_missing_values,
                                                     throw_error = unexpected_exceptions_error['missing_values'],
                                                     thresholds = thresholds['cmv_scores'],
                                                     logger = logger)

            check_score_dict.update(cmv_obj['scores'])

        if run_check_missing_values:

            checks_list.extend(cmv_obj['checks'])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["missing_values"] = "ALL"
        ##
        if run_silent_check_missing_types:

            cmt_obj = check_missing_types(dataframe = dataframe[cols_check_missing_types],
                                                    MISSING_TYPES = MISSING_TYPES,
                                                    independent = False,
                                                    silent = not run_check_missing_types,
                                                    throw_error = unexpected_exceptions_error['missing_types'],
                                                    thresholds = thresholds['cmt_scores'],
                                                    logger = logger)

            check_score_dict.update(cmt_obj['scores'])

        if run_check_missing_types:

            checks_list.extend(cmt_obj['checks'])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["missing_types"] = "ALL"
        ##

        if run_silent_check_date_format:

            cdf_obj = check_date_format(dataframe = dataframe[cols_check_date_format],
                                                  expected_date_format = expected_date_format,
                                                  independent = False,
                                                  silent = not run_check_date_format,
                                                  throw_error = unexpected_exceptions_error['date_format'],
                                                  thresholds = thresholds['cdf_scores'],
                                                  logger = logger)

            check_score_dict.update(cdf_obj['scores'])

        if run_check_date_format:

            checks_list.extend(cdf_obj['checks'])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["date_format"] = "ALL"

        ##

        if run_silent_check_date_range:

            cdr_obj = check_date_range(dataframe = dataframe[cols_check_date_range],
                                                 earliest_date = earliest_date,
                                                 latest_date = latest_date,
                                                 independent = False,
                                                 silent = not run_check_date_range,
                                                 ignore_dates = [v for k, v in MISSING_TYPES.items()
                                                                 if k.startswith("date_")],
                                                 throw_error = unexpected_exceptions_error['date_range'],
                                                 thresholds = thresholds['cdr_scores'],
                                                 logger = logger)

            check_score_dict.update(cdr_obj['scores'])

        if run_check_date_range:

            checks_list.extend(cdr_obj['checks'])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["date_range"] = "ALL"
        ##

        if run_silent_check_duplicates:

            dup_obj = check_duplicates(dataframe = dataframe[cols_check_duplicates],
                                                subset = ids_for_dedup,
                                                independent = False,
                                                silent = not run_check_duplicates,
                                                throw_error = unexpected_exceptions_error['duplicates'],
                                                thresholds = thresholds['dup_scores'],
                                                logger = logger)

            check_score_dict.update(dup_obj['scores'])

        if run_check_duplicates:

            checks_list.extend(dup_obj['checks'])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["duplicates"] = "ALL"
        ##

        if run_silent_check_inf_values:

            inf_obj = check_inf_values(dataframe = dataframe[cols_check_inf_values],
                                       independent = False,
                                       silent = not run_check_inf_values,
                                       throw_error = unexpected_exceptions_error['inf_values'],
                                       thresholds = thresholds['inf_scores'],
                                       logger = logger)

            check_score_dict.update(inf_obj['scores'])

        if run_check_inf_values:

            checks_list.extend(inf_obj['checks'])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["inf_values"] = "ALL"

        ##

        if run_silent_check_numeric_range:

            cnr_obj = check_numeric_range(dataframe = dataframe[cols_check_numeric_range],
                                                    lower_bound = numeric_lower_bound,
                                                    upper_bound = numeric_upper_bound,
                                                    independent = False,
                                                    silent = not run_check_numeric_range,
                                                    ignore_values = [v for k, v in MISSING_TYPES.items()
                                                                     if k.startswith("numeric_")],
                                                    throw_error = unexpected_exceptions_error['numeric_range'],
                                                    thresholds = thresholds['cnr_scores'],
                                                    logger = logger)

            check_score_dict.update(cnr_obj['scores'])

        if run_check_numeric_range:

            checks_list.extend(cnr_obj['checks'])

            if not checks_list[-1]:
                unexpected_exceptions_scaned["numeric_range"] = "ALL"

        ##

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
                    'check_scores' : check_score_dict,
                    'unexpected_exceptions_scaned' : unexpected_exceptions_scaned}


    except Exception as e:
        logger.error("Error occured during duv score calculation!")
        print("The error:", e)
