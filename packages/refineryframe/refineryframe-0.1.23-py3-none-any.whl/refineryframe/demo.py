"""
demo.py - Support module for refineryframe package that contains definitions of testing dataframes, etc.

"""


import numpy as np
import pandas as pd


tiny_example = {'dataframe' : pd.DataFrame({
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
    'CharColumn': ['Fół', None, np.nan, 'nót eXpęćTęd', '']
}),

                'MISSING_TYPES' : {'date_not_delivered': '1850-01-09',
                                'date_other_missing_type': '1850-01-08',
                                'numeric_not_delivered': -999,
                                'character_not_delivered': 'missing'},
                'replace_dict' : {-996 : -999,
                            "1000-01-09": "1850-01-09"}}

