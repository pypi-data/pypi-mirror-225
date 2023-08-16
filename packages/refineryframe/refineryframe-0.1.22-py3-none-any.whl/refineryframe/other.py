"""
Module Name: other.py

This module contains various utility functions for logging, data manipulation, and data type handling.

Functions:
    shoutOUT(type="dline", mess=None, dotline_length=50, logger: logging.Logger = logging):
        Print a line of text with a specified length and format.

    get_type_dict(dataframe: pd.DataFrame, explicit: bool = True, stringout: bool = False,
                  logger: logging.Logger = logging) -> str:
        Returns a string representation of a dictionary containing the data types
        of each column in the given pandas DataFrame.

    set_types(dataframe: pd.DataFrame, types_dict_str: dict, replace_dict: dict = None,
              expected_date_format: str = '%Y-%m-%d', logger: logging.Logger = logging) -> pd.DataFrame:
        Change the data types of the columns in the given DataFrame based on a dictionary of intended data types.

    treat_unexpected_cond(df: pd.DataFrame, description: str, group: str, features: list,
                          query: str, warning: bool, replace, logger: logging.Logger = logging) -> pd.DataFrame:
        Replace unexpected values in a pandas DataFrame with replace values.

Dependencies:
    - logging
    - pandas as pd
    - re

Note:
    Please refer to the docstrings of individual functions for detailed information and usage examples.

"""


import logging
import re
import pandas as pd

def shoutOUT(output_type : str = "dline",
             mess : str = None,
             dotline_length : int = 50,
             logger : logging.Logger = logging) -> None:
    """
    Print a line of text with a specified length and format.

    Args:
        output_type (str): The type of line to print. Valid values are "dline" (default),
            "line", "pline", "HEAD1", "title", "subtitle", "subtitle2", "subtitle3", and "warning".
        mess (str): The text to print out.
        dotline_length (int): The length of the line to print.

    Returns:
        None

    Examples:
        shoutOUT("HEAD1", mess="Header", dotline_length=50)
        shoutOUT(output_type="dline", dotline_length=50)
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

    switch[output_type]()


def get_type_dict(dataframe : pd.DataFrame,
                  explicit : bool = True,
                  stringout : bool = False,
                  logger : logging.Logger = logging) -> dict:
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


        if warning is False:

            features = [i for i in list(df.columns) if re.compile(features).match(i)]

            for col in features:
                query = generate_condition([col])

                search = df.query(query)
                nrow = search.shape[0]

                if nrow > 0:
                    df.loc[search.index,col] = replace




    if replace is not None:
        return df
