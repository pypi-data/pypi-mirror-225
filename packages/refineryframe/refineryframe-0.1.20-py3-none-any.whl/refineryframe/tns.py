"""
This module contains test and safeguards for DS pipeline.

Classes:

Refiner - combines funtions below

Functions:

- get_type_dict(dataframe,
                explicit=False,
                stringout=True): returns a string representation of a dictionary
                                 containing the data types of each column in the
                                 given DataFrame
- set_types(dataframe,
            types_dict_str,
            replace_dict = None): change the data types of the columns in the
                                  given DataFrame based on a dictionary of
                                  intended data types. Returns the DataFrame
                                  with the changed data types.
...

- detect_unexpected_values(dataframe,
                             MISSING_TYPES,
                             unexpected_exceptions = {"col_names_types": "NONE",
                                                      "missing_values": "NONE",
                                                      "missing_types": "NONE",
                                                      "inf_values": "NONE",
                                                      "date_format": "NONE",
                                                      "duplicates": "NONE",
                                                      "date_range": "NONE",
                                                      "numeric_range": "NONE"},
                             ids_for_dup = None,
                             TEST_DUV_FLAGS_PATH = None,
                             types_dict_str = None,
                             expected_date_format = '%Y-%m-%d',
                             earliest_date = "1900-08-25",
                             latest_date = "2100-01-01",
                             numeric_lower_bound = 0,
                             numeric_upper_bound = float("inf")):
                               Detect unexpected values in a pandas DataFrame.

"""

import logging
from datetime import datetime
import pandas as pd
import numpy as np
from unidecode import unidecode
import re
import attr


# Default missing data types

MISSING_TYPES = {'date_not_delivered': '1850-01-09',
                 'numeric_not_delivered': -999,
                 'character_not_delivered': 'missing'}

