import tempfile
from .base_tts import View
from .db_management import Database

class SchemaRetrieve(View):

    def __init__(self, db_file, host, user, password, database):
        self.db_file = db_file
        self.conn = None
        self.extension = ""
        # Create a Database instance with MySQL connection parameters
        self.db = Database(host, user, password, database)

    def db_to_schema(self):
        if self.db_file is not None:
            # Save file temporarily and retrieve file path
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(self.db_file.getvalue())
                file_path = temp_file.name

            try:
                if self.db_file.name.endswith('.sql'):
                    self.extension = "sql"
                    # Execute the SQL script using MySQL
                    self.conn = self.db.sql_handling(self.db_file)
                    print("ERROR OCCURED HERE BELOW")
                else:
                    self.extension = "db"
                    # For MySQL, we generally use connection parameters so this branch
                    # simply creates a connection using those parameters.
                    self.conn = self.db.db_handling(file_path)

                # Fetch tables from the database
             
                tables = self.db.fetch_table_details(self.conn)
  
                schema = self.db.define_schema(tables, self.conn)
          

                # Display table names and optionally first 5 rows of each table
                View().header("Available Tables")
                preprocessed_tables = View().process_text(tables)
                for table in preprocessed_tables:
                    with View().expander(table):
                        self.db.return_first_5_row(table, self.conn)

                return schema

            except Exception as e:
                print("HELLo")
                View().error(f"An error occurred: {e} {e.__cause__}")
                return ""

    def transform_schema(self, schema):
        transformed_schema = {}
        for table, columns in schema.items():
            transformed_schema[table] = {
                column["name"]: column["type"] for column in columns
            }
        return transformed_schema

    def display_schema_diagram(self, schema):
        # Define the number of columns to display the schema side by side.
        cols = View().columns(3)  # Adjust the number of columns as needed.

        # For each column, display the table schema.
        col_index = 0
        for table_name, columns in schema.items():
            with cols[col_index]:
                View().subheader(f"Table: {table_name}")
                for column_name, column_type in columns.items():
                    View().write(f"{column_name}: {column_type}")

            # Move to the next column after each table.
            col_index += 1
            if col_index >= len(cols):
                col_index = 0  # Reset to the first column if there are more tables than columns.
