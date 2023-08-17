import os
import filecmp
import difflib
import csv
from typing import List, Tuple
from typing import Union
import pandas as pd
import numpy as np
from robot.api import logger
from robot.api.deco import keyword


@keyword('Find Delimiter In File')
def find_delimiter(filename: str) -> Union[str, None]:
    """
    Find the delimiter used in a CSV file.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `filename`|  The name of the CSV file.

    `Returns:`
    | *`Type`* | *`Description`* |
    | `str` | `The delimiter used in the CSV file as a string.` |

    Examples:
    | ${delimiter} | Find Delimiter | example.csv |
    """
    _, ext = os.path.splitext(filename)

    if ext in ['.xls', '.xlsx']:
        logger.info(f'{filename} is an Excel file. Cannot find delimiter.')
        return None

    try:
        with open(filename, 'rb') as f:
            # Read a sample of the data to analyze the dialect
            sample = f.read(1024).decode()

            # List of delimiters to test
            delimiters = [',', '\t', ';', '|', ':', '~', '\x01']
            delimiter_str = "".join(delimiters)

            # Use csv.Sniffer to guess the dialect
            dialect = csv.Sniffer().sniff(sample, delimiters=delimiter_str)

        delimiter = chr(getattr(dialect, 'delimiter'))

        # Log the delimiter
        logger.info(f'The delimiter in {filename} is "{delimiter}"')

        return delimiter
    except UnicodeDecodeError:
        logger.info(f'{filename} is not a delimiter file')
        return None


