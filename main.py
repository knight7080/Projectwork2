from TTS.base_tts import View
from TTS.retrieve_schema import SchemaRetrieve
from TTS.text_to_sql_gemini import GenerateQuery
from TTS.db_management import Database

def main():
    view = View()  # Initialize the view with the dark theme
    view.title("Text to SQL LLM")
    
    # Gather MySQL connection parameters from the user
    # mysql_host = view.text_area("MySQL Host", "localhost")
    # mysql_user = view.text_area("MySQL User", "root")
    # mysql_password = view.text_area("MySQL Password", "",)  # Consider using a password input widget if available.
    mysql_database = view.text_area("MySQL Database", "test_db")

    Home, QueryEditor = view.tabs(["Home", "Query Editor"])

    with Home:
        # For MySQL, we expect an SQL file containing the script to execute.
        db_file = view.file_uploader("Upload SQL file", type=["sql"])
        Tables, Schema = view.tabs(["Tables List", "Schema Diagram"])

        with Tables:
            if db_file:
                # Pass the MySQL connection parameters to schemaRetrieve.
                schema_retrieve = SchemaRetrieve(
                    db_file=db_file,
                    host="localhost",
                    user="root",
                    password="Sql@123",
                    database=mysql_database
                )
                schema = schema_retrieve.db_to_schema()
                if schema:
                    schema_context = schema_retrieve.transform_schema(schema=schema)
            else:
                view.subheader("Please upload the SQL file to view the tables.")

        with Schema:
            try:
                schema_retrieve.display_schema_diagram(schema_context)
            except Exception as e:
                view.subheader("Please upload the SQL file to view the schema diagram.")

    with QueryEditor:
        view.header("SQL Query Tester")
        nlp_input = view.text_area("Write your NLP Input here:", "")

        if view.button("SQL Query Tester"):
            if schema_context:
                # Generate SQL query using the provided NLP input and schema context.
                sql_query = GenerateQuery().generate_sql_query_with_gemini(nlp_input, schema_context)
                view.write(sql_query)
                
                # Clean the generated query.
                sql_query = view.extract_sql_query(sql_query)
                print("SQL QUERY", sql_query)

                # Execute the query using the Database instance from schema_retrieve.
                if schema_retrieve.extension == 'sql':
                    schema_retrieve.db.execute_sql_query(sql_query, schema_retrieve.conn)
                else:
                    schema_retrieve.db.execute_db_query(sql_query, schema_retrieve.conn)
            else:
                view.error("Please upload the SQL file to proceed.")

main()
