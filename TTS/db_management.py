import mysql.connector
import pandas as pd
from .base_tts import View

class Database(View):

    def __init__(self, host, user, password, database):
        # Store MySQL connection parameters
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def sql_handling(self, file_path):
        """
        Execute an SQL script from a file against a MySQL database.
        """
        print("Error")
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(conn.is_connected())
        except mysql.connector.Error as err:
            self.error(f"Error connecting to MySQL: {err}")
            return None

        sql_script = file_path.read().decode("utf-8")

        if sql_script.strip():
            print('SQL SCRIPT')
            try:
                cursor = conn.cursor()
                # Execute the SQL script; multi=True allows executing multiple statements
                print(sql_script)
                resultset = cursor.execute(sql_script)
                print(str(len(resultset))+" this is the lengtht ")
                for result in resultset:
                    # Optionally process each result here
                    pass
                conn.commit()
                self.success("SQL script executed successfully.")
            except mysql.connector.Error as err:
                print(f"Error executing SQL script: {err}")
        else:
            self.warning("The SQL file is empty. Please provide valid SQL statements.")

        return conn

    def db_handling(self, file_path):
        """
        For MySQL, we generally connect using parameters, not a file path.
        This method simply creates a new connection.
        """
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            return None
        return conn

    def fetch_table_details(self, conn):
        """
        Retrieve table names from the connected MySQL database.
        """
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return tables

    def return_first_5_row(self, table_name, conn):
        """
        Display the first 5 rows of the specified table.
        """
        # Using pandas read_sql_query for convenience.
        data = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
        View().write(data)

    def execute_db_query(self, query, conn):
        """
        Execute a database query and display results using pandas.
        """
        try:
            data = pd.read_sql(query, conn)
            self.write(data)
        except Exception as e:
            self.error(f"Error executing query: {e}")

    def execute_sql_query(self, query, conn):
        """
        Execute a SQL query using a cursor, fetch all data, and display it.
        """
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # Retrieve column names from the cursor description.
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=column_names)
        View().table(df)

    def define_schema(self, tables, conn):
        """
        Define the schema for each table by retrieving column names and types.
        """
        schema = {}
        cursor = conn.cursor()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DESCRIBE {table_name};")
            columns = cursor.fetchall()
            # Each column tuple typically looks like:
            # (Field, Type, Null, Key, Default, Extra)
            schema[table_name] = [{"name": col[0], "type": col[1]} for col in columns]
        return schema

    def display_table_data(self, tables, conn):
        """
        Display available tables and optionally their first 5 rows.
        """
        View().header("Available Tables")
        if tables:
            View().write("Tables in the uploaded SQL file:")
            for table in tables:
                View().write(f"- {table[0]}")
                # Display first 5 rows from each table
                self.return_first_5_row(table[0], conn)
        else:
            View().warning("No tables found in the SQL script.")