@keyword(name="Create Dataframe From File")
def create_dataframe_from_file(file_path: str, delimiter: str = ',', has_header: bool = True,
                               width: list = None, colspecs: list = None,
                               column_names: list = None, dtypes: dict = None,
                               encoding: str = 'ISO-8859-1',
                               on_bad_lines: str = 'warn', skiprows: int = 0, skipfooter: int = 0):
    """
    Creates a Pandas DataFrame from a CSV, PSV, or fixed-width file.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `file_path`    | `(str)` | `The path to the input file.` |
    | `delimiter`    | `(str)` | The delimiter character used in the input file. Default is ','.` |
    | `has_header`   | `(bool)` | `Whether the input file has headers. Default is True.` |
    | `width`        | `(list or tuple)` | `A list or tuple of integers specifying the width of each fixed-width field. Required when reading a fixed-width file. Default is None.` |
    | `encoding`     | `(str)` | `The encoding of the input file. Default is 'ISO-8859-1'.` |
    | `on_bad_lines` | `(str)` | `What to do with bad lines encountered in the input file. Valid values are 'raise', 'warn', and 'skip'. Default is 'warn'.` |
    | `skiprows`     | `(int or list-like)` | `Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the file. Default is 0.` |
    | `skipfooter`   | `(int)` | `Number of lines to skip at the end of the file. Default is 0.` |

    `Returns:`
    | *`Type`* | *`Description`* |
    | `pandas.DataFrame` | `The DataFrame created from the input file.` |

    Examples:
    | Create Dataframe From File | /path/to/file.csv |
    | Create Dataframe From File | /path/to/file.psv | delimiter='|', has_header=False |
    | Create Dataframe From File | /path/to/file.xlsx | has_header=False |
    | Create Dataframe From File | /path/to/file.fwf | width=[10, 20, 30] |
    | Create Dataframe From File | /path/to/file.csv | encoding='utf-8', on_bad_lines='raise' |
    """

    # Set default dtype as 'str' if not provided
    if dtypes is None:
        dtypes = 'str'

    # Determine the file type based on the file extension
    file_ext = file_path.split('.')[-1].lower()
    if file_ext == 'csv':
        # Log info message
        logger.info(f"        Reading CSV file '{file_path}' with delimiter '{delimiter}' and encoding '{encoding}'")
        # Read CSV file into a DataFrame
        if has_header:
            df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, on_bad_lines=on_bad_lines,
                             skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)
        else:
            df = pd.read_csv(file_path, delimiter=delimiter, header=None, encoding=encoding, on_bad_lines=on_bad_lines,
                             skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)
    elif file_ext == 'psv':
        # Log info message
        logger.info(f"        Reading PSV file '{file_path}' with delimiter '|'")
        # Read PSV file into a DataFrame
        if has_header:
            df = pd.read_csv(file_path, delimiter='|', encoding=encoding, on_bad_lines=on_bad_lines, skiprows=skiprows,
                             skipfooter=skipfooter, dtype=dtypes)
        else:
            df = pd.read_csv(file_path, delimiter='|', header=None, encoding=encoding, on_bad_lines=on_bad_lines,
                             skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)
    elif file_ext == 'xlsx':
        # Log info message
        logger.info(f"        Reading Excel file '{file_path}'")
        # Read Excel file into a DataFrame
        if has_header:
            df = pd.read_excel(file_path, skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)
        else:
            df = pd.read_excel(file_path, header=None, skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)

    # elif file_ext == 'dat':
    #     # Log info message
    #     logger.info(f"Step 1: Reading fixed-width file '{file_path}' with width {width}")
    #     # Read fixed-width file into a DataFrame
    #     df = pd.read_fwf(file_path, widths=width, header=None, encoding=encoding, on_bad_lines=on_bad_lines,
    #                      skiprows=1, skipfooter=1, dtype=str)
    elif file_ext == 'dat' and delimiter is not None:
        # Log info message
        logger.info(f"        Reading delimited .dat file '{file_path}' with delimiter '{delimiter}'")
        # Read delimited .dat file into a DataFrame

        if has_header:
            try:
                df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, on_bad_lines=on_bad_lines,
                                 skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)

            except pd.errors.ParserError:
                print("Parser error encountered with CPython. Retrying with Python parser...")
                df_csv = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, on_bad_lines=on_bad_lines,
                                     skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes, engine='python')

                # Save the cleaned data to a CSV file
                write_df_to_csv(df_csv,'tmp_data_extract.csv', index=False)

                # Read the saved CSV file
                df = pd.read_csv('tmp_data_extract.csv')

        else:
            try:
                df = pd.read_csv(file_path, delimiter=delimiter, header=None, names=column_names,
                                 encoding=encoding, on_bad_lines=on_bad_lines,
                                 skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)
            except pd.errors.ParserError:
                print("Parser error encountered with CPython. Retrying with Python parser...")
                df_csv = pd.read_csv(file_path, delimiter=delimiter, header=None, names=column_names,
                                     encoding=encoding, on_bad_lines=on_bad_lines,
                                     skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes, engine='python')

                # Save the cleaned data to a CSV file
                write_df_to_csv(df_csv,'tmp_data_extract.csv', index=False)

                # Read the saved CSV file
                df = pd.read_csv('tmp_data_extract.csv')

    elif file_ext == 'dat' and width is not None:
        # Log info message
        logger.info(f"        Reading fixed-width file '{file_path}' with specified width")
        # Read fixed-width file into a DataFrame using width parameter
        df = pd.read_fwf(file_path, widths=width, header=None, names=column_names,
                         encoding=encoding, on_bad_lines=on_bad_lines,
                         skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)

    elif file_ext == 'dat' and colspecs is not None:
        # Log info message
        logger.info(f"        Reading fixed-width file '{file_path}' with specified colspecs")
        # Read fixed-width file into a DataFrame using colspecs parameter
        df = pd.read_fwf(file_path, colspecs=colspecs, header=None, names=column_names,
                         encoding=encoding, on_bad_lines=on_bad_lines,
                         skiprows=skiprows, skipfooter=skipfooter, dtype=dtypes)

    else:
        # Log error message and raise exception
        logger.error(
            f"Error: Unsupported file type '{file_ext}'. Supported file types are 'csv', 'psv', 'xlsx', and 'dat'.")
        raise Exception(f"Unsupported file type '{file_ext}'")

    # Log info message
    logger.info(f"        DataFrame created with {df.shape[0]} rows and {df.shape[1]} columns")
    # Return the DataFrame
    return df


