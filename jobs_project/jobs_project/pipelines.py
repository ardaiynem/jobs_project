import sys
import os

# Add the project root directory to the Python path (Since I can not define __init__ file in the infra directory)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from infra.postgresql_connector import PostgreSQLConnector
from infra.redis_connector import RedisConnector
from infra.mongodb_connector import MongoDBConnector
import redis
from itemadapter import ItemAdapter
from datetime import datetime
from scrapy.exceptions import DropItem
import json
from .items import JobsProjectItem

class JobsProjectPipeline:
    def open_spider(self, spider):
        """
        Initializes the PostgreSQL, Redis, and MongoDB connectors.
        
        Args:
            spider (scrapy.Spider): The spider object.
        """
        # Initialize the PostgreSQL, Redis, and MongoDB connectors
        self.pg_conn = PostgreSQLConnector()
        self.rd_conn = RedisConnector()
        self.mongo_conn = MongoDBConnector()
        
        # Create the jobs table in the PostgreSQL database (if it does not exist))
        self.pg_conn.create_jobs_table()

    def close_spider(self, spider):
        """
        Closes the PostgreSQL, Redis, and MongoDB connections.

        Args:
            spider (scrapy.Spider): The spider object.
        """

        self.pg_conn.close_connection()
        self.rd_conn.close_connection()
        self.mongo_conn.close_connection()

    def check_field_existence(self, adapter, item, field_names):
        """
        Checks if the required fields are present in the item.
        """
        for field_name in field_names:
            if not adapter.get(field_name):
                raise DropItem("Missing title in %s" % item)
            
    def str_to_type(self, adapter, field_name, field_type):
        """
        Converts the field value to the specified type from str.
        """
        if adapter.get(field_name) and isinstance(adapter[field_name], str):
            adapter[field_name] = field_type(adapter[field_name])

    # Function to parse and convert the timestamp
    def convert_to_postgres_format(date_str):
        # Parse the input date string
        parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        # Return the string representation in ISO 8601 (PostgreSQL compatible)
        return parsed_date.isoformat()

    def process_item(self, item, spider):
        """
        Processes the job item extracted by the spider.

        Args:
            item (dict): The job item extracted by the spider.
            spider (scrapy.Spider): The spider object.
        
        Returns:
            JobsProjectItem: The processed job item.
        """
        adapter = ItemAdapter(item)

        # Check if the required fields are present in the item
        self.check_field_existence(adapter, item, ['title', 'req_id'])

        # Check if the job (req_id) already exists in the Redis database for duplicate detection
        item_key = f"job:{adapter['req_id']}"
        if self.rd_conn.exists_key(item_key):
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.rd_conn.set_key(item_key, 1)

        # Convert the timestamp to the PostgreSQL compatible format
        if adapter.get('created_at'):
            adapter['created_at'] = self.convert_to_postgres_format(adapter['created_at'])

        if adapter.get('updated_at'):
            adapter['updated_at'] = self.convert_to_postgres_format(adapter['updated_at'])

        # Convert the field values to the specified types
        self.str_to_type(adapter, 'latitude', float)
        self.str_to_type(adapter, 'longitude', float)
        self.str_to_type(adapter, 'salary_value', float)
        self.str_to_type(adapter, 'salary_min_value', float)
        self.str_to_type(adapter, 'salary_max_value', float)

        # Convert the list and dictionary fields to JSON strings
        for field in adapter.keys():
            if isinstance(adapter[field], (dict, list)):
                adapter[field] = json.dumps(adapter[field])

        # Insert the job data into the PostgreSQL
        field_names = ', '.join(adapter.keys())
        field_values = ', '.join(['%s'] * len(adapter.keys()))
        values = [adapter.get(key) for key in adapter.keys()]
        try:
            # Data processing and insertion
            self.pg_conn.insert_jobs_data(field_names, field_values, values)
        except Exception as e:
            print(f"Error processing item: {e}")
            raise DropItem(f"Failed to process item: {item}")

        # Insert the job data into the MongoDB
        try:
            self.mongo_conn.insert_data(adapter.asdict())
        except Exception as e:
            print(f"Error processing item: {e}")
            raise DropItem(f"Failed to process item: {item}")
        
        return item