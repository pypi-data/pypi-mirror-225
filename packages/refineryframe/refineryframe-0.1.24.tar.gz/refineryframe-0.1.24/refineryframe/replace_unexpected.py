"""
replace_unexpected.py - Data Replacement Module

This module contains a function to replace unexpected values in a pandas DataFrame with specified missing types.
It covers various aspects of data validation, including replacing missing values, out-of-range numeric values,
date values outside specified date ranges, and handling character-related issues such as capitalization and Unicode characters.
"""

import logging
from datetime import datetime
import pandas as pd
import numpy as np
from unidecode import unidecode
from refineryframe.other import get_type_dict, treat_unexpected_cond, add_index_to_duplicate_columns
from refineryframe.detect_unexpected import check_duplicate_col_names


####

def replace_unexpected_values(dataframe : pd.DataFrame,
                             MISSING_TYPES : dict = {'date_not_delivered': '1850-01-09',
                                                    'numeric_not_delivered': -999,
                                                    'character_not_delivered': 'missing'},
                             unexpected_exceptions : dict = {"irregular_values": "NONE",
                                                      "date_range": "NONE",
                                                      "numeric_range": "NONE",
                                                      "capitalization": "NONE",
                                                      "unicode_character": "NONE"},
                             unexpected_conditions = None,
                             TEST_RUV_FLAGS_PATH : str = None,
                             earliest_date : str = "1900-08-25",
                             latest_date : str = "2100-01-01",
                             numeric_lower_bound : float = 0,
                             numeric_upper_bound : float = float("inf"),
                            logger : logging.Logger = None) -> dict:

    """
    Replace unexpected values in a pandas DataFrame with missing types.

    Parameters:
    -----------

    dataframe (pandas DataFrame):
        The DataFrame to be checked.
    MISSING_TYPES (dict):
        Dictionary that maps column names to the values considered as missing
        for that column.
    unexpected_exceptions (dict):
        Dictionary that lists column exceptions for each of the \
            following checks: col_names_types, missing_values, missing_types, \
                inf_values, date_format, duplicates, date_range, and numeric_range.
    TEST_DUV_FLAGS_PATH (str):
        Path for checking unexpected values (default is None).
    earliest_date (str):
        The earliest acceptable date (default is "1900-08-25").
    latest_date (str):
        The latest acceptable date (default is "2100-01-01").
    numeric_lower_bound (float):
        The lowest acceptable value for numeric columns (default is 0).
    numeric_upper_bound (float):
        The highest acceptable value for numeric columns
        (default is infinity).

    Returns:
        ruv_score - number between 0 and 1 that means data quality score
    """

    # Create a logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    try:

        dataframe = dataframe.copy()

        # Check of column names are not duplicated

        cdcn_obj = check_duplicate_col_names(dataframe = dataframe,
                                                    throw_error = False,
                                                    logger = logger)


        if not cdcn_obj['COLUMN_NAMES_DUPLICATES_TEST'][-1]:

            dataframe = add_index_to_duplicate_columns(dataframe = dataframe,
                                                        column_name_freq = cdcn_obj['column_name_freq'],
                                                        logger = logger)

        # Separate column names by major types

        column_types = get_type_dict(dataframe,
                                     explicit = False,
                                     stringout = False)

        all_columns = column_types.items()

        index_cols = [k for k, v in all_columns if v == 'index']
        category_cols = [k for k, v in all_columns if v in ['index','category']]
        date_cols = [k for k, v in all_columns if v == 'date']
        numeric_cols = [k for k, v in all_columns if v == 'numeric']

        all_columns = index_cols + category_cols + date_cols + numeric_cols

        # Limit columns based on exceptions

        category_cols_replace_missing_values = [x for x in category_cols
                                    if x not in unexpected_exceptions["irregular_values"]]

        date_cols_replace_missing_values = [x for x in date_cols
                                    if x not in unexpected_exceptions["irregular_values"]]

        numeric_cols_replace_missing_values = [x for x in numeric_cols
                                    if x not in unexpected_exceptions["irregular_values"]]


        cols_replace_date_range = [x for x in date_cols
                                    if x not in unexpected_exceptions["date_range"]]

        cols_replace_numeric_range = [x for x in numeric_cols
                                    if x not in unexpected_exceptions["numeric_range"]]

        cols_replace_character_unicode = [x for x in category_cols
                                    if x not in unexpected_exceptions["unicode_character"]]

        cols_replace_capitalization = [x for x in category_cols
                                    if x not in unexpected_exceptions["capitalization"]]

        # Check if all columns are exceptions

        run_replace_category_missing_values = ((unexpected_exceptions["irregular_values"] != "ALL") & \
            (len(category_cols_replace_missing_values) > 0))

        run_replace_date_missing_values = ((unexpected_exceptions["irregular_values"] != "ALL") & \
            (len(date_cols_replace_missing_values) > 0))

        run_replace_numeric_missing_values = ((unexpected_exceptions["irregular_values"] != "ALL") & \
            (len(numeric_cols_replace_missing_values) > 0))

        run_replace_date_range = (unexpected_exceptions["date_range"] != "ALL") & (len(cols_replace_date_range) > 0)
        run_replace_numeric_range = (unexpected_exceptions["numeric_range"] != "ALL") & (len(cols_replace_numeric_range) > 0)

        run_replace_character_unicode = (unexpected_exceptions["unicode_character"] != "ALL") & (len(cols_replace_character_unicode) > 0)
        run_replace_capitalization = (unexpected_exceptions["capitalization"] != "ALL") & (len(cols_replace_capitalization) > 0)

        if unexpected_conditions:
            run_replace_additional_cons = sum([unexpected_conditions[i]['set'] is not None for i in unexpected_conditions]) > 0
        else:
            run_replace_additional_cons = False

        # Run checks

        if run_replace_category_missing_values:

            logger.debug("=== replacing missing values in category cols with missing types")

            irregular_character_values = ["nan", "inf", "-inf", "None", "", "NaN", "NaT"]

            dataframe[category_cols_replace_missing_values] = (dataframe[category_cols_replace_missing_values]\
                .astype(str).replace(irregular_character_values,
                                    MISSING_TYPES['character_not_delivered']))



        if run_replace_capitalization:

            logger.debug("=== replacing all upper case characters with lower case")

            for col in cols_replace_capitalization:

                dataframe[col] = dataframe[col].astype(str).str.lower()

        if run_replace_character_unicode:

            logger.debug("=== replacing character unicode to latin")

            # Function to replace Latin Unicode characters
            def replace_unicode(text):
                return unidecode(text)

            for col in cols_replace_character_unicode:

                dataframe[col] = dataframe[col].astype(str).apply(replace_unicode)

        if run_replace_additional_cons:

            logger.debug("=== replacing with additional cons")

            conds = [i for i in unexpected_conditions if unexpected_conditions[i]['set'] is not None]

            for cond in conds:

                unexpected_condition = unexpected_conditions[cond]

                dataframe = treat_unexpected_cond(df = dataframe,
                                                  description = unexpected_condition['description'],
                                                  group = unexpected_condition['group'],
                                                  features = unexpected_condition['features'],
                                                  query = unexpected_condition['query'],
                                                  warning = False,
                                                  replace = unexpected_condition['set'],
                                                  logger=logger)



        if run_replace_date_missing_values:

            logger.debug("=== replacing missing values in date cols with missing types")

            irregular_date_values = [pd.NaT]

            dataframe[date_cols_replace_missing_values] = (dataframe[date_cols_replace_missing_values]\
                .replace(irregular_date_values,
                         MISSING_TYPES['date_not_delivered']))


        if run_replace_numeric_missing_values:

            logger.debug("=== replacing missing values in numeric cols with missing types")

            irregular_numeric_values = [np.nan, np.inf, -np.inf, None]

            dataframe[numeric_cols_replace_missing_values] = (dataframe[numeric_cols_replace_missing_values]\
                .replace(irregular_numeric_values,
                         MISSING_TYPES['numeric_not_delivered']))


        if run_replace_date_range:

            logger.debug("=== replacing values outside of expected date range")

            ignore_dates = [v for k, v in MISSING_TYPES.items() if k.startswith("date_")]

            early_dates_list = []
            future_dates_list = []


            for col in cols_replace_date_range:

                ignore_mask = dataframe[col].isin(ignore_dates)

                if earliest_date in cols_replace_date_range:
                    early_dates_list = list((dataframe[col][((dataframe[col] < dataframe[earliest_date]) \
                        & (~ignore_mask))]).astype(str))

                else:
                    early_dates_list = list((dataframe[col][((dataframe[col] < datetime.strptime(earliest_date, "%Y-%m-%d")) \
                        & (~ignore_mask))]).astype(str))


                if latest_date in cols_replace_date_range:
                    future_dates_list = (list((dataframe[col][((dataframe[col] > dataframe[latest_date]) \
                        & (~ignore_mask))]).astype(str)))


                else:
                    future_dates_list = list((dataframe[col][((dataframe[col] > datetime.strptime(latest_date, "%Y-%m-%d")) \
                        & (~ignore_mask))]).astype(str))


                dataframe[col] = dataframe[col].replace(early_dates_list,
                                                        MISSING_TYPES['date_not_delivered'])

                dataframe[col] = dataframe[col].replace(future_dates_list,
                                                        MISSING_TYPES['date_not_delivered'])



        if run_replace_numeric_range:

            logger.debug("=== replacing values outside of expected numeric range")

            ignore_values = [v for k, v in MISSING_TYPES.items() if k.startswith("numeric_")]

            outside_lower_bound_list = []
            outside_upper_bound_list = []

            # Check if all values in each numeric column are within range
            for col in cols_replace_numeric_range:

                if numeric_lower_bound in cols_replace_numeric_range:
                    outside_lower_bound_list = list(dataframe[col][((dataframe[col] < dataframe[numeric_lower_bound]) \
                        & (~dataframe[col].isin(ignore_values)))])
                else:
                    outside_lower_bound_list = list(dataframe[col][((dataframe[col] < numeric_lower_bound) \
                        & (~dataframe[col].isin(ignore_values)))])

                if numeric_upper_bound in cols_replace_numeric_range:
                    outside_upper_bound_list = list(dataframe[col][((dataframe[col] > dataframe[numeric_upper_bound]) \
                        & (~dataframe[col].isin(ignore_values)))])
                else:
                    outside_upper_bound_list = list(dataframe[col][((dataframe[col] > numeric_upper_bound) \
                        & (~dataframe[col].isin(ignore_values)))])

                dataframe[col] = dataframe[col].replace(outside_lower_bound_list,
                                                                      MISSING_TYPES['numeric_not_delivered'])

                dataframe[col] = dataframe[col].replace(outside_upper_bound_list,
                                                                      MISSING_TYPES['numeric_not_delivered'])




        # counting not_delivered instances

        missing_not_delivered_types = ([MISSING_TYPES['date_not_delivered']] \
            + [MISSING_TYPES['numeric_not_delivered']] \
                + [MISSING_TYPES['character_not_delivered']])

        df3 = dataframe.applymap(lambda x: 1 if x in missing_not_delivered_types else 0)
        df4 = dataframe.astype(str).applymap(lambda x: 1 if x in missing_not_delivered_types else 0)
        df5 = df3 + df4 > 0

        col_med = np.median(df5.sum(axis = 0) / df5.shape[0])
        row_med = np.median(df5.sum(axis = 1) / df5.shape[1])

        ruv_score0 = 1 - sum(df5.sum()) / np.prod(df5.shape)
        ruv_score1 = 1 - (col_med + row_med)/2
        ruv_score2 = 1 - (col_med**2 + row_med**2)/2

        logger.debug(f"** Usable values in the dataframe: {ruv_score0*100: .2f}%")
        logger.debug(f"** Uncorrected data quality score: {ruv_score1*100: .2f}%")
        logger.debug(f"** Corrected data quality score: {ruv_score2*100: .2f}%")

        if ruv_score2 < 0.5:
            logger.warning("** Dataframe is completely unusable based on corrected data quality score!")

        if TEST_RUV_FLAGS_PATH is not None:

            with open(TEST_RUV_FLAGS_PATH, "w", encoding="utf8") as f:
                f.write(str(ruv_score2))

    except Exception as e:
        logger.error("Error occured while replacing unexpeted values with missing types!")
        print("The error:", e)

        ruv_score0 = 0
        ruv_score1 = 0
        ruv_score2 = 0

    out_dict = {'dataframe' : dataframe,
                'ruv_score0': ruv_score0,
                'ruv_score1': ruv_score1,
                'ruv_score2': ruv_score2}


    return out_dict