@keyword("Write DataFrame To CSV File")
def write_df_to_csv(df_to_write: pd.DataFrame, file_path: str, file_name: str, index: bool = False):
    """
    Write the DataFrame to a CSV file.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `df_to_write`    | `pandas.DataFrame` | `The DataFrame to write to the CSV file.` |
    | `file_path`    | `str` | `The path where the CSV file needs to be created.` |
    | `file_name`    | `str` | `The name of the CSV file to be created.` |
    | `index`    | `bool` | `Whether to include the index in the CSV file. Default is False.` |

    `Returns:`
    | *`Type`* | *`Description`* |
    | `None`    | `This method does not return anything.` |

    Examples:
    | Write DataFrame To CSV File | ${df} | /path/to/file/ | example.csv |
    | Write DataFrame To CSV File | ${df} | /path/to/file/ | example.csv | True |
    """
    logger.info('Step 1: Writing DataFrame to CSV file...')
    try:
        df_to_write.to_csv(path_or_buf=file_path + '/' + file_name, mode='w', index=index)
        logger.info('Step 2: Writing DataFrame to CSV file completed successfully.')
    except Exception as e:
        logger.error(f'Step 2: Writing DataFrame to CSV file failed with error: {e}')


@keyword("Write DataFrame To PSV File")
def write_df_to_psv(df_to_write: pd.DataFrame, file_path: str, file_name: str):
    """
    Write the DataFrame to a PSV (pipe-separated values) file.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `df_to_write` | `pandas.DataFrame` | `The DataFrame to write to the PSV file.` |
    | `file_path` | `str` | `The path where the PSV file needs to be created.` |
    | `file_name` | `str` | `The name of the PSV file to be created.` |

    `Returns:`
    | *`Type`* | *`Description`* |
    | `None` | `This method does not return anything.` |

    Examples:
    | Write DataFrame To PSV File | ${df} | /path/to/file/ | example.psv |
    """

    logger.info('Step 1: Writing DataFrame to PSV file...')
    try:
        df_to_write.to_csv(path_or_buf=file_path + '/' + file_name, mode='w', sep='|', index=False)
        logger.info('Step 2: Writing DataFrame to PSV file completed successfully.')
    except Exception as e:
        logger.error(f'Step 2: Writing DataFrame to PSV file failed with error: {e}')


