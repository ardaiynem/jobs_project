import psycopg2
import os

class PostgreSQLConnector:
    def __init__(self):
        self.conn = self.connect_postgresql()
        self.cursor = self.conn.cursor()

    def connect_postgresql(self):
        """
        Connects to the PostgreSQL database using the environment variables.
        
        Returns:
            psycopg2.extensions.connection: The connection object to the PostgreSQL database.
        """
        return psycopg2.connect(
            dbname=os.getenv("SQL_NAME"),
            user=os.getenv("SQL_USER"),
            password=os.getenv("SQL_PASSWORD"),
            host=os.getenv("SQL_HOST"),
            port=os.getenv("SQL_PORT"),
        )

    def get_cursor(self):
        """
        Returns the cursor object for the PostgreSQL connection.
        
        Returns:
            psycopg2.extensions.cursor: The cursor object for the PostgreSQL connection.
        """
        return self.conn.cursor()

    def execute_query(self, query, params=None):
        """
        Executes the given query and returns the result.
        
        Args:
            query (str): The SQL query to be executed.
            params (tuple): The parameters to be passed to the query.
            
        Returns:
            list: The result of the query execution.

        Raises:
            psycopg2.Error: An error occurred while executing the query.
        """

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if query.strip().lower().startswith("select"):
                result = self.cursor.fetchall()
            else:
                self.conn.commit()
                result = None

            return result
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Database error: {e}")
            raise

    def close_connection(self):
        """
        Closes the connection to the PostgreSQL database.
        """

        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    def create_jobs_table(self):
        """
        Creates the jobs table in the PostgreSQL database.
        """

        create_table_query = """
        CREATE TABLE IF NOT EXISTS raw_table (
            id SERIAL PRIMARY KEY,
            slug TEXT,
            language TEXT,
            languages TEXT,
            req_id TEXT,
            title TEXT,
            description TEXT,
            street_address TEXT,
            city TEXT,
            state TEXT,
            country_code TEXT,
            postal_code TEXT,
            location_type TEXT,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            categories TEXT,
            tags TEXT,
            tags5 TEXT,
            tags6 TEXT,
            brand TEXT,
            promotion_value TEXT,
            salary_currency TEXT,
            salary_value NUMERIC,
            salary_min_value NUMERIC,
            salary_max_value NUMERIC,
            benefits TEXT,
            employment_type TEXT,
            hiring_organization TEXT,
            source TEXT,
            apply_url TEXT,
            internal BOOLEAN,
            searchable BOOLEAN,
            applyable BOOLEAN,
            li_easy_applyable BOOLEAN,
            ats_code TEXT,
            meta_data TEXT,
            update_date TIMESTAMPTZ,
            create_date TIMESTAMPTZ,
            category TEXT,
            full_location TEXT,
            short_location TEXT
        );
        """
        self.execute_query(create_table_query)
    
    def insert_jobs_data(self, field_names, field_values, values):
        """
        Inserts the job data into the PostgreSQL database.

        Args:
            field_names (str): The comma-separated field names.
            field_values (str): The comma-separated field values.
            values (list): The list of values to be inserted.
        """

        insert_query = f'INSERT INTO raw_table ({field_names}) VALUES ({field_values})'
        self.execute_query(insert_query, values)
