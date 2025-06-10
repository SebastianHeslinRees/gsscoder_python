import pandas as pd
import numpy as np
import pickle
import pkg_resources

def load_pickle(filename):
    """Load data from pickle file in package's lookups directory"""
    path = pkg_resources.resource_filename(__name__, f"lookups/{filename}")
    with open(path, 'rb') as f:
        return pickle.load(f)

def validate_recode_gss(df_in, col_code, col_data, recode_to_year, recode_from_year, fun, la_names, database_year):
    """
    Validate inputs for recode_gss function
    """
    assert isinstance(df_in, pd.DataFrame), "df_in must be a pandas DataFrame"
    assert isinstance(col_code, str), "col_code must be a string"
    assert isinstance(col_data, (str, list)), "col_data must be a string or list of strings"
    assert isinstance(recode_to_year, (int, float)), "recode_to_year must be numeric"
    assert isinstance(recode_from_year, (int, float)), "recode_from_year must be numeric"
    assert fun in ['sum', 'mean'], "fun must be 'sum' or 'mean'"

    assert recode_from_year >= 2008, "recode_from_year must be 2008 or later"
    assert recode_from_year <= database_year, f"recode_from_year cannot be later than the database year ({database_year})"
    assert recode_to_year >= 2008, "recode_to_year must be 2008 or later"
    assert recode_to_year <= database_year, f"recode_to_year cannot be later than the database year ({database_year})"

    if isinstance(col_data, str):
        col_data = [col_data]

    for col in col_data:
        assert col in df_in.columns, f"{col} is not in the input DataFrame"
        assert np.issubdtype(df_in[col].dtype, np.number), f"{col} must be numeric"

    assert col_code in df_in.columns, f"{col_code} is not in the input DataFrame"

    poss_name_cols = df_in.select_dtypes(include=[object]).columns
    for col in poss_name_cols:
        if df_in[col].isin(la_names).any():
            print(f"Warning: LA names detected in column '{col}'. Consider removing this column.")

def recode_gss(
    df_in,
    col_code='gss_code',
    col_data='value',
    fun='sum',
    recode_from_year=None,
    recode_to_year=None,
    aggregate_data=True,
    lad_code_changes=None,
    all_lad_codes_dates=None,
    database_year=2024
):
    """
    Recode GSS codes between different year vintages.
    Handles splits/merges and optionally aggregates data.
    """

    # Automatically load package-internal data if not passed
    if all_lad_codes_dates is None:
        all_lad_codes_dates = load_pickle("all_lad_codes_dates.pickle")
    if lad_code_changes is None:
        lad_code_changes = load_pickle("lad_code_changes.pickle")

    la_names = all_lad_codes_dates['gss_name'].unique()

    validate_recode_gss(df_in, col_code, col_data, recode_to_year, recode_from_year, fun, la_names, database_year)

    df = df_in.copy()
    df.rename(columns={col_code: 'gss_code'}, inplace=True)

    code_changes = lad_code_changes.copy()

    if recode_to_year < recode_from_year:
        code_changes['split2'] = code_changes['merge']
        code_changes['merge2'] = code_changes['split']
        code_changes.drop(['split', 'merge'], axis=1, inplace=True)
        code_changes.rename(columns={
            'split2': 'split',
            'merge2': 'merge',
            'changed_to_code': 'tmp1',
            'changed_from_code': 'changed_to_code',
            'tmp1': 'changed_from_code',
            'changed_to_name': 'tmp2',
            'changed_from_name': 'changed_to_name',
            'tmp2': 'changed_from_name'
        }, inplace=True)
        code_changes['year'] -= 1

    lookup = pd.DataFrame(columns=['changed_from_code', 'changed_to_code'])

    for year in range(recode_from_year, recode_to_year + 1):
        new_rows = code_changes[
            (code_changes['changed_from_code'].isin(df['gss_code'])) & (code_changes['year'] == year)
        ][['changed_from_code', 'changed_to_code']]
        lookup = pd.concat([lookup, new_rows], ignore_index=True)

        update_rows = code_changes[
            (code_changes['changed_from_code'].isin(lookup['changed_to_code'])) & (code_changes['year'] == year)
        ][['changed_from_code', 'changed_to_code']]
        if not update_rows.empty:
            lookup = lookup.merge(update_rows, how='left', left_on='changed_to_code', right_on='changed_from_code')
            lookup['changed_to_code'] = np.where(
                lookup['changed_to_code_y'].notna(), lookup['changed_to_code_y'], lookup['changed_to_code']
            )
            lookup.drop(columns=['changed_to_code_y', 'changed_from_code_y'], inplace=True)

    lookup.drop_duplicates(inplace=True)
    lookup = lookup[lookup['changed_from_code'] != lookup['changed_to_code']]

    if lookup['changed_from_code'].duplicated().any():
        lookup = lookup.groupby('changed_from_code')['changed_to_code'].apply(lambda x: ', '.join(x.unique())).reset_index()

    df = df.merge(lookup, how='left', left_on='gss_code', right_on='changed_from_code')
    df['gss_code'] = df['changed_to_code'].fillna(df['gss_code'])
    df.drop(columns=['changed_from_code', 'changed_to_code'], inplace=True)

    if isinstance(col_data, str):
        col_data = [col_data]

    group_cols = [col for col in df.columns if col not in col_data]

    if aggregate_data:
        if fun == 'sum':
            df = df.groupby(group_cols, as_index=False)[col_data].sum()
        elif fun == 'mean':
            df = df.groupby(group_cols, as_index=False)[col_data].mean()

    df.rename(columns={'gss_code': col_code}, inplace=True)
    df = df[df_in.columns]

    return df