@attr.s
class Refiner:

    """
    Refiner is a class that encapsulates funtions from refineframe.
    """


    # inputs
    dataframe = attr.ib(type=pd.DataFrame)
    replace_dict = attr.ib(default=None, type=dict)

    # inputs with defaults
    MISSING_TYPES = attr.ib(default=MISSING_TYPES, type=dict)
    expected_date_format = attr.ib(default='%Y-%m-%d', type=str)
    mess = attr.ib(default="INITIAL PREPROCESSING", type=str)
    shout_type = attr.ib(default="HEAD2", type=str)

    logger = attr.ib(default=logging)
    logger_name = attr.ib(default='Refiner')
    loggerLvl = attr.ib(default=logging.INFO)
    dotline_length = attr.ib(default=50, type=int)

    lower_bound = attr.ib(default=-float("inf"))
    upper_bound = attr.ib(default=float("inf"))
    earliest_date = attr.ib(default="1900-08-25")
    latest_date = attr.ib(default="2100-01-01")

    unexpected_exceptions_duv = attr.ib(default={"col_names_types": "NONE",
                                              "missing_values": "NONE",
                                              "missing_types": "NONE",
                                              "inf_values": "NONE",
                                              "date_format": "NONE",
                                              "duplicates": "NONE",
                                              "date_range": "NONE",
                                              "numeric_range": "NONE"}, type=dict)

    unexpected_exceptions_ruv = attr.ib(default={"irregular_values": "NONE",
                                                      "date_range": "NONE",
                                                      "numeric_range": "NONE",
                                                      "capitalization": "NONE",
                                                      "unicode_character": "NONE"}, type=dict)

    unexpected_conditions = attr.ib(default=None)

    ignore_values = attr.ib(default=[])
    ignore_dates = attr.ib(default=[])

    # outputs
    type_dict = attr.ib(default={}, init = False, type=dict)

    MISSING_TYPES_TEST = attr.ib(default=None, init = False)
    MISSING_COUNT_TEST = attr.ib(default=None, init = False)
    NUM_INF_TEST = attr.ib(default=None, init = False)
    DATE_FORMAT_TEST = attr.ib(default=None, init = False)
    DUPLICATES_TEST = attr.ib(default=None, init = False)
    COL_NAMES_TYPES_TEST = attr.ib(default=None, init = False)
    NUMERIC_RANGE_TEST = attr.ib(default=None, init = False)

    duv_score = attr.ib(default=None, init = False)
    ruv_score0 = attr.ib(default=None, init = False)
    ruv_score1 = attr.ib(default=None, init = False)
    ruv_score2 = attr.ib(default=None, init = False)

    def __attrs_post_init__(self):
        self.initialize_logger()

    def initialize_logger(self):

        logging.basicConfig(level=self.loggerLvl)
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.loggerLvl)

        self.logger = logger


    def shout(self):

        """
        Print a line of text with a specified length and format.
        """

        shoutOUT(type=self.shout_type,
                 mess=self.mess,
                 dotline_length=self.dotline_length,
                 logger=self.logger)

    def get_type_dict_from_dataframe(self,
                      explicit=True,
                      stringout=False):

        """
        Returns a string representation of a dictionary containing the data types
        of each column in the given pandas DataFrame.

        Numeric columns will have type 'numeric', date columns will have type 'date',
        character columns will have type 'category', and columns containing 'id' at
        the beginning or end of their name will have type 'index'.
        """

        type_dict = get_type_dict(dataframe=self.dataframe,
                                       explicit=explicit,
                                       stringout=stringout)

        return type_dict

    def set_type_dict(self,
                      type_dict=None,
                      explicit=True,
                      stringout=False):

        """
        Change the data types of the columns in the given DataFrame
        based on a dictionary of intended data types.
        """

        if type_dict is None:
            type_dict = get_type_dict(dataframe=self.dataframe,
                                       explicit=explicit,
                                       stringout=stringout,
                                      logger = self.logger)

        self.type_dict = type_dict


    def set_types(self,
                  type_dict=None,
                  replace_dict=None,
                  expected_date_format=None):

        """
        Change the data types of the columns in the given DataFrame
        based on a dictionary of intended data types.
        """

        if type_dict is None:
            type_dict = self.type_dict
        if replace_dict is None:
            replace_dict = self.replace_dict
        if expected_date_format is None:
            expected_date_format = self.expected_date_format

        self.dataframe = set_types(dataframe=self.dataframe,
                                  types_dict_str=type_dict,
                                  replace_dict=replace_dict,
                                  expected_date_format=expected_date_format,
                                      logger = self.logger)

    def check_missing_types(self):

        """
        The function takes a DataFrame and a dictionary of missing types as input, and
        searches for any instances of these missing types in each column of the DataFrame.
        If any instances are found, a warning message is logged containing the column name,
        the missing value, and the count of missing values found.
        """

        self.MISSING_TYPES_TEST = check_missing_types(dataframe = self.dataframe,
                                                        MISSING_TYPES = self.MISSING_TYPES,
                                                        independent = True,
                                      logger = self.logger)

    def check_missing_values(self):

        """
        Count the number of NaN, None, and NaT values in each column of a pandas DataFrame.
        """

        self.MISSING_COUNT_TEST = check_missing_values(dataframe = self.dataframe,
                                      logger = self.logger)

    def check_inf_values(self):

        """
        Count the inf values in each column of a pandas DataFrame.
        """

        self.NUM_INF_TEST = check_inf_values(dataframe = self.dataframe,
                                             independent = True,
                                             logger = self.logger)

    def check_date_format(self):

        """
        Check if the values in the datetime columns of the input dataframe
        have the expected 'YYYY-MM-DD' format.
        """

        self.DATE_FORMAT_TEST = check_date_format(dataframe = self.dataframe,
                                                  expected_date_format = self.expected_date_format,
                                                  independent = True,
                                                  logger = self.logger)

    def check_duplicates(self,
                         subset = None):

        """
        Check for duplicates in a pandas DataFrame.
        """

        self.DUPLICATES_TEST = check_duplicates(dataframe = self.dataframe,
                                                 subset = subset,
                                                 independent = True,
                                                 logger = self.logger)

    def check_col_names_types(self):

        """
        Checks if a given dataframe has the same column names as keys in a given dictionary
        and those columns have the same types as items in the dictionary.
        """

        self.COL_NAMES_TYPES_TEST = check_col_names_types(dataframe = self.dataframe,
                          types_dict_str = self.type_dict,
                          independent = True,
                                      logger = self.logger)

    def check_numeric_range(self,
                            numeric_cols = None,
                            lower_bound = None,
                            upper_bound = None,
                            ignore_values = None):

        """
        Check if numeric values are in expected ranges
        """

        if lower_bound is None:
            lower_bound = self.lower_bound
        if upper_bound is None:
            upper_bound = self.upper_bound
        if ignore_values is None:
            ignore_values = self.ignore_values

        self.NUMERIC_RANGE_TEST = check_numeric_range(dataframe = self.dataframe,
                                                      numeric_cols = numeric_cols,
                                                      lower_bound = lower_bound,
                                                      upper_bound = upper_bound,
                                                      independent = True,
                                                      ignore_values = ignore_values,
                                                      logger = self.logger)

    def check_date_range(self,
                        earliest_date = None,
                        latest_date = None,
                        ignore_dates = None):

        """
        Check if dates are in expected ranges
        """

        if earliest_date is None:
            earliest_date = self.earliest_date
        if latest_date is None:
            latest_date = self.latest_date
        if ignore_dates is None:
            ignore_dates = self.ignore_dates

        self.DATE_RANGE_TEST = check_date_range(dataframe = self.dataframe,
                                                 earliest_date = earliest_date,
                                                 latest_date = latest_date,
                                                 independent = True,
                                                 ignore_dates = ignore_dates,
                                                logger = self.logger)

    def detect_unexpected_values(self,
                                 MISSING_TYPES = None,
                                 unexpected_exceptions = None,
                                 unexpected_conditions = None,
                                 ids_for_dup = None,
                                 TEST_DUV_FLAGS_PATH = None,
                                 types_dict_str = None,
                                 expected_date_format = None,
                                 earliest_date = None,
                                 latest_date = None,
                                 numeric_lower_bound = None,
                                 numeric_upper_bound = None,
                                 print_score = True):

        """
        Detect unexpected values in a pandas DataFrame.
        """

        if MISSING_TYPES is None:
            MISSING_TYPES = self.MISSING_TYPES
        if unexpected_exceptions is None:
            unexpected_exceptions = self.unexpected_exceptions_duv
        if unexpected_conditions is None:
            unexpected_conditions = self.unexpected_conditions
        if types_dict_str is None:
            types_dict_str = self.type_dict
        if expected_date_format is None:
            expected_date_format = self.expected_date_format
        if earliest_date is None:
            earliest_date = self.earliest_date
        if latest_date is None:
            latest_date = self.latest_date
        if numeric_lower_bound is None:
            numeric_lower_bound = self.lower_bound
        if numeric_upper_bound is None:
            numeric_upper_bound = self.upper_bound

        self.duv_score = detect_unexpected_values(dataframe = self.dataframe,
                                                 MISSING_TYPES = MISSING_TYPES,
                                                 unexpected_exceptions = unexpected_exceptions,
                                                 unexpected_conditions = unexpected_conditions,
                                                 ids_for_dup = ids_for_dup,
                                                 TEST_DUV_FLAGS_PATH = TEST_DUV_FLAGS_PATH,
                                                 types_dict_str = types_dict_str,
                                                 expected_date_format = expected_date_format,
                                                 earliest_date = earliest_date,
                                                 latest_date = latest_date,
                                                 numeric_lower_bound = numeric_lower_bound,
                                                 numeric_upper_bound = numeric_upper_bound,
                                                 print_score = print_score,
                                      logger = self.logger)

    def replace_unexpected_values(self,
                             MISSING_TYPES = None,
                             unexpected_exceptions = None,
                             unexpected_conditions = None,
                             TEST_RUV_FLAGS_PATH = None,
                             earliest_date = None,
                             latest_date = None,
                             numeric_lower_bound = None,
                             numeric_upper_bound = None):

        """
        Replace unexpected values in a pandas DataFrame with missing types.
        """

        if MISSING_TYPES is None:
            MISSING_TYPES = self.MISSING_TYPES
        if unexpected_exceptions is None:
            unexpected_exceptions = self.unexpected_exceptions_ruv
        if unexpected_conditions is None:
            unexpected_conditions = self.unexpected_conditions
        if earliest_date is None:
            earliest_date = self.earliest_date
        if latest_date is None:
            latest_date = self.latest_date
        if numeric_lower_bound is None:
            numeric_lower_bound = self.lower_bound
        if numeric_upper_bound is None:
            numeric_upper_bound = self.upper_bound

        out_dict = replace_unexpected_values(dataframe = self.dataframe,
                             MISSING_TYPES = MISSING_TYPES,
                             unexpected_exceptions = unexpected_exceptions,
                             unexpected_conditions = unexpected_conditions,
                             TEST_RUV_FLAGS_PATH = TEST_RUV_FLAGS_PATH,
                             earliest_date = earliest_date,
                             latest_date = latest_date,
                             numeric_lower_bound = numeric_lower_bound,
                             numeric_upper_bound = numeric_upper_bound,
                                      logger = self.logger)

        self.dataframe = out_dict['dataframe']
        self.ruv_score0 = out_dict['ruv_score0']
        self.ruv_score1 = out_dict['ruv_score1']
        self.ruv_score2 = out_dict['ruv_score2']




