import pytest
from refineryframe.detect_unexpected import check_missing_types, \
    check_missing_values, check_inf_values, check_date_format, \
        check_duplicates, check_col_names_types, check_numeric_range, \
            check_date_range, check_duplicate_col_names, add_index_to_duplicate_columns, \
                detect_unexpected_values



def test_check_missing_types_int_error(df1):
    with pytest.raises(ValueError):
        check_missing_types(df1,
                            MISSING_TYPES={
                        'numeric_not_delivered': -999},
                            throw_error=True)

def test_check_missing_types_date_error(df1):
    with pytest.raises(ValueError):
        check_missing_types(df1,
                            MISSING_TYPES={'date_not_delivered': '1850-01-09'},
                            throw_error=True)

def test_check_missing_types_cat_error(df1):
    with pytest.raises(ValueError):
        check_missing_types(df1,
                            MISSING_TYPES={'character_not_delivered': 'missing'},
                            throw_error=True)

def test_check_missing_types_exc_error(df1):
    with pytest.raises(AttributeError):
        check_missing_types(df1,
                            MISSING_TYPES=-1,
                            throw_error=True)

def test_check_missing_types_scores_error(df1, MISSING_TYPES):
    with pytest.raises(ValueError):
        check_missing_types(df1,
                            MISSING_TYPES=MISSING_TYPES,
                            independent=False,
                            throw_error=True)

def test_check_missing_types_scores_check_error(df, MISSING_TYPES):

    cmt_obj = check_missing_types(df,
                            MISSING_TYPES=MISSING_TYPES,
                            independent=False,
                            throw_error=False)

    assert cmt_obj['scores']['cmt_scores']['numeric_score'] == 100
    assert cmt_obj['scores']['cmt_scores']['date_score'] == 100
    assert cmt_obj['scores']['cmt_scores']['cat_score'] == 97.78


#############

def test_check_missing_values_error(df):
    with pytest.raises(ValueError):
        check_missing_values(df,
                             throw_error=True)

def test_check_missing_values_scores_check_error(df):

    cmv_obj = check_missing_values(df,
                            independent=False,
                            throw_error=False)

    assert cmv_obj['scores']['cmv_scores']['missing_values_score'] == 53.33


#################

def test_check_inf_values_error(df):
    with pytest.raises(ValueError):
        check_inf_values(df,
                         throw_error=True)

def test_check_inf_values_print_error(caplog):

    check_inf_values(-1,
                     throw_error=False)

    assert "Error occured while checking inf values!" in caplog.text

################

def test_check_date_format_error(df):
    with pytest.raises(ValueError):
        check_date_format(df,
                          throw_error=True)

def test_check_date_format_print_error(caplog):

    check_date_format(-1,
                      throw_error=False)

    assert "Error occurred while checking date format!" in caplog.text


def test_check_date_format_scores_check_error(df):

    cdf_obj = check_date_format(df,
                                independent=False,
                                throw_error=False)

    assert cdf_obj['scores']['cdf_scores']['date_format_score'] == 50.0


########

def test_check_duplicates_error(df2):
    with pytest.raises(ValueError):
        check_duplicates(df2,
                         subset=['NumericColumn'],
                         throw_error=True)


def test_check_duplicates_error2(df_dup):
    with pytest.raises(ValueError):
        check_duplicates(df_dup,
                         subset=['num_id'],
                         throw_error=True)

def test_check_duplicates_error3(df_dup):
    with pytest.raises(ValueError):
        check_duplicates(df_dup,
                         throw_error=True)


def test_check_duplicates_error(df_dup):

    dup_obj = check_duplicates(df_dup,
                               independent=False,
                               throw_error=False)

    assert dup_obj['scores']['dup_scores']['row_dup_score'] == 83.33
    assert dup_obj['scores']['dup_scores']['key_dup_score'] == 100.0

##############


def test_check_col_names_types_error(df, types_dict_str):
    with pytest.raises(ValueError):
        check_col_names_types(df,
                              types_dict_str,
                              throw_error=True)

def test_check_col_names_types_error2(df, types_dict_str2):
    with pytest.raises(ValueError):
        check_col_names_types(df,
                              types_dict_str2,
                              throw_error=True)

def test_check_col_names_types_error3(df, types_dict_str3):
    with pytest.raises(ValueError):
        check_col_names_types(df,
                              types_dict_str3,
                              throw_error=True)

def test_check_col_names_types_error4(df, types_dict_str3, caplog):

    check_col_names_types(df,
                            types_dict_str3,
                            throw_error=False)

    assert "Error occured while checking column names and types" in caplog.text