@keyword("Compare All File Contents In Directories")
def df_diff(actual_file_path_name: str, expected_file_path_name: str, delimiter: str = ',', has_header: bool = True,
            width: list = None, colspecs: list = None, column_names: list = None, dtypes: dict = None,
            encoding: str = 'ISO-8859-1', on_bad_lines: str = 'warn', skiprows: int = 0, skipfooter: int = 0,
            key_columns: list = None, ignore_columns: list = None, report_type: str = 'all'):
    """
    Compare the difference between two files' contents and generate a detailed mismatch report.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `actual_file_path_name` | `(str)` | `The path to the first file containing the actual DataFrame to compare.` |
    | `expected_file_path_name` | `(str)`  | `The path to the second file containing the expected DataFrame to compare.` |
    | `delimiter` | `(str)` | `The delimiter character used in the input files. Default is ','.` |
    | `has_header` | `(bool)` | `Whether the input files have headers. Default is True.` |
    | `width` | `(list or tuple)` | `A list or tuple of integers specifying the width of each fixed-width field. Required when reading a fixed-width file. Default is None.` |
    | `colspecs` | `(list or tuple)` | `A list or tuple of pairs (int, int) specifying the column ranges for fixed-width fields. Required when reading a fixed-width file. Default is None.` |
    | `column_names` | `(list)` | `A list of column names to use if the input files do not have headers.` |
    | `dtypes` | `(dict)` | `A dictionary specifying the data types of columns in the DataFrame.` |
    | `encoding` | `(str)` | `The encoding of the input files. Default is 'ISO-8859-1'.` |
    | `on_bad_lines` | `(str)` | `What to do with bad lines encountered in the input files. Valid values are 'raise', 'warn', and 'skip'. Default is 'warn'.` |
    | `skiprows` | `(int or list-like)` | `Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the files. Default is 0.` |
    | `skipfooter` | `(int)` | `Number of lines to skip at the end of the files. Default is 0.` |
    | `key_columns` | `(list)` | `A list of column names to use as the primary keys for the comparison.` |
    | `ignore_columns` | `(list)` | `A list of column names to ignore during the comparison.` |
    | `report_type` | `(str)` | `The type of report to generate. Valid values are 'all', 'duplicate', or 'key_mismatch'. Default is 'all'.` |

    `Returns:`
    | *`Type`* | *`Description`* |
    | `pandas.DataFrame` | `A DataFrame containing the rows that are different between the two input DataFrames.` |

    Examples:
    | ${df1} | Read CSV | path/to/actual.csv |
    | ${df2} | Read CSV | path/to/expected.csv |
    | ${diff} | Compare All File Contents In Directories | ${df1} | ${df2} | key_columns=['col1', 'col2'] | ignore_columns=['col3'] |
    """

    logger.info('****************************************************************************************************')
    logger.info('PandasUtil Data Frame Comparison - Cell by Cell comparison with detailed mismatch report')
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Based on file format create the data frames with delimiter(sep)')

    df1 = create_dataframe_from_file(actual_file_path_name, delimiter, has_header, width, colspecs, column_names,
                                     dtypes, encoding, on_bad_lines, skiprows, skipfooter)
    df2 = create_dataframe_from_file(expected_file_path_name, delimiter, has_header, width, colspecs, column_names,
                                     dtypes, encoding, on_bad_lines, skiprows, skipfooter)

    # Store total records in actual and expected df
    total_expected = round(len(df1))
    total_actual = round(len(df2))
    total_mismatch = total_expected - total_actual

    logger.info('Step-02 : Remove the columns based on ignore columns list')
    # If ignore columns are specified, remove those columns from comparison
    if len(ignore_columns) > 0:
        # Get column index type
        col_idx = df1.columns.get_loc(df1.columns.tolist()[0])

        # Iterate all the columns in ignore column list and if the column exist delete the column
        for col in ignore_columns:
            # Based on the column index type delete the column
            if isinstance(col_idx, int):
                if int(col) in df1.columns.tolist():
                    df1.drop(df1.columns[int(col)], axis=1, inplace=True)
            elif isinstance(col_idx, str):
                if col in df1.columns.tolist():
                    df1.drop(df1.columns[col], axis=1, inplace=True)

            if isinstance(col_idx, int):
                if int(col) in df2.columns.tolist():
                    df2.drop(df2.columns[int(col)], axis=1, inplace=True)
            elif isinstance(col_idx, str):
                if col in df2.columns.tolist():
                    df2.drop(df2.columns[col], axis=1, inplace=True)

    logger.info('Step-03 : Check for duplicate rows in both actual and expected')

    # Check for column differences in df1 and df2
    df1_col_diff = set(df1.columns) - set(df2.columns)
    df2_col_diff = set(df2.columns) - set(df1.columns)

    logger.debug(df1_col_diff)
    df1_col_diff = set(df1.columns) - set(df2.columns)

    # If key column is not specified then consider all columns except last column
    if len(key_columns) == 0:
        key_columns = df1.columns.tolist()
        key_columns.pop()

    # Sort both expected and actual data frame
    df1.sort_values(by=key_columns, ascending=True, inplace=True)
    df2.sort_values(by=key_columns, ascending=True, inplace=True)

    # Check for duplicate key columns in expected and actual data frame
    df1_dup_df = df1[df1[key_columns].duplicated()]
    df2_dup_df = df2[df2[key_columns].duplicated()]

    logger.debug(df1_dup_df)
    logger.debug(df2_dup_df)
    logger.debug(len(df1_dup_df))
    logger.debug(len(df2_dup_df))

    total_expected_dup = round(len(df1_dup_df))
    total_actual_dup = round(len(df2_dup_df))

    logger.info('Step-04 : Remove duplicate records from actual and expected')

    # Get the duplicate key columns
    dup_expected_df = df1_dup_df.copy()
    dup_actual_df = df2_dup_df.copy()
    dup_expected_df['source'] = 'Expected'
    dup_actual_df['source'] = 'Actual'

    # Combine the duplicate keys from expected and actual data frame
    dup_cons_df = pd.concat([dup_expected_df, dup_actual_df], axis=0)
    dup_cons_df.reset_index(inplace=True)
    dup_cons_df.drop('index', axis=1, inplace=True)

    # Drop the duplicate columns before detailed comparison
    df1.drop_duplicates(key_columns, inplace=True)
    df2.drop_duplicates(key_columns, inplace=True)

    logger.debug(dup_expected_df)
    logger.debug(dup_actual_df)
    logger.debug(dup_cons_df)

    logger.info('Step-05 : Sort the actual and expected based on key columns and reset the index')

    # Sort df1 and df2 based on key columns and reset the index
    df1.sort_values(by=key_columns, ascending=True, inplace=True)
    df2.sort_values(by=key_columns, ascending=True, inplace=True)
    df1.reset_index(inplace=True)
    df2.reset_index(inplace=True)

    # Set the index based on key columns in df1 and df2. Remove the default index column
    df1 = df1.set_index(key_columns, drop=True, append=False, inplace=False, verify_integrity=True)
    df2 = df2.set_index(key_columns, drop=True, append=False, inplace=False, verify_integrity=True)
    df1 = df1.drop('index', axis=1)
    df2 = df2.drop('index', axis=1)

    logger.info('Step-06 : Identify the rows matching based on key in both actual and expected')

    # Identify the rows matching based on key in both df1 and df2
    merge_outer_df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True, indicator='source')
    # merge_outer_df = pd.merge(df1_key_columns, df2_key_columns, how='outer', on=key_columns, indicator='source')

    # Based on the key columns create key matched and mismatched details
    key_matched_df = merge_outer_df.loc[merge_outer_df['source'] == 'both'].copy()
    logger.debug(len(key_matched_df))
    key_mismatched_df = merge_outer_df.loc[merge_outer_df['source'] != 'both'].copy()
    key_mismatched_df = key_mismatched_df[['source']]

    # key_matched_df['source'] = 'Matched'
    # key_mismatched_df['source'] = 'MisMatched'
    logger.debug(key_mismatched_df)

    # Update the source column left_only to actual and right_only to expected
    # key_mismatched_df.loc[key_mismatched_df['source'] == 'left_only', 'source'] = 'Actual'

    expected_key_mismatch = len(key_mismatched_df[key_mismatched_df.source == 'left_only'])
    actual_key_mismatch = len(key_mismatched_df[key_mismatched_df.source == 'right_only'])

    logger.info('Step-07 : Create the summary report based on count diff, duplicate rows and key mismatches')

    # Create the executive summary df
    exec_summary_col = ['Summary', 'Expected', 'Actual', 'Mismatch']

    exec_summary_df = pd.DataFrame(columns=exec_summary_col)
    exec_summary_df.loc[1] = ['Total_Records', total_expected, total_actual, total_mismatch]
    exec_summary_df.loc[2] = ['Duplicates', total_expected_dup, total_actual_dup, 0]
    exec_summary_df.loc[3] = ['Key_Mismatch', expected_key_mismatch, actual_key_mismatch, 0]

    logger.debug(exec_summary_df)

    logger.info('Step-08 : Remove the mismatched key values and proceed further in validation')
    df1.drop(key_mismatched_df.loc[key_mismatched_df['source'] == 'left_only'].index, inplace=True)
    df2.drop(key_mismatched_df.loc[key_mismatched_df['source'] == 'right_only'].index, inplace=True)

    # Step-08 to Step-12: Handle different report types
    if report_type == 'all':
        # Continue with all the comparison steps and generate all reports
        pass
    elif report_type == 'duplicate':
        # Return only the duplicate records report and exit the function
        logger.info('Step-09 : Comparison completed and generated info for reports(summary, duplicate')
        logger.info('************************************************************************************************')
        return exec_summary_df, dup_cons_df
    elif report_type == 'key_mismatch':
        # Return only the key mismatch report and exit the function
        logger.info('Step-09 : Comparison completed and generated info for reports(summary, key_mismatch')
        logger.info('************************************************************************************************')
        return exec_summary_df, key_mismatched_df
    else:
        # Invalid report type specified, raise an exception
        raise ValueError("Invalid 'report_type' specified. Valid values are 'all', 'duplicate', or 'key_mismatch'.")

    logger.info('Step-09 : Started cell by cell comparison for key values that exist in both actual and expected')

    # Verify if columns in both df1 and df2 are same
    if not df1.columns.equals(df2.columns):
        logger.debug('Failed - Column mismatch determined')
        # Handle the column mismatch case here if needed
        # ...

    logger.info('Step-10 : Verify column data types in both the files, if not convert based on actual')
    if not df1.dtypes.equals(df2.dtypes):
        logger.debug('Data Types are different, trying to convert')
        df2 = df2.astype(df1.dtypes)

    logger.info('Step-11 : Verify cell by cell data in both the data frame and generate mismatch report')

    # Identify where cells are different and generate a boolean mask
    diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())

    # Create a DataFrame with mismatched cells
    cell_comp_df = df1.where(diff_mask).stack().reset_index()
    key_columns_names = key_columns if isinstance(key_columns, list) else [key_columns]
    cell_comp_df.columns = key_columns_names + ['Column', 'Expected_Data']

    def get_index_value(row):
        if len(key_columns_names) > 1:
            return tuple(row[key] for key in key_columns_names)
        else:
            return row[key_columns_names[0]]

    # Apply the helper function to get index values
    cell_comp_df['Index_Value'] = cell_comp_df.apply(get_index_value, axis=1)

    # Use Index_Value to fetch Actual_Data
    cell_comp_df['Actual_Data'] = cell_comp_df.apply(
        lambda row: df2.at[row['Index_Value'], row['Column']],
        axis=1
    )

    # Add a 'Compare_Result' column
    cell_comp_df['Compare_Result'] = np.where(cell_comp_df['Expected_Data'] != cell_comp_df['Actual_Data'],
                                              'Mismatch', 'Match')

    # Drop the Index_Value column before returning
    cell_comp_df = cell_comp_df.drop(columns=['Index_Value'])

    logger.info('Step-12 : Comparison completed and generated info for reports(summary, keys mismatch, cell by cell)')
    logger.info('****************************************************************************************************')

    return exec_summary_df, dup_cons_df, key_matched_df, key_mismatched_df, cell_comp_df


