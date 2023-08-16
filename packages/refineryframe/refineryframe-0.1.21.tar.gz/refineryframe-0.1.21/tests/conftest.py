import pytest
import logging
import pandas as pd
import numpy as np
import attr
from datetime import datetime
from refineryframe.refiner import Refiner


@pytest.fixture(scope='session')
def df():

    df = pd.DataFrame({
    'num_id' : [1, 2, 3, 4, 5],
    'NumericColumn': [1, -np.inf, np.inf,np.nan, None],
    'NumericColumn_exepted': [1, -996, np.inf,np.nan, None],
    'NumericColumn2': [None, None, 1,None, None],
    'NumericColumn3': [1, 2, 3, 4, 5],
    'DateColumn': pd.date_range(start='2022-01-01', periods=5),
    'DateColumn2': [pd.NaT,pd.to_datetime('2022-01-01'),pd.NaT,pd.NaT,pd.NaT],
    'DateColumn3': ['2122-05-01',
                    '2022-01-01',
                    '2021-01-01',
                    '1000-01-09',
                    '1850-01-09'],
    'CharColumn': ['Fół', None, np.nan, 'nót eXpęćTęd', '']})

    yield df


@pytest.fixture(scope='session')
def df_dup():

    df = pd.DataFrame({
    'num_id': ['1', '2', '3', '4', '5','5'],
    'NumericColumn': [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn_exepted': [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn3': [1, 2, 0, 0, 0, 0],
    'DateColumn': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-05'],
    'DateColumn2': ['1850-01-09', '2022-01-01', '1850-01-09', '1850-01-09', '1850-01-09', '1850-01-09'],
    'DateColumn3': ['1850-01-09', '2022-01-01', '1850-01-09', '1850-01-09', '1850-01-09', '1850-01-09'],
    'CharColumn': ['fol', 'miss', 'miss', 'miss', 'miss', 'miss']
})

    yield df

@pytest.fixture(scope='session')
def df_dup2():

    df = pd.DataFrame({
    'num_id': ['1', '2', '3', '4', '5','5'],
    'NumericColumn': [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn00': [1.0, 0.0, 0.0, 0.0, 0.0, 0.1],
    'NumericColumn_exepted': [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn3': [1, 2, 0, 0, 0, 0],
    'DateColumn': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-05'],
    'DateColumn2': ['1850-01-09', '2022-01-01', '1850-01-09', '1850-01-09', '1850-01-09', '1850-01-09'],
    'DateColumn3': ['1850-01-09', '2022-01-01', '1850-01-09', '1850-01-09', '1850-01-09', '1850-01-09'],
    'CharColumn': ['fol', 'miss', 'miss', 'miss', 'miss', 'miss']
})
    df.columns = ['num_id', 'NumericColumn', 'NumericColumn', 'NumericColumn_exepted',
       'NumericColumn2', 'NumericColumn3', 'DateColumn', 'DateColumn2',
       'DateColumn3', 'CharColumn']

    yield df

@pytest.fixture(scope='session')
def df1():

    df = pd.DataFrame({
    'num_id': ['1', '2', '3', '4', '5'],
    'NumericColumn': [1.0, -999.0, -999.0, -999.0, -999.0],
    'NumericColumn_exepted': [1.0, -999.0, -999.0, -999.0, -999.0],
    'NumericColumn2': [-999.0, -999.0, -999.0, -999.0, -999.0],
    'NumericColumn3': [1, 2, 3, 4, -999],
    'DateColumn': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05'],
    'DateColumn2': ['1850-01-09', '2022-01-01', '1850-01-09', '1850-01-09', '1850-01-09'],
    'DateColumn3': ['1850-01-09', '2022-01-01', '1850-01-09', '1850-01-09', '1850-01-09'],
    'CharColumn': ['fol', 'missing', 'missing', 'not expected', 'missing']
})

    # Convert the DateColumns to datetime64[ns]
    df['DateColumn'] = pd.to_datetime(df['DateColumn'])
    df['DateColumn2'] = pd.to_datetime(df['DateColumn2'])
    df['DateColumn3'] = pd.to_datetime(df['DateColumn3'])

    yield df


@pytest.fixture(scope='session')
def df2():

    df = pd.DataFrame({
    'num_id': ['1', '2', '3', '4', '5'],
    'NumericColumn': [1.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn_exepted': [1.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn2': [0.0, 0.0, 0.0, 0.0, 0.0],
    'NumericColumn3': [1, 2, 0, 0, 0],
    'DateColumn': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05'],
    'DateColumn2': ['1850-01-09', '2022-01-01', '1850-01-09', '1850-01-09', '1850-01-09'],
    'DateColumn3': ['1850-01-09', '2022-01-01', '1850-01-09', '1850-01-09', '1850-01-09'],
    'CharColumn': ['fol', 'miss', 'miss', 'miss', 'miss']
})

    # Convert the DateColumns to datetime64[ns]
    df['DateColumn'] = pd.to_datetime(df['DateColumn'])
    df['DateColumn2'] = pd.to_datetime(df['DateColumn2'])
    df['DateColumn3'] = pd.to_datetime(df['DateColumn3'])

    yield df

@pytest.fixture(scope='session')
def MISSING_TYPES():

    MISSING_TYPES = {'date_not_delivered': '1850-01-09',
                 'date_other_missing_type': '1850-01-08',
                 'numeric_not_delivered': -999,
                 'character_not_delivered': 'missing'}

    yield MISSING_TYPES

@pytest.fixture(scope='session')
def unexpected_exceptions():

    unexpected_exceptions = {
    "col_names_types": "NONE",
    "missing_values": ["NumericColumn_exepted"],
    "missing_types": "NONE",
    "inf_values": "NONE",
    "date_format": "NONE",
    "duplicates": "ALL",
    "date_range": "NONE",
    "numeric_range": "NONE"
}

    yield unexpected_exceptions

@pytest.fixture(scope='session')
def unexpected_exceptions2():

    unexpected_exceptions2 = {
    "col_names_types": "NONE",
    "missing_values": "ALL",
    "missing_types": "ALL",
    "inf_values": "NONE",
    "date_format": "NONE",
    "duplicates": "ALL",
    "date_range": "NONE",
    "numeric_range": "ALL"
}

    yield unexpected_exceptions2


@pytest.fixture(scope='session')
def scanned_unexpected_exceptions():

    scanned_unexpected_exceptions = {
                "col_names_types": "NONE",
                "missing_values": "ALL",
                "missing_types": "NONE",
                "inf_values": "ALL",
                "date_format": "ALL",
                "duplicates": "NONE",
                "date_range": "ALL",
                "numeric_range": "NONE"
            }

    yield scanned_unexpected_exceptions


@pytest.fixture(scope='session')
def refiner_settings():

    refiner_settings = {'replace_dict': {-996: -999, '1000-01-09': '1850-01-09'},
                        'MISSING_TYPES': {'date_not_delivered': '1850-01-09',
                        'numeric_not_delivered': -999,
                        'character_not_delivered': 'missing'},
                        'expected_date_format': '%Y-%m-%d',
                        'mess': 'INITIAL PREPROCESSING',
                        'shout_type': 'HEAD2',
                        'logger_name': 'Refiner',
                        'loggerLvl': 10,
                        'dotline_length': 50,
                        'lower_bound': -np.inf,
                        'upper_bound': np.inf,
                        'earliest_date': '1900-08-25',
                        'latest_date': '2100-01-01',
                        'ids_for_dedup': 'ALL',
                        'unexpected_exceptions_duv': {'col_names_types': 'NONE',
                                                    'missing_values': 'ALL',
                                                    'missing_types': 'ALL',
                                                    'inf_values': 'NONE',
                                                    'date_format': 'NONE',
                                                    'duplicates': 'ALL',
                                                    'date_range': 'NONE',
                                                    'numeric_range': 'ALL'},
                        'unexpected_exceptions_ruv': {'irregular_values': 'NONE',
                                                    'date_range': 'NONE',
                                                    'numeric_range': 'NONE',
                                                    'capitalization': 'NONE',
                                                    'unicode_character': 'NONE'},
                                                    'unexpected_conditions': None,
                        'unexpected_exceptions_error': {"col_name_duplicates": False,
                                                   "col_names_types": False,
                                                    "missing_values": False,
                                                    "missing_types": False,
                                                    "inf_values": False,
                                                    "date_format": False,
                                                    "duplicates": False,
                                                    "date_range": False,
                                                    "numeric_range": False},
                        'thresholds' : {'cmt_scores' : {'numeric_score' : 100,
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
                        'ignore_values': [],
                        'ignore_dates': [],
                        'type_dict': {}}

    yield refiner_settings





@pytest.fixture(scope='session')
def types_dict_str():

    types_dict_str = {'num_id' : 'int64',
                   'NumericColumn' : 'float64',
                   'NumericColumn_exepted' : 'float64',
                   'NumericColumn2' : 'float64',
                   'NumericColumn3' : 'int64',
                   'DateColumn' : 'datetime64[ns]',
                   'DateColumn2' : 'datetime64[ns]',
                   'DateColumn3' : 'datetime64[ns]',
                   'CharColumn' : 'object'}

    yield types_dict_str

@pytest.fixture(scope='session')
def types_dict_str2():

    types_dict_str = """{'num_id' : 'int64',\
        'NumericColumn' : 'float64',\
            'NumericColumn_exepted' : 'float64',\
                'NumericColumn2' : 'float64',\
                    'NumericColumn3' : 'int64',\
                        'DateColumn' : 'datetime64[ns]',\
                            'DateColumn2' : 'datetime64[ns]',\
                                'DateColumn3' : 'datetime64[ns]',\
                                    'CharColumn' : 'object'}"""

    yield types_dict_str

@pytest.fixture(scope='session')
def types_dict_str3():

    types_dict_str = {'num_id' : 'int64',
                   'NumericColumn' : 'float64',
                   'NumericColumn4' : 'float64',
                   'NumericColumn_exepted' : 'float64',
                   'NumericColumn2' : 'float64',
                   'NumericColumn3' : 'int64',
                   'DateColumn' : 'datetime64[ns]',
                   'DateColumn2' : 'datetime64[ns]',
                   'DateColumn3' : 'datetime64[ns]',
                   'CharColumn' : 'object'}

    yield types_dict_str


@pytest.fixture(scope='session')
def replace_dict():

    replace_dict = {-996 : -999,
                "1000-01-09": "1850-01-09"}

    yield replace_dict

@pytest.fixture(scope='session')
def tns(df,replace_dict,unexpected_exceptions):

    tns = Refiner(dataframe = df,
              replace_dict = replace_dict,
              loggerLvl = logging.DEBUG,
              unexpected_exceptions_duv = unexpected_exceptions)

    yield tns

@pytest.fixture(scope='session')
def tns2(df,replace_dict,unexpected_exceptions2):

    tns = Refiner(dataframe = df,
              replace_dict = replace_dict,
              loggerLvl = logging.DEBUG,
              unexpected_exceptions_duv = unexpected_exceptions2)

    yield tns

@pytest.fixture(scope='session')
def unexpected_conditions():

    unexpected_conditions = {
    '1': {
        'description': 'Replace numeric missing with with zero',
        'group': 'regex_columns',
        'features': r'^Numeric',
        'query': "{col} < 0",
        'warning': True,
        'set': 0
    },
    '2': {
        'description': "Clean text column from '-ing' endings and 'not ' beginings",
        'group': 'regex clean',
        'features': ['CharColumn'],
        'query': [r'ing', r'^not.'],
        'warning': False,
        'set': ''
    },
    '3': {
        'description': "Detect/Replace numeric values in certain column with zeros if > 2",
        'group': 'multicol mapping',
        'features': ['NumericColumn3'],
        'query': '{col} > 2',
        'warning': True,
        'set': 0
    },
    '4': {
        'description': "Replace strings with values if some part of the string is detected",
        'group': 'string check',
        'features': ['CharColumn'],
        'query': f"CharColumn.str.contains('cted', regex = True)",
        'warning': False,
        'set': 'miss'
    }
    }

    yield unexpected_conditions