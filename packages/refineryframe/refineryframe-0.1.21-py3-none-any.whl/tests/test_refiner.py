import pytest
import logging
from refineryframe.refiner import Refiner, check_duplicates

def test_make_refiner_class(df, replace_dict, unexpected_exceptions):

    try:
        tns = Refiner(dataframe = df,
              replace_dict = replace_dict,
              ids_for_dedup = None,
              loggerLvl = logging.DEBUG,
              unexpected_exceptions_duv = unexpected_exceptions)
    except Exception as e:
        pytest.fail(f"divide function raised an exception: {e}")

    # If no exception was raised, the test passes
    assert isinstance(tns, Refiner)

def test_getting_types(tns):

    assert tns.get_type_dict_from_dataframe() == {'num_id': 'int64',
                                                    'NumericColumn': 'float64',
                                                    'NumericColumn_exepted': 'float64',
                                                    'NumericColumn2': 'float64',
                                                    'NumericColumn3': 'int64',
                                                    'DateColumn': 'datetime64[ns]',
                                                    'DateColumn2': 'datetime64[ns]',
                                                    'DateColumn3': 'object',
                                                    'CharColumn': 'object'}


def test_setting_types(tns, types_dict_str):

    tns.set_types(type_dict = types_dict_str)

    assert tns.get_type_dict_from_dataframe() == {'num_id': 'int64',
                                                    'NumericColumn': 'float64',
                                                    'NumericColumn_exepted': 'float64',
                                                    'NumericColumn2': 'float64',
                                                    'NumericColumn3': 'int64',
                                                    'DateColumn': 'datetime64[ns]',
                                                    'DateColumn2': 'datetime64[ns]',
                                                    'DateColumn3': 'datetime64[ns]',
                                                    'CharColumn': 'object'}

def test_check_missing_types(tns, caplog):

    tns.check_missing_types()

    assert "Column NumericColumn_exepted: (-999) : 1 : 20.00%" in caplog.text
    assert "Column DateColumn3: (1850-01-09) : 2 : 40.00%" in caplog.text


def test_check_missing_values(tns, caplog):

    tns.check_missing_values()

    assert "Column NumericColumn: (NA) : 2 : 40.00%" in caplog.text
    assert "Column NumericColumn_exepted: (NA) : 2 : 40.00%" in caplog.text
    assert "Column NumericColumn2: (NA) : 4 : 80.00%" in caplog.text
    assert "Column DateColumn2: (NA) : 4 : 80.00%" in caplog.text
    assert "Column CharColumn: (NA) : 2 : 40.00%" in caplog.text

def test_check_inf_values(tns, caplog):

    tns.check_inf_values()

    assert "Column NumericColumn: (INF) : 2 : 40.00%" in caplog.text
    assert "Column NumericColumn_exepted: (INF) : 1 : 20.00%" in caplog.text

def test_check_col_names_types(tns, caplog):

    tns.check_col_names_types()

    assert "" in caplog.text

def test_check_date_format(tns, caplog):

    tns.check_date_format()

    assert "Column DateColumn2 has non-date values or unexpected format." in caplog.text

def test_check_duplicates(tns, caplog):

    tns.check_duplicates()

    assert "" in caplog.text

def test_check_duplicates_not_independent(df1):

    assert all(check_duplicates(df1, independent=False)) is True

def test_check_numeric_range(tns, caplog):

    tns.check_numeric_range()

    assert "" in caplog.text



def test_detect_unexpected_values(tns, caplog):

    tns.detect_unexpected_values(earliest_date = "1920-01-01",
                         latest_date = "DateColumn3")

    assert "checking column names and types" in caplog.text
    assert "checking for presence of missing values" in caplog.text
    assert "Column NumericColumn: (NA) : 2 : 40.00%" in caplog.text
    assert "Column NumericColumn_exepted: (-999) : 1 : 20.00%" in caplog.text
    assert "Column NumericColumn2: (NA) : 4 : 80.00%" in caplog.text
    assert "Column DateColumn2: (NA) : 4 : 80.00%" in caplog.text
    assert "Column CharColumn: (NA) : 2 : 40.00%" in caplog.text
    assert "checking for presence of missing types" in caplog.text
    assert "Column NumericColumn_exepted: (-999) : 1 : 20.00%" in caplog.text
    assert "Column DateColumn3: (1850-01-09) : 2 : 40.00%" in caplog.text
    assert "checking propper date format" in caplog.text
    assert "Column DateColumn2 has non-date values or unexpected format." in caplog.text
    assert "checking expected date range" in caplog.text
    assert "Not all dates in DateColumn are later than DateColumn3" in caplog.text
    assert "checking for presense of inf values in numeric colums" in caplog.text
    assert "checking expected numeric range" in caplog.text
    assert "Percentage of passed tests: 50.00%" in caplog.text


def test_get_unexpected_exceptions_scaned(tns, scanned_unexpected_exceptions):

    scanned_unexpected_exceptions2 = tns.get_unexpected_exceptions_scaned()

    assert scanned_unexpected_exceptions2 == scanned_unexpected_exceptions


