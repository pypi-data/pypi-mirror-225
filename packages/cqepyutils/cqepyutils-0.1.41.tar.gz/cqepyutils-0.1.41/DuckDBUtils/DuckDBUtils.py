import duckdb
import os
import pandas as pd

# Declare variables
DATABASE = ':memory:'
SRC_PATH = 'src_path.dat'
TRG_PATH = 'trg_path.dat'
MAPPING_FILE = 'Mapping.xlsx'
PRIMARY_KEYS = ['key_column1', 'key_column2']

# Initialize DuckDB connection
conn = duckdb.connect(database=DATABASE, read_only=False)


def load_data_into_duckdb(file_path, table_name):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.dat':
        mapping_df = pd.read_excel(MAPPING_FILE)

        # Trim spaces from the field_name column and extract column names
        mapping_df['field_name'] = mapping_df['field_name'].str.strip()
        column_names = mapping_df['field_name'].tolist()

        structure = list(zip(mapping_df['start_position'], mapping_df['end_position'], column_names))
        data = []

        with open(file_path, 'r') as file:
            for line in file:
                row = {}
                for start, end, column_name in structure:
                    # Adjust start position for 0-based indexing
                    row[column_name] = line[start - 1:end].strip()
                data.append(row)

        conn.register(table_name, pd.DataFrame(data, columns=column_names))

    elif extension == '.csv':
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}')")

    elif extension == '.xml':
        # Assuming XML files have a consistent structure and can be read directly into a DataFrame
        data = pd.read_xml(file_path)
        conn.register(table_name, data)

    elif extension == '.json':
        data = pd.read_json(file_path)
        conn.register(table_name, data)

    else:
        raise ValueError(f"Unsupported file format: {extension}")

    # Return the column names for the loaded table
    column_info = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [col[1] for col in column_info]


# Load data and get column names
columns_src_names = load_data_into_duckdb(SRC_PATH, 'table_src')
columns_trg_names = load_data_into_duckdb(TRG_PATH, 'table_trg')

# Define keys string for SQL queries
keys_str = ', '.join(PRIMARY_KEYS)

# Perform comparisons
# ... [rest of the comparison code]

# For source_key_duplicate
source_key_duplicate = conn.execute(f"""
    SELECT *
    FROM table_src
    WHERE ({keys_str}) IN (
        SELECT {keys_str}
        FROM table_src
        GROUP BY {keys_str}
        HAVING COUNT(*) > 1
    )
""").fetchall()
pd.DataFrame(source_key_duplicate, columns=columns_src_names).to_csv('source_key_duplicate.csv', index=False)

# For target_key_duplicate
target_key_duplicate = conn.execute(f"""
    SELECT *
    FROM table_trg
    WHERE ({keys_str}) IN (
        SELECT {keys_str}
        FROM table_trg
        GROUP BY {keys_str}
        HAVING COUNT(*) > 1
    )
""").fetchall()
pd.DataFrame(target_key_duplicate, columns=columns_trg_names).to_csv('target_key_duplicate.csv', index=False)

# ... [similarly for other CSV writes]