def shoutOUT(type="dline",
             mess=None,
             dotline_length=50,
             logger : logging.Logger = logging):
    """
    Print a line of text with a specified length and format.

    Args:
        type (str): The type of line to print. Valid values are "dline" (default),
            "line", "pline", "HEAD1", "title", "subtitle", "subtitle2", "subtitle3", and "warning".
        mess (str): The text to print out.
        dotline_length (int): The length of the line to print.

    Returns:
        None

    Examples:
        shoutOUT("HEAD1", mess="Header", dotline_length=50)
        shoutOUT(type="dline", dotline_length=50)
    """

    switch = {
        "dline": lambda: logger.info("=" * dotline_length),
        "line": lambda: logger.debug("-" * dotline_length),
        "pline": lambda: logger.debug("." * dotline_length),
        "HEAD1": lambda: logger.info("".join(["\n",
                                              "=" * dotline_length,
                                              "\n",
                                              "-" * ((dotline_length - len(mess)) // 2 - 1),
                                              mess,
                                              "-" * ((dotline_length - len(mess)) // 2 - 1),
                                              " \n",
                                              "=" * dotline_length])),
        "HEAD2": lambda: logger.info("".join(["\n",
                                              "*" * ((dotline_length - len(mess)) // 2 - 1),
                                              mess,
                                              "*" * ((dotline_length - len(mess)) // 2 - 1)])),
        "HEAD3": lambda: logger.info("".join(["\n",
                                              "/" * ((dotline_length - 10 - len(mess)) // 2 - 1),
                                              mess,
                                              "\\" * ((dotline_length - 10 - len(mess)) // 2 - 1)])),
        "title": lambda: logger.info(f"** {mess}"),
        "subtitle": lambda: logger.info(f"*** {mess}"),
        "subtitle2": lambda: logger.debug(f"+++ {mess}"),
        "subtitle3": lambda: logger.debug(f"++++ {mess}"),
        "warning": lambda: logger.warning(f"!!! {mess} !!!"),
    }

    switch[type]()


def get_type_dict(dataframe : pd.DataFrame,
                  explicit : bool = True,
                  stringout : bool = False,
                  logger : logging.Logger = logging):
    """
    Returns a string representation of a dictionary containing the data types
    of each column in the given pandas DataFrame.

    Numeric columns will have type 'numeric', date columns will have type 'date',
    character columns will have type 'category', and columns containing 'id' at
    the beginning or end of their name will have type 'index'.

    Parameters
    ----------
    dataframe : pandas DataFrame
        The DataFrame to extract column data types from.

    Returns
    -------
    str
        A string representation of a dictionary containing the data types
        of each column in the given DataFrame. The keys are the column names
        and the values are the corresponding data types.
    """

    try:

        if explicit:

            class_list = [f"'{col}' : '{dataframe[col].dtype}'" for col in dataframe.columns]

            dtypes_dict = dataframe.dtypes.to_dict()

            # Convert the data type objects to string representations
            type_dict = {col: str(dtype) for col, dtype in dtypes_dict.items()}

        else:
            type_dict = {}

            for col in dataframe.columns:
                col_lower = col.lower()
                if (col_lower.startswith('id_') \
                    or (col_lower.find('_id_') > 0) \
                    or col_lower.endswith('_id')):
                    col_type = 'index'
                elif dataframe[col].dtype == 'object':
                    col_type = 'category'
                elif dataframe[col].dtype.name.startswith('datetime'):
                    col_type = 'date'
                else:
                    col_type = 'numeric'
                type_dict[col] = col_type

            class_list = [f"'{col}' : '{type_dict[col]}'" for col in dataframe.columns]

        if stringout:
            output = f"{{{', '.join(class_list)}}}"
        else:
            output = type_dict


        return output

    except Exception as e:
        logger.error("Error in get_type_dict")
        print(e)


def set_types(dataframe: pd.DataFrame,
              types_dict_str: dict,
              replace_dict: dict = None,
              expected_date_format: str = '%Y-%m-%d',
             logger : logging.Logger = logging) -> pd.DataFrame:
    """
    Change the data types of the columns in the given DataFrame
    based on a dictionary of intended data types.

    Args:
        dataframe (pandas.DataFrame): The DataFrame to change the data types of.
        types_dict_str (dict): A dictionary where the keys are the column names
            and the values are the intended data types for those columns.
        replace_dict (dict, optional): A dictionary containing replacement values
            for specific columns. Defaults to None.
        expected_date_format (str, optional): The expected date format for date columns.
            Defaults to '%Y-%m-%d'.

    Returns:
        pandas.DataFrame: The DataFrame with the changed data types.

    Raises:
        ValueError: If the keys in the dictionary do not match the columns in the DataFrame.
        TypeError: If the data types cannot be changed successfully.
    """
    try:
        dataframe = dataframe.copy()

        # Filter the dictionary to include only the columns present in the DataFrame
        dtypes_dict = {col: dtype for col, dtype in types_dict_str.items() if col in dataframe.columns}

        # Use the astype() method to change the data types of the columns in the DataFrame
        for col, dtype in dtypes_dict.items():
            if dtype.startswith('datetime'):
                if replace_dict is not None:
                    dataframe[col] = dataframe[col].astype(str).replace(replace_dict)
                dataframe[col] = pd.to_datetime(dataframe[col], errors='coerce', format=expected_date_format)
            elif dtype.startswith('int'):
                if replace_dict is not None:
                    dataframe[col] = dataframe[col].astype("float64").replace(replace_dict)
                dataframe[col] = dataframe[col].astype("float64").astype(dtype)
            else:
                if replace_dict is not None:
                    dataframe[col] = dataframe[col].replace(replace_dict)
                dataframe[col] = dataframe[col].astype(dtype)

    except Exception as e:
        logger.error("Unable to change the data types of the DataFrame.",
                     "Please check the types_dict_str argument.")
        raise e

    return dataframe


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

            if independent:
                cond = dtype.startswith('date')
            else:
                cond = True

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

        if subset is not None:
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
                             MISSING_TYPES : dict = MISSING_TYPES,
                             unexpected_exceptions : dict = {"col_names_types": "NONE",
                                                      "missing_values": "NONE",
                                                      "missing_types": "NONE",
                                                      "inf_values": "NONE",
                                                      "date_format": "NONE",
                                                      "duplicates": "NONE",
                                                      "date_range": "NONE",
                                                      "numeric_range": "NONE"},
                             unexpected_conditions : dict = None,
                             ids_for_dup : list = None,
                             TEST_DUV_FLAGS_PATH : str = None,
                             types_dict_str : dict = None,
                             expected_date_format : str = '%Y-%m-%d',
                             earliest_date : str = "1900-08-25",
                             latest_date : str = "2100-01-01",
                             numeric_lower_bound : float = 0,
                             numeric_upper_bound : float = float("inf"),
                             print_score : bool = True,
                            logger : logging.Logger = logging) -> float:

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
    ids_for_dup (list): List of columns to identify duplicates (default is None).
    TEST_DUV_FLAGS_PATH (str): Path for checking unexpected values (default is None).
    types_dict_str (str): String that describes the expected types of the columns (default is None).
    expected_date_format (str): The expected date format (default is '%Y-%m-%d').
    earliest_date (str): The earliest acceptable date (default is "1900-08-25").
    latest_date (str): The latest acceptable date (default is "2100-01-01").
    numeric_lower_bound (float): The lowest acceptable value for numeric columns (default is 0).
    numeric_upper_bound (float): The highest acceptable value for numeric columns
                                    (default is infinity).

    Returns:
        duv_score - number between 0 and 1 that means what percentage of tests have passed
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


        if ids_for_dup is None:
            ids_for_dup = index_cols


        # Run checks

        checks_list = []


        if run_check_col_names_types:

            logger.debug(f"=== checking column names and types")

            checks_list.extend(check_col_names_types(dataframe = dataframe[cols_check_col_names_types],
                                                       types_dict_str = types_dict_str,
                                                       independent = False,
                                                       logger = logger))

        if run_check_missing_values:

            logger.debug(f"=== checking for presence of missing values")

            checks_list.extend([check_missing_values(dataframe = dataframe[cols_check_missing_values],
                                                     logger = logger)])

        if run_check_missing_types:

            logger.debug(f"=== checking for presence of missing types")

            checks_list.extend(check_missing_types(dataframe = dataframe[cols_check_missing_types],
                                                    MISSING_TYPES = MISSING_TYPES,
                                                    independent = False,
                                                    logger = logger))

        if run_check_date_format:

            logger.debug(f"=== checking propper date format")

            checks_list.extend([check_date_format(dataframe = dataframe[cols_check_date_format],
                                                  expected_date_format = expected_date_format,
                                                  independent = False,
                                                  logger = logger)])


        if run_check_date_range:

            logger.debug(f"=== checking expected date range")

            checks_list.extend(check_date_range(dataframe = dataframe[cols_check_date_range],
                                                 earliest_date = earliest_date,
                                                 latest_date = latest_date,
                                                 independent = False,
                                                 ignore_dates = [v for k, v in MISSING_TYPES.items()
                                                                 if k.startswith("date_")],
                                                 logger = logger))

        if run_check_duplicates:

            logger.debug(f"=== checking for duplicates")

            checks_list.extend(check_duplicates(dataframe = dataframe[cols_check_duplicates],
                             subset = ids_for_dup,
                             independent = False,
                             logger = logger))


        if run_check_inf_values:

            logger.debug(f"=== checking for presense of inf values in numeric colums")

            checks_list.extend([check_inf_values(dataframe = dataframe[cols_check_inf_values],
                                                 independent = False,
                                                 logger = logger)])

        if run_check_numeric_range:

            logger.debug(f"=== checking expected numeric range")

            checks_list.extend(check_numeric_range(dataframe = dataframe[cols_check_numeric_range],
                                                    lower_bound = numeric_lower_bound,
                                                    upper_bound = numeric_upper_bound,
                                                    independent = False,
                                                    ignore_values = [v for k, v in MISSING_TYPES.items()
                                                                     if k.startswith("numeric_")],
                                                    logger = logger))


        if run_check_additional_cons:

            logger.debug(f"=== checking additional cons")

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

            return duv_score


    except Exception as e:
        logger.error("Error occured during duv score calculation!")
        print("The error:", e)


#### TEMP FUNCTIONS FOR replace_unexpected


def treat_unexpected_cond(df : pd.DataFrame,
                          description : str,
                          group : str,
                          features : list,
                          query : str,
                          warning : bool,
                          replace,
                          logger : logging.Logger = logging) -> pd.DataFrame:

    """
    Replace unexpected values in a pandas DataFrame with replace values.

    Parameters:
    -----------
    df (pandas DataFrame): The DataFrame to be checked.
    description (str): Description of the unexpected condition being treated.
    group (str): Group identifier for the unexpected condition.
    features (list): List of column names or regex pattern for selecting columns.
    query (str): Query string for selecting rows based on the unexpected condition.
    warning (str): Warning message to be logged if unexpected condition is found.
    replace (object): Value to replace the unexpected values with.

    Returns:
    -------
    df (pandas DataFrame): The DataFrame with replaced unexpected values, if replace is not None.
    """

    df = df.copy()

    logger.debug(description)
    #print(group)
    if group == 'regex_columns':

        features = [i for i in list(df.columns) if re.compile(features).match(i)]

        detected_nrows = 0

        for col in features:
            query1 = query.format(col = col)

            search = df.query(query1)
            nrow = search.shape[0]

            if nrow > 0:

                if warning:
                    detected_nrows =+ 1
                else:
                    df.loc[search.index,col] = replace

        if warning and (detected_nrows > 0):

            mess = f"{description} :: {nrow}"
            logger.warning(mess)


    if group in ['mapping missing', 'multicol mapping', 'string check', 'complex with missing']:

        for col in features:

            if group == 'multicol mapping':

                query1 = query.format(col = col)

            else:
                query1 = query

            search = df.query(query1)
            nrow = search.shape[0]

            if nrow > 0:

                if warning:

                    mess = f"{description} :: {nrow}"
                    logger.warning(mess)

                if replace is not None:
                    df.loc[search.index, col] = replace

    if group in ['logical sum']:

        search = df.query(query)
        nrow = search.shape[0]

        if nrow > 0:

            if warning:
                mess = f"{description} :: {nrow}"
                logger.warning(mess)
            else:
                for col in features:
                    df.loc[search.index, col] = replace

    if group == 'regex clean':

        if warning:
            mess = f"{description} :: {nrow}"
            logger.warning(mess)
        else:
            for col in features:
                for reg in query:
                    df.loc[:,col] = [re.sub(reg, replace, string) for string in df[col]]

    ## specialized temporary messy piece of code
    def generate_condition(range_str):

        digits = []
        for string in range_str:
            match = re.search(r'\d+_\d+', string)
            if match:
                digits.append(match.group())

        range_str = digits[0]

        range_start, range_end = map(int, range_str.split('_'))

        conditions = []
        for i in range(range_end, range_start - 1, -1):
            conditions.append(f"PAYM_BUCKET_{i:02} == -999999.0")

        return " | ".join(["(" + " and ".join(conditions[:idx+1]) + ")" for idx in range(len(conditions))])

    if group == 'regex payments clean':


        if warning == False:

            features = [i for i in list(df.columns) if re.compile(features).match(i)]

            for col in features:
                query = generate_condition([col])

                search = df.query(query)
                nrow = search.shape[0]

                if nrow > 0:
                    df.loc[search.index,col] = replace




    if replace is not None:
        return df


####

def replace_unexpected_values(dataframe : pd.DataFrame,
                             MISSING_TYPES : dict = MISSING_TYPES,
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
                            logger : logging.Logger = logging) -> dict:

    """
    Replace unexpected values in a pandas DataFrame with missing types.

    Parameters:
    -----------

    dataframe (pandas DataFrame): The DataFrame to be checked.
    MISSING_TYPES (dict): Dictionary that maps column names to the values considered as missing
                              for that column.
    unexpected_exceptions (dict): Dictionary that lists column exceptions for each of the
                                      following checks: col_names_types, missing_values, missing_types,
                                      inf_values, date_format, duplicates, date_range, and numeric_range.
    TEST_DUV_FLAGS_PATH (str): Path for checking unexpected values (default is None).
    earliest_date (str): The earliest acceptable date (default is "1900-08-25").
    latest_date (str): The latest acceptable date (default is "2100-01-01").
    numeric_lower_bound (float): The lowest acceptable value for numeric columns (default is 0).
    numeric_upper_bound (float): The highest acceptable value for numeric columns
                                    (default is infinity).

    Returns:
        ruv_score - number between 0 and 1 that means data quality score
    """


    try:


        dataframe = dataframe.copy()

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

        cols_replace_missing_values = [x for x in all_columns
                                    if x not in unexpected_exceptions["irregular_values"]]

        cols_not_replace_missing_values = [x for x in all_columns
                                    if x in unexpected_exceptions["irregular_values"]]

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

        checks_list = []


        if run_replace_category_missing_values:

            logger.debug(f"=== replacing missing values in category cols with missing types")

            irregular_character_values = ["nan", "inf", "-inf", "None", "", "NaN", "NaT"]

            dataframe[category_cols_replace_missing_values] = (dataframe[category_cols_replace_missing_values]\
                .astype(str).replace(irregular_character_values,
                                    MISSING_TYPES['character_not_delivered']))



        if run_replace_capitalization:

            logger.debug(f"=== replacing all upper case characters with lower case")

            for col in cols_replace_capitalization:

                dataframe[col] = dataframe[col].astype(str).str.lower()

        if run_replace_character_unicode:

            logger.debug(f"=== replacing character unicode to latin")

            # Function to replace Latin Unicode characters
            def replace_unicode(text):
                return unidecode(text)

            for col in cols_replace_character_unicode:

                dataframe[col] = dataframe[col].astype(str).apply(replace_unicode)

        if run_replace_additional_cons:

            logger.debug(f"=== replacing with additional cons")

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

            logger.debug(f"=== replacing missing values in date cols with missing types")

            irregular_date_values = [pd.NaT]

            dataframe[date_cols_replace_missing_values] = (dataframe[date_cols_replace_missing_values]\
                .replace(irregular_date_values,
                         MISSING_TYPES['date_not_delivered']))


        if run_replace_numeric_missing_values:

            logger.debug(f"=== replacing missing values in numeric cols with missing types")

            irregular_numeric_values = [np.nan, np.inf, -np.inf, None]

            dataframe[numeric_cols_replace_missing_values] = (dataframe[numeric_cols_replace_missing_values]\
                .replace(irregular_numeric_values,
                         MISSING_TYPES['numeric_not_delivered']))


        if run_replace_date_range:

            logger.debug(f"=== replacing values outside of expected date range")

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

            logger.debug(f"=== replacing values outside of expected numeric range")

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
            logger.warning(f"** Dataframe is completely unusable based on corrected data quality score!")

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