@keyword('Compare All Files In Directories')
def files_diff(src_dir: str, tgt_dir: str) -> pd.DataFrame:
    """
    Compare all files in source and target directories and return a DataFrame with the comparison results.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `src_dir` | `str` | `The source directory to compare.` |
    | `tgt_dir` | `str` | `TThe target directory to compare.` |

    `Returns:`
    | *`Type`* | *`Description`* |
    | `pd.DataFrame` | `A DataFrame containing the comparison results, including file name, status, comments, and size in both directories.` |

    Examples:
    | ${result}= | Files Diff | ${source_dir} | ${target_dir} |
    | ${result}= | Files Diff | /path/to/source/dir | /path/to/target/dir |
    """

    logger.info(f"Step 1: Log the comparison directories")
    logger.info(f"Comparing files in {src_dir} and {tgt_dir}")

    common_files = find_common_files(src_dir, tgt_dir)

    match, mismatch, errors = compare_files(src_dir, tgt_dir, common_files)

    only_in_src = find_files_only_in_dir(src_dir, common_files)

    only_in_tgt = find_files_only_in_dir(tgt_dir, common_files)

    df = create_comparison_df(match, mismatch, errors, only_in_src, only_in_tgt, src_dir, tgt_dir)

    logger.info(f"Step 10: Created File Comparison Report - {len(df)} Files")
    return df