def test_check_col_names_types_scores_check_error(df, types_dict_str):

    ccnt_obj = check_col_names_types(df,
                                     types_dict_str,
                            independent=False,
                            throw_error=False)

    assert ccnt_obj['scores']['ccnt_scores']['missing_score'] == 100.0
    assert ccnt_obj['scores']['ccnt_scores']['incorrect_dtypes_score'] == 88.89

##########

def test_check_numeric_range_lower_error(df):
    with pytest.raises(ValueError):
        check_numeric_range(df,
                            numeric_cols=['NumericColumn','NumericColumn_exepted'],
                              lower_bound=0,
                              throw_error=True)

def test_check_numeric_range_upper_error(df):
    with pytest.raises(ValueError):
        check_numeric_range(df,
                            numeric_cols=['NumericColumn','NumericColumn_exepted'],
                              upper_bound=0.5,
                              throw_error=True)

def test_check_numeric_range_error(caplog):

    check_numeric_range(-1,
                        throw_error=False)

    assert "Error occurred while checking numeric ranges!" in caplog.text

def test_check_numeric_range_scores_check_error(df):

    cnr_obj = check_numeric_range(df[['num_id','NumericColumn','NumericColumn_exepted','NumericColumn2','NumericColumn3']],
                                  lower_bound=0,
                                  upper_bound=3,
                                  independent=False,
                                  throw_error=False)

    assert cnr_obj['scores']['cnr_scores']['low_numeric_score'] == 93.33
    assert cnr_obj['scores']['cnr_scores']['upper_numeric_score'] == 80.0

###############

def test_check_date_range_error(df1):
    with pytest.raises(ValueError):
        check_date_range(df1,
                         throw_error=True)

def test_check_date_range_error(df1):
    with pytest.raises(ValueError):
        check_date_range(df1,
                         throw_error=True)

def test_check_date_range_error2(caplog):

    check_date_range(-1,
                     throw_error=False)

    assert "Error occured while checking date ranges!" in caplog.text

def test_check_date_range_error3(df1, caplog):

    EE = check_date_range(df1,
                      independent=True,
                      throw_error=False)

    assert EE == False


def test_check_date_range_early_error(df1):
    with pytest.raises(ValueError):
        check_date_range(df1,
                         earliest_date=['DateColumn3'],
                         throw_error=True)

def test_check_date_range_latest_error(df1):
    with pytest.raises(ValueError):
        check_date_range(df1,
                         latest_date=['DateColumn2'],
                         throw_error=True)


def test_check_date_range_scores_ckeck_error(df):

    cdr_obj = check_date_range(df[['DateColumn','DateColumn2']],
                 earliest_date="2023-01-01",
                 latest_date='2021-01-01',
                    independent=False,
                    silent = False)

    assert cdr_obj['scores']['cdr_scores']['early_dates_score'] == 60.0
    assert cdr_obj['scores']['cdr_scores']['future_dates_score'] == 60.0

############

def test_check_duplicate_col_names_error(df_dup2):
    with pytest.raises(ValueError):
        check_duplicate_col_names(df_dup2,
                                  throw_error=True)

def test_check_duplicate_col_names_error2(caplog):

    check_duplicate_col_names(-1,
                                throw_error=False)

    assert "Error occured while checking duplicates!" in caplog.text

def test_add_index_to_duplicate_columns_error(df_dup2):
    with pytest.raises(ValueError):
        add_index_to_duplicate_columns(df_dup2,
                                       column_name_freq= {})

def test_add_index_to_duplicate_columns_error2(df_dup2):

    df2 = add_index_to_duplicate_columns(df_dup2,
                                       column_name_freq= {'num_id': 1,
                                                'NumericColumn': 2,
                                                'NumericColumn_exepted': 1,
                                                'NumericColumn2': 1,
                                                'NumericColumn3': 1,
                                                'DateColumn': 1,
                                                'DateColumn2': 1,
                                                'DateColumn3': 1,
                                                'CharColumn': 1})

    assert list(df2.columns) == ['num_id', 'NumericColumn_(1)', 'NumericColumn_(2)',
       'NumericColumn_exepted', 'NumericColumn2', 'NumericColumn3',
       'DateColumn', 'DateColumn2', 'DateColumn3', 'CharColumn']


def test_detect_unexpected_values_error(df_dup2):

    df2 = detect_unexpected_values(df_dup2)

    assert df2['duv_score'] == 0.8