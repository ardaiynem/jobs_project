import pymongo
import os
from pymongo.errors import PyMongoError

class MongoDBConnector:
    def __init__(self):
        self.client = self.connect_mongodb()
        self.db = self.client['jobs_db']
        self.collection = self.db['raw_collection']

    def connect_mongodb(self):
        """
        Connects to the MongoDB database.
        
        Returns:
            pymongo.MongoClient: The MongoDB client object.
        
        Raises:
            PyMongoError: An error occurred when connecting to the MongoDB database.
        """
        try:
            return pymongo.MongoClient(
                host=os.getenv('MONGO_HOST'),
                port=int(os.getenv('MONGO_PORT')),
                username=os.getenv('MONGO_INITDB_ROOT_USERNAME'),
                password=os.getenv('MONGO_INITDB_ROOT_PASSWORD')
            )
        except PyMongoError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def insert_data(self, data):
        """
        Inserts the given data into the MongoDB collection.
        
        Args:
            data (dict): The data to be inserted into the MongoDB collection.
        
        Raises:
            PyMongoError: An error occurred when inserting data into the MongoDB collection.
        """
        try:
            self.collection.insert_one(data)
        except PyMongoError as e:
            print(f"Error inserting data into MongoDB: {e}")
            raise

    def update_data(self, query, new_values):
        """
        Updates the data in the MongoDB collection that matches the given query.

        Args:
            query (dict): The query to match the data to be updated.
            new_values (dict): The new values to be updated in the data.

        Raises:
            PyMongoError: An error occurred when updating data in the MongoDB collection.
        """
        try:
            self.collection.update_one(query, {'$set': new_values})
        except PyMongoError as e:
            print(f"Error updating data in MongoDB: {e}")
            raise

    def delete_data(self, query):
        """
        Deletes the data in the MongoDB collection that matches the given query.
        
        Args:
            query (dict): The query to match the data to be deleted.
        
        Raises:
            PyMongoError: An error occurred when deleting data from the MongoDB collection.
        """
        try:
            self.collection.delete_one(query)
        except PyMongoError as e:
            print(f"Error deleting data from MongoDB: {e}")
            raise

    def get_all_data(self):
        """
        Retrieves all the data from the MongoDB collection.

        Returns:
            list: A list of all the data in the MongoDB collection.
        
        Raises:
            PyMongoError: An error occurred when retrieving data from the MongoDB collection.
        """
        try:
            return list(self.collection.find())
        except PyMongoError as e:
            print(f"Error retrieving data from MongoDB: {e}")
            raise

    def close_connection(self):
        """
        Closes the connection to the MongoDB database.

        Raises:
            PyMongoError: An error occurred when closing the MongoDB connection.
        """
        try:
            self.client.close()
        except PyMongoError as e:
            print(f"Error closing MongoDB connection: {e}")
            raise