def test_duv_score1(tns):

    assert tns.duv_score == 0.5


def test_replace_unexpected(tns,df1, caplog):

    tns.replace_unexpected_values(numeric_lower_bound = "NumericColumn3",
                                numeric_upper_bound = 4,
                                earliest_date = "1920-01-02",
                                latest_date = "DateColumn2",
                                unexpected_exceptions = {"irregular_values": "NONE",
                                                            "date_range": "DateColumn",
                                                            "numeric_range": "NONE",
                                                            "capitalization": "NONE",
                                                            "unicode_character": "NONE"})

    assert "replacing missing values in category cols with missing types" in caplog.text
    assert "replacing all upper case characters with lower case" in caplog.text
    assert "replacing character unicode to latin" in caplog.text
    assert "replacing missing values in date cols with missing types" in caplog.text
    assert "replacing missing values in numeric cols with missing types" in caplog.text
    assert "replacing values outside of expected date range" in caplog.text
    assert "replacing values outside of expected numeric range" in caplog.text
    assert "Usable values in the dataframe:  44.44%" in caplog.text
    assert "Uncorrected data quality score:  32.22%" in caplog.text
    assert "Corrected data quality score:  52.57%" in caplog.text

    assert tns.dataframe.equals(df1)


def test_detect_unexpected_values_with_conds(tns, unexpected_conditions, caplog):

    tns.detect_unexpected_values(unexpected_conditions = unexpected_conditions)

    assert "checking column names and types" in caplog.text
    assert "checking for presence of missing values" in caplog.text
    assert "Column CharColumn: (missing) : 3 : 60.00%" in caplog.text
    assert "Column DateColumn2: (1850-01-09) : 4 : 80.00%" in caplog.text
    assert "Column DateColumn3: (1850-01-09) : 4 : 80.00%" in caplog.text
    assert "Column NumericColumn: (-999) : 4 : 80.00%" in caplog.text
    assert "Column NumericColumn_exepted: (-999) : 4 : 80.00%" in caplog.text
    assert "Column NumericColumn2: (-999) : 5 : 100.00%" in caplog.text
    assert "Column NumericColumn3: (-999) : 1 : 20.00%" in caplog.text
    assert "checking propper date format" in caplog.text
    assert "checking expected date range" in caplog.text
    assert "checking for presense of inf values in numeric colums" in caplog.text
    assert "checking expected numeric range" in caplog.text

    assert "Replace numeric missing with with zero" in caplog.text
    assert "Replace numeric missing with with zero :: 1" in caplog.text
    assert "Detect/Replace numeric values in certain column with zeros if > 2" in caplog.text
    assert "Detect/Replace numeric values in certain column with zeros if > 2 :: 2" in caplog.text
    assert "Percentage of passed tests: 66.67%" in caplog.text


def test_replace_unexpected_with_conds(tns,df2, unexpected_conditions, caplog):

    tns.replace_unexpected_values(unexpected_conditions = unexpected_conditions)

    assert "replacing missing values in category cols with missing types" in caplog.text
    assert "replacing all upper case characters with lower case" in caplog.text
    assert "replacing character unicode to latin" in caplog.text
    assert "replacing missing values in date cols with missing types" in caplog.text
    assert "replacing missing values in numeric cols with missing types" in caplog.text
    assert "replacing values outside of expected date range" in caplog.text
    assert "replacing values outside of expected numeric range" in caplog.text

    assert "replacing with additional cons" in caplog.text
    assert "Replace numeric missing with with zero" in caplog.text
    assert "Clean text column from '-ing' endings and 'not ' beginings" in caplog.text
    assert "Detect/Replace numeric values in certain column with zeros if > 2" in caplog.text
    assert "Replace strings with values if some part of the string is detected" in caplog.text


    assert "Usable values in the dataframe:  82.22%" in caplog.text
    assert "Uncorrected data quality score:  88.89%" in caplog.text
    assert "Corrected data quality score:  97.53%" in caplog.text

    assert tns.dataframe.equals(df2)


def test_get_refiner_settings(tns2,refiner_settings):

    refiner_settings2 = tns2.get_refiner_settings()

    assert refiner_settings2 == refiner_settings


def test_set_refiner_settings(tns2,df, refiner_settings):

    tns = Refiner(dataframe = df)

    tns.set_refiner_settings(refiner_settings)

    tns.shout(mess = "TNS1")
    tns.detect_unexpected_values()
    tns2.shout(mess = "TNS2")
    tns2.detect_unexpected_values()

    assert tns.duv_score == tns2.duv_score


#     @pytest.mark.parametrize("a,expected", [
#     (2, 4),
#     (6, 8)
# ])
# def test_my_function2(a,expected):

#     assert my_function2(a) is expected

# def test_invalid_val():
#     with pytest.raises(TypeError):
#         my_function2('2')


# def test_with_fixture(b):
#     assert my_function2(b) is 4
