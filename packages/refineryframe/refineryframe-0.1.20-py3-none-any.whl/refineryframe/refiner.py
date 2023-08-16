"""
refineryframe Module

This module provides a Refiner class to encapsulate functions for data refinement
and validation. The Refiner class is designed to work with pandas DataFrames and
perform various checks and replacements for data preprocessing.
"""

import logging
import pandas as pd
import attr
from refineryframe.other import shoutOUT, get_type_dict, set_types
from refineryframe.detect_unexpected import check_date_range, \
    check_col_names_types, check_date_format, check_duplicates, \
        check_inf_values, check_missing_values, check_numeric_range, \
            check_missing_types, detect_unexpected_values
from refineryframe.replace_unexpected import replace_unexpected_values

@attr.s
class Refiner:

    """
    Class that encapsulates functions for data refining and validation.

    Attributes:
        dataframe (pd.DataFrame): The input pandas DataFrame to be processed.
        replace_dict (dict, optional): A dictionary to define replacements for specific values in the DataFrame.
        MISSING_TYPES (dict, optional): Default values for missing types in different columns of the DataFrame.
        expected_date_format (str, optional): The expected date format for date columns in the DataFrame.
        mess (str, optional): A custom message used in the `shout` method for printing.
        shout_type (str, optional): The type of output for the `shout` method (e.g., 'HEAD2').
        logger (logging.Logger, optional): A custom logger object for logging messages.
        logger_name (str, optional): The name of the logger for the class instance.
        loggerLvl (int, optional): The logging level for the logger.
        dotline_length (int, optional): The length of the line to be printed in the `shout` method.
        lower_bound (float, optional): The lower bound for numeric range validation.
        upper_bound (float, optional): The upper bound for numeric range validation.
        earliest_date (str, optional): The earliest allowed date for date range validation.
        latest_date (str, optional): The latest allowed date for date range validation.
        ids_for_dedup (list, optional): A list of column names to be used for duplicate detection.
        unexpected_exceptions_duv (dict, optional): A dictionary of unexpected exceptions for data value validation.
        unexpected_exceptions_ruv (dict, optional): A dictionary of unexpected exceptions for data replacement validation.
        unexpected_conditions (None or callable, optional): A callable function for custom unexpected conditions.
        ignore_values (list, optional): A list of values to ignore during numeric range validation.
        ignore_dates (list, optional): A list of dates to ignore during date range validation.

    Methods:
        shout(mess=None): Prints a line of text with a specified length and format.
        get_type_dict_from_dataframe(explicit=True, stringout=False): Returns a dictionary containing the data types
            of each column in the given pandas DataFrame.
        set_type_dict(type_dict=None, explicit=True, stringout=False): Changes the data types of the columns in the
            DataFrame based on a dictionary of intended data types.
        set_types(type_dict=None, replace_dict=None, expected_date_format=None): Changes the data types of the columns
            in the DataFrame based on a dictionary of intended data types.
        get_refiner_settings(): Extracts values of parameters from the Refiner and saves them in a dictionary for later use.
        set_refiner_settings(settings: dict): Updates input parameters with values from the provided settings dict.
        check_missing_types(): Searches for instances of missing types in each column of the DataFrame.
        check_missing_values(): Counts the number of NaN, None, and NaT values in each column of the DataFrame.
        check_inf_values(): Counts the inf values in each column of the DataFrame.
        check_date_format(): Checks if the values in the datetime columns have the expected 'YYYY-MM-DD' format.
        check_duplicates(subset=None): Checks for duplicates in the DataFrame.
        check_col_names_types(): Checks if the DataFrame has the same column names as the types_dict_str dictionary
            and those columns have the same types as items in the dictionary.
        check_numeric_range(numeric_cols=None, lower_bound=None, upper_bound=None, ignore_values=None): Checks if
            numeric values are in expected ranges.
        check_date_range(earliest_date=None, latest_date=None, ignore_dates=None): Checks if dates are in expected ranges.
        detect_unexpected_values(MISSING_TYPES=None, unexpected_exceptions=None, unexpected_conditions=None,
                                 ids_for_dedup=None, TEST_DUV_FLAGS_PATH=None, types_dict_str=None,
                                 expected_date_format=None, earliest_date=None, latest_date=None, numeric_lower_bound=None,
                                 numeric_upper_bound=None, print_score=True): Detects unexpected values in the DataFrame.
        get_unexpected_exceptions_scaned(dataframe=None): Returns unexpected_exceptions with appropriate settings for the
            values in the DataFrame.
        replace_unexpected_values(MISSING_TYPES=None, unexpected_exceptions=None, unexpected_conditions=None,
                                  TEST_RUV_FLAGS_PATH=None, earliest_date=None, latest_date=None, numeric_lower_bound=None,
                                  numeric_upper_bound=None): Replaces unexpected values in the DataFrame with missing types
                                  based on a dictionary of unexpected exceptions.
    """


    # inputs
    dataframe = attr.ib(type=pd.DataFrame)
    replace_dict = attr.ib(default=None, type=dict)

    # inputs with defaults
    MISSING_TYPES = attr.ib(default={'date_not_delivered': '1850-01-09',
                 'numeric_not_delivered': -999,
                 'character_not_delivered': 'missing'}, type=dict)
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
    ids_for_dedup = attr.ib(default="ALL", type=list)

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
    unexpected_exceptions_scaned = attr.ib(default={},init = False, type=dict)
    type_dict = attr.ib(default={}, init = False, type=dict)

    MISSING_TYPES_TEST = attr.ib(default=None, init = False)
    MISSING_COUNT_TEST = attr.ib(default=None, init = False)
    NUM_INF_TEST = attr.ib(default=None, init = False)
    DATE_FORMAT_TEST = attr.ib(default=None, init = False)
    DATE_RANGE_TEST = attr.ib(default=None, init = False)
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

        """
        Initialize a logger for the class instance based on the specified logging level and logger name.
        """

        logging.basicConfig(level=self.loggerLvl)
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.loggerLvl)

        self.logger = logger


    def shout(self, mess = None) -> None:

        """
        Prints a line of text with a specified length and format.
        """

        if mess is None:
            mess = self.mess

        shoutOUT(output_type=self.shout_type,
                 mess=mess,
                 dotline_length=self.dotline_length,
                 logger=self.logger)

    def get_type_dict_from_dataframe(self,
                      explicit=True,
                      stringout=False) -> dict:

        """
        Returns a dictionary or string representation of a dictionary containing the data types
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
                      stringout=False) -> None:

        """
        Changes the data types of the columns in the given DataFrame
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
        Changes the data types of the columns in the given DataFrame
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

        self.type_dict = type_dict

    def get_refiner_settings(self) -> dict:

        """
        Extracts values of parameters from refiner and saves them in dictionary for later use.
        """

        exclude_attributes = ['dataframe',
                      'MISSING_TYPES_TEST',
                      'MISSING_COUNT_TEST',
                      'NUM_INF_TEST',
                      'DATE_FORMAT_TEST',
                      'DATE_RANGE_TEST',
                      'DUPLICATES_TEST',
                      'COL_NAMES_TYPES_TEST',
                      'NUMERIC_RANGE_TEST',
                      'logger',
                      'unexpected_exceptions_scaned',
                      'duv_score',
                      'ruv_score0',
                      'ruv_score1',
                      'ruv_score2']

        # Getting the dictionary representation of the instance
        my_instance_dict = attr.asdict(self)

        # Excluding 'exclude_attributes' from the dictionary representation
        filtered_instance_dict = {key: value for key, value in my_instance_dict.items() if key not in exclude_attributes}

        return filtered_instance_dict

    def set_refiner_settings(self, settings : dict) -> None:

        """
        Updates input parameters with values from provided settings dict.
        """

        # Overwrite parameters of the existing instance
        for key, value in settings.items():
            setattr(self, key, value)

        # Reinitialize logger
        self.initialize_logger()


    def check_missing_types(self) -> None:

        """
        Takes a DataFrame and a dictionary of missing types as input,
        and searches for any instances of these missing types in each column of the DataFrame.

        If any instances are found, a warning message is logged containing the column name,
        the missing value, and the count of missing values found.
        """

        self.MISSING_TYPES_TEST = check_missing_types(dataframe = self.dataframe,
                                                        MISSING_TYPES = self.MISSING_TYPES,
                                                        independent = True,
                                      logger = self.logger)

    def check_missing_values(self) -> None:

        """
        Counts the number of NaN, None, and NaT values in each column of a pandas DataFrame.
        """

        self.MISSING_COUNT_TEST = check_missing_values(dataframe = self.dataframe,
                                      logger = self.logger)

    def check_inf_values(self) -> None:

        """
        Counts the inf values in each column of a pandas DataFrame.
        """

        self.NUM_INF_TEST = check_inf_values(dataframe = self.dataframe,
                                             independent = True,
                                             logger = self.logger)

    def check_date_format(self) -> None:

        """
        Checks if the values in the datetime columns of the input dataframe
        have the expected 'YYYY-MM-DD' format.
        """

        self.DATE_FORMAT_TEST = check_date_format(dataframe = self.dataframe,
                                                  expected_date_format = self.expected_date_format,
                                                  independent = True,
                                                  logger = self.logger)

    def check_duplicates(self,
                         subset = None) -> None:

        """
        Checks for duplicates in a pandas DataFrame.
        """

        if subset is None:
            subset = self.ids_for_dedup

        self.DUPLICATES_TEST = check_duplicates(dataframe = self.dataframe,
                                                 subset = subset,
                                                 independent = True,
                                                 logger = self.logger)

    def check_col_names_types(self) -> None:

        """
        Checks if a given dataframe has the same column names as keys in a given dictionary
        and those columns have the same types as items in the dictionary.
        """

        self.COL_NAMES_TYPES_TEST = check_col_names_types(dataframe = self.dataframe,
                          types_dict_str = self.type_dict,
                          independent = True,
                                      logger = self.logger)

    def check_numeric_range(self,
                            numeric_cols : list = None,
                            lower_bound = None,
                            upper_bound = None,
                            ignore_values = None) -> None:

        """
        Checks if numeric values are in expected ranges.
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
                        ignore_dates = None) -> None:

        """
        Checks if dates are in expected ranges.
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
                                 ids_for_dedup = None,
                                 TEST_DUV_FLAGS_PATH = None,
                                 types_dict_str = None,
                                 expected_date_format = None,
                                 earliest_date = None,
                                 latest_date = None,
                                 numeric_lower_bound = None,
                                 numeric_upper_bound = None,
                                 print_score = True) -> None:

        """
        Detects unexpected values in a pandas DataFrame.
        """

        if MISSING_TYPES is None:
            MISSING_TYPES = self.MISSING_TYPES
        if unexpected_exceptions is None:
            unexpected_exceptions = self.unexpected_exceptions_duv
        if unexpected_conditions is None:
            unexpected_conditions = self.unexpected_conditions
        if types_dict_str is None:
            types_dict_str = self.type_dict
        if ids_for_dedup is None:
            ids_for_dedup = self.ids_for_dedup
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

        duv_obj = detect_unexpected_values(dataframe = self.dataframe,
                                                 MISSING_TYPES = MISSING_TYPES,
                                                 unexpected_exceptions = unexpected_exceptions,
                                                 unexpected_conditions = unexpected_conditions,
                                                 ids_for_dedup = ids_for_dedup,
                                                 TEST_DUV_FLAGS_PATH = TEST_DUV_FLAGS_PATH,
                                                 types_dict_str = types_dict_str,
                                                 expected_date_format = expected_date_format,
                                                 earliest_date = earliest_date,
                                                 latest_date = latest_date,
                                                 numeric_lower_bound = numeric_lower_bound,
                                                 numeric_upper_bound = numeric_upper_bound,
                                                 print_score = print_score,
                                      logger = self.logger)

        self.duv_score = duv_obj['duv_score']
        self.unexpected_exceptions_scaned = duv_obj['unexpected_exceptions_scaned']

    def get_unexpected_exceptions_scaned(self, dataframe = None) -> dict:

        """
        Returns unexpected_exceptions with appropriate settings to the values in the dataframe.
        """

        if dataframe is None:
            dataframe = self.dataframe

        duv_obj = detect_unexpected_values(dataframe = dataframe,
                                                 MISSING_TYPES = self.MISSING_TYPES,
                                                 unexpected_exceptions = self.unexpected_exceptions_duv,
                                                 unexpected_conditions = self.unexpected_conditions,
                                                 ids_for_dedup = self.ids_for_dedup,
                                                 TEST_DUV_FLAGS_PATH = None,
                                                 types_dict_str = self.type_dict,
                                                 expected_date_format = self.expected_date_format,
                                                 earliest_date = self.earliest_date,
                                                 latest_date = self.latest_date,
                                                 numeric_lower_bound = self.lower_bound,
                                                 numeric_upper_bound = self.upper_bound,
                                                 print_score = True,
                                      logger = self.logger)

        return duv_obj['unexpected_exceptions_scaned']




    def replace_unexpected_values(self,
                             MISSING_TYPES = None,
                             unexpected_exceptions = None,
                             unexpected_conditions = None,
                             TEST_RUV_FLAGS_PATH = None,
                             earliest_date = None,
                             latest_date = None,
                             numeric_lower_bound = None,
                             numeric_upper_bound = None) -> None:

        """
        Replaces unexpected values in a pandas DataFrame with missing types.
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
