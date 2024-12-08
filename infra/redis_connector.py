import redis
import os

class RedisConnector:
    def __init__(self):
        self.conn = self.connect_redis()

    def connect_redis(self):
        """
        Connects to the Redis database using the environment variables.
        
        Returns:
            redis.StrictRedis: The connection object to the Redis database.
        """
        try:
            return redis.StrictRedis(
                host=os.getenv('REDIS_HOST'),
                port=os.getenv('REDIS_PORT'),
                db=os.getenv('REDIS_DB')
            )
        except redis.RedisError as e:
            print(f"Error connecting to Redis: {e}")
            raise

    def get_connection(self):
        """
        Returns the connection object to the Redis database.
        """
        return self.conn
    
    def set_key(self, key, value):
        """
        Sets the given key-value pair in the Redis database.
        """
        try:
            self.conn.set(key, value)
        except redis.RedisError as e:
            print(f"Error setting key in Redis: {e}")
            raise

    def get_key(self, key):
        """
        Gets the value of the given key from the Redis database.
        """
        try:
            return self.conn.get(key)
        except redis.RedisError as e:
            print(f"Error getting key from Redis: {e}")
            raise
    
    def exists_key(self, key):
        """
        Checks if the given key exists in the Redis database.
        """
        try:
            return self.conn.exists(key)
        except redis.RedisError as e:
            print(f"Error checking key existence in Redis: {e}")
            raise

    def delete_key(self, key):
        """
        Deletes the given key from the Redis database.
        """
        try:
            self.conn.delete(key)
        except redis.RedisError as e:
            print(f"Error deleting key from Redis: {e}")
            raise

    def close_connection(self):
        """
        Closes the connection to the Redis database.
        """
        try:
            self.conn.close()
        except redis.RedisError as e:
            print(f"Error closing Redis connection: {e}")
            raise