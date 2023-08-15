from robot.api import logger
from typing import List
import pandas as pd


class DynamicTestCases(object):
    """A Robot Framework test library to dynamically add test cases to the current suite."""
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.current_suite = None

    def _start_suite(self, suite, result):
        self.current_suite = suite

    def add_test_case(self, name: str, doc: str, tags: List[str], kwname: str, **kwargs):
        """Adds a test case to the current suite.

        Args:
            | *Name*                  | *Type*   | *Description*                                                      |
            | `name`                  | `str`    | The test case name.                                                |
            | `doc`                   | `str`    | The documentation for the test case.                               |
            | `tags`                  | `str`    | Tags to be associated with the test case.                          |
            | `kwname`                | `str`    | The keyword to call.                                               |
            | `**kwargs`              | `str`    | Keyword arguments to be passed to the keyword.                     |

        Example:
        | Add Test Case | Example Test Case | This is a dynamic test case | ['smoke'] | My Keyword | arg1=value1 | arg2=value2 |
        """
        test_case = self.current_suite.tests.create(name=name, doc=doc, tags=tags)
        args = []
        for arg_name, arg_value in kwargs.items():
            args.append(f'{arg_name}={arg_value}')
        test_case.body.create_keyword(name=kwname, args=args)
        # self.suite.tests.append(test_case)

        logger.info(f"Added test case '{name}' with keyword '{kwname}' and keyword arguments:")
        for arg_name, arg_value in kwargs.items():
            logger.info(f"    {arg_name} = {arg_value}")

    def read_test_data_and_add_test_cases(self, csv_file_path: str):
        """Reads test data from a CSV file and adds test cases dynamically.

        Args:
            | *Name*                  | *Type*   | *Description*                                                      |
            | `csv_file_path`         | `str`    | The path to the CSV file containing test data.                    |

        The CSV file should have the following columns:
        - test_name (*str*): Name of the test case.
        - test_scenario (*str*): Description of the test scenario.
        - test_tags (*str*): Comma-separated tags for categorization.
        - keyword (*str*): The keyword associated with the test.
        - Any additional columns ending with '_v' (*str*): Additional parameters for the test case.

        Additionally, the 'tbe' column should be present to determine whether a test case should be added.
        Valid values for 'tbe' are: 'YES', 'yes', 'y' (case-insensitive).

        Example:
        | Read Test Data And Add Test Cases | /path/to/test_data.csv |
        """
        try:
            df = pd.read_csv(csv_file_path)

            # Filter rows based on values in the 'tbe' column
            filtered_df = df[df['tbe'].str.lower().isin(['yes', 'y'])]

            for _, row in filtered_df.iterrows():
                name = row.get('test_name', '')
                doc = row.get('test_scenario', '')
                tags = row.get('test_tags', '').split(',')
                kwname = row.get('keyword', '')
                kwargs = {col[:-2]: row[col] if pd.notna(row[col]) else None for col in df.columns if
                          col.endswith('_v')}
                # Remove keys with None values
                kwargs = {key: value for key, value in kwargs.items() if
                          value is not None}
                # kwargs = {col[:-2]: row[col] for col in df.columns if col.endswith('_v')}
                self.add_test_case(name=name, doc=doc, tags=tags, kwname=kwname, **kwargs)
            logger.info(f"Successfully added test cases from '{csv_file_path}'.")
        except Exception as e:
            logger.error(f"Error occurred while reading test data from '{csv_file_path}': {e}")
