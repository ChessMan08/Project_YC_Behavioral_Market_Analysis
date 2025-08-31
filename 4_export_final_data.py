import duckdb

# Path to the database file (relative to where this script will be run from)
db_path = 'dbt_project.duckdb'

# Name of the final table we want to export
table_to_export = 'fct_market_intelligence'

# Name for our final output CSV file
output_csv_path = '../final_analytics_data.csv' # Go up one level to save the CSV

print(f"Attempting to connect to DuckDB database at: {db_path}")

try:
    con = duckdb.connect(database=db_path, read_only=True)
    print("Connection successful.")
    print(f"Exporting table '{table_to_export}' to '{output_csv_path}'...")

    sql_query = f"""
    COPY (SELECT * FROM {table_to_export}) 
    TO '{output_csv_path}' (HEADER, DELIMITER ',');
    """

    con.execute(sql_query)
    con.close()

    print(f"Successfully exported data.")

except Exception as e:
    print(f"An error occurred: {e}")