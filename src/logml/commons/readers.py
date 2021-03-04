import os

import pandas as pd

UNALLOWED_CHARACTERS = ' -[]()+\'/,'


def sanitize_column(col_name, replace_dot=False):
    """
    Replaces unallowed characters in a given column name, casts to lower case.
    Additional rules/flags could be added.
    """
    col_name = col_name.strip().lower()

    for ch in UNALLOWED_CHARACTERS:
        col_name = col_name.replace(ch, '_')

    if replace_dot:
        col_name = col_name.replace('.', '_')

    col_name = col_name.replace('%', 'perc')

    return col_name


def load_csv(csv_path: str,
             parse_dates=None,
             dateformat=None,
             thousands=None,
             datetime_errors='raise',
             sep=',',
             encoding='utf-8',
             col_prefix="",
             has_header='infer',
             sanitize_columns=False,
             replace_dot=True):
    """Utility for loading a given file.

    In case a given input is csv file, additional parsing flags are applied.
    """
    df = pd.DataFrame()
    is_feather = csv_path.endswith('feather')
    is_parquet = csv_path.endswith('parquet')
    is_excel = csv_path.endswith('xlsx')

    try:
        if is_parquet:
            df = pd.read_parquet(csv_path)
        elif is_excel:
            df = pd.read_excel(csv_path)
        elif is_feather:
            df = pd.read_feather(csv_path)
        else:
            if not os.path.exists(csv_path):
                logging.debug("%s not found; loading .gz archive", csv_path)
                csv_path = "%s.gz" % csv_path

            df = pd.read_csv(
                csv_path,
                sep=sep,
                encoding=encoding,
                header=has_header,
                thousands=thousands
            )

        if sanitize_columns and has_header:
            df.columns = [col_prefix + sanitize_column(x, replace_dot)
                          for x in df.columns]

        if not is_parquet and not is_feather:
            if parse_dates:
                for col in parse_dates:
                    df[col] = pd.to_datetime(
                        df[col], format=dateformat, errors=datetime_errors)

    except Exception as e:
        raise Exception(f'Loading file \'{csv_path}\' failed, error: {e}')

    return df