@keyword('Find Common Files In Directories')
def find_common_files(src_dir: str, tgt_dir: str) -> List[str]:
    """
    Find files that exist in both directories.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `src_dir` | `str` | `The source directory.` |
    | `tgt_dir` | `str` | `The target directory.` |

    `Returns:`
    | *`Type`* | *`Description`* |
    | `List[Tuple[str, str]]` | `A list of tuples containing file paths, one for each file that exists in both directories.` |

    Examples:
    | ${result}= | Find Common Files | ${source_dir} | ${target_dir} |
    | ${result}= | Find Common Files | /path/to/source/dir | /path/to/target/dir |
    """
    logger.info(f"Step 2: Find common files in source and target directories")
    common_files = []
    for file in os.listdir(src_dir):
        if file in os.listdir(tgt_dir):
            common_files.append(file)
    return common_files


def compare_files(src_dir: str, tgt_dir: str, common_files: List[str]) -> Tuple[List[Tuple[str, int, int]],
List[Tuple[str, int, int, float]],
List[Tuple[str, str]]]:
    """
    Compare the files in the source and target directories.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `src_dir` | `str` | `The source directory.` |
    | `tgt_dir` | `str` | `The target directory.` |
    | `files` | `list` | `A list of files to compare.` |

    `Returns:`
    | *`Type`* | *`Description`* |
    | `tuple` | `A tuple containing lists of matching files, mismatching files with percentage difference, and files with errors.` |

    Examples:
    | ${src_dir} | Set Variable | /path/to/source |
    | ${tgt_dir} | Set Variable | /path/to/target |
    | @{common_files} | Create List | file1.txt | file2.txt |
    | ${match_files} | ${mismatch_files} | ${error_files} | Compare Files | ${src_dir} | ${tgt_dir} | @{common_files} |
    | Log List | ${match_files} |
    | Log List | ${mismatch_files} |
    | Log List | ${error_files} |

    """
    match = []
    mismatch = []
    errors = []

    logger.info(f"Step 3: Compare each common file")
    for file in common_files:
        try:
            src_path = os.path.join(src_dir, file)
            tgt_path = os.path.join(tgt_dir, file)

            src_size = os.path.getsize(src_path)
            tgt_size = os.path.getsize(tgt_path)

            result = filecmp.cmpfiles(src_dir, tgt_dir, [file], shallow=False)
            if result[0]:
                match.append((file, src_size, tgt_size))
            else:
                diff_percentage = compare_file_contents(src_path, tgt_path)
                mismatch.append((file, src_size, tgt_size, diff_percentage))
        except Exception as e:
            errors.append((file, str(e)))

    return match, mismatch, errors


@keyword('Compare Files Using Diff')
def compare_file_contents(src_path: str, tgt_path: str) -> float:
    """
    Compares file contents using difflib and returns the percentage difference.

    Args:
        src_path (str): The source file path to compare.
        tgt_path (str): The target file path to compare.

    Returns:
        float: The percentage difference between the two files.

    Robot Framework Usage:
    | ${diff_percentage} | Compare File Contents | ${src_path} | ${tgt_path} |

    Examples:
    | ${diff_percentage} | Compare File Contents | /path/to/source/file.txt | /path/to/target/file.txt |
    """
    logger.info(f"Step 4: Compare file contents for {src_path} and {tgt_path}")
    with open(src_path, 'r') as f1, open(tgt_path, 'r') as f2:
        src_lines = f1.readlines()
        tgt_lines = f2.readlines()

    matcher = difflib.SequenceMatcher(None, src_lines, tgt_lines)
    diff_percentage = 100.0 - matcher.ratio() * 100.0

    return round(diff_percentage, 2)


def find_files_only_in_dir(directory: str, common_files: List[str]) -> List[str]:
    """
    Finds files that exist only in a directory and not in the common files list.

    Args:
        directory (str): The directory to search.
        common_files (List[str]): A list of common files.

    Returns:
        List[str]: A list of files that exist only in the directory.

    Robot Framework Usage:
        | *Arguments* |              |
        | directory   | ${dir_path}  |
        | common_files| @{common_files}|
        |             |              |
        | *Returns*   |              |
        |             | @{only_in_dir}|

    Examples:
        | ${common_files}= |  find common files | /path/to/source | /path/to/target |
        | ${only_in_source}= | find files only in dir | /path/to/source | ${common_files} |
        | ${only_in_target}= | find files only in dir | /path/to/target | ${common_files} |
    """
    logger.info(f"Step 4: Find files that exist only in {directory}")
    only_in_dir = []
    for file in os.listdir(directory):
        if file not in common_files:
            only_in_dir.append(file)
    return only_in_dir


@keyword("Create Comparison Dataframe")
# @keyword("Create Comparison Dataframe")
def create_comparison_df(match: List[Tuple[str, int, int]],
                         mismatch: List[Tuple[str, int, int, float]],
                         errors: List[Tuple[str, str]],
                         only_in_src: List[str],
                         only_in_tgt: List[str],
                         src_dir: str,
                         tgt_dir: str) -> pd.DataFrame:
    """
    Creates a DataFrame containing the comparison results.

    Args:
        match (List[Tuple[str, int, int]]): A list of matching files and their sizes.
        mismatch (List[Tuple[str, int, int, float]]): A list of mismatching files, their sizes, and the percentage difference.
        errors (List[Tuple[str, str]]): A list of files with errors and the error message.
        only_in_src (List[str]): A list of files only in the source directory.
        only_in_tgt (List[str]): A list of files only in the target directory.
        src_dir (str): Path to the source directory.
        tgt_dir (str): Path to the target directory.

    Returns:
        pd.DataFrame: A DataFrame containing the comparison results, including file name, status, comments, and size in both directories.
    """
    logger.info(f"Step 4: Create comparison DataFrame")
    data = []

    # Add matching files
    for file, src_size, tgt_size in match:
        data.append({"FileName": file,
                     "Status": "MATCH",
                     "Comments": "",
                     "Common_File": "Yes",
                     "Src_Size": src_size,
                     "Tgt_Size": tgt_size,
                     "Diff_Percentage": ""})

    # Add mismatching files
    for file, src_size, tgt_size, diff_percentage in mismatch:
        data.append({"FileName": file,
                     "Status": "MISMATCH",
                     "Comments": f"Percentage Difference: {diff_percentage:.2f}%",
                     "Common_File": "Yes",
                     "Src_Size": src_size,
                     "Tgt_Size": tgt_size,
                     "Diff_Percentage": diff_percentage})

    # Add files with errors
    for file, error in errors:
        data.append({"FileName": file,
                     "Status": "ERROR",
                     "Comments": error,
                     "Common_File": "Yes",
                     "Src_Size": "",
                     "Tgt_Size": "",
                     "Diff_Percentage": ""})

    # Add files only in source directory
    for file in only_in_src:
        data.append({"FileName": file,
                     "Status": "ONLY IN SRC",
                     "Comments": "",
                     "Common_File": "No",
                     "Src_Size": os.path.getsize(os.path.join(src_dir, file)),
                     "Tgt_Size": "",
                     "Diff_Percentage": ""})

    # Add files only in target directory
    for file in only_in_tgt:
        data.append({"FileName": file,
                     "Status": "ONLY IN TGT",
                     "Comments": "",
                     "Common_File": "No",
                     "Src_Size": "",
                     "Tgt_Size": os.path.getsize(os.path.join(tgt_dir, file)),
                     "Diff_Percentage": ""})

    df = pd.DataFrame(data, columns=["FileName", "Common_File", "Src_Size", "Tgt_Size", "Diff_Percentage", "Status",
                                     "Comments"])

    return df


@keyword('Compare All Files In Directories With Diffs')
def files_diff_with_diffs(src_dir: str, tgt_dir: str) -> None:
    """
    Compare all files in source and target directories and print the comparison results with diffs for matching files.

    `Args:`
    | *`Name`* | *`Type`* | *`Description`* |
    | `src_dir` | `str` | `The source directory to compare.` |
    | `tgt_dir` | `str` | `TThe target directory to compare.` |

    `Returns:`
    | `None` |  |

    Examples:
    | Files Diff With Diffs | ${source_dir} | ${target_dir} |
    | Files Diff With Diffs | /path/to/source/dir | /path/to/target/dir |
    """

    logger.info(f"Step 0: Starting comparison of files in {src_dir} and {tgt_dir}")

    # Call files_diff to get a dataframe of comparison results
    df = files_diff(src_dir, tgt_dir)

    # Loop through the matching files and print diffs
    for _, row in df[df['Status'] == 'Match'].iterrows():
        src_file = os.path.join(src_dir, row['File Name'])
        tgt_file = os.path.join(tgt_dir, row['File Name'])
        df_diff(src_file, tgt_file)
