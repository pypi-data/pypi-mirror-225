# import pymongo
import yaml
from pymongo import MongoClient

# # Connection parameters
# host = 'localhost'  # Replace with your MongoDB server's hostname or IP address
# port = 27017  # Replace with the MongoDB server's port number

# # Create a MongoClient object
# client = MongoClient(host, port)


class MongoDBHelper:
    def __init__(self, host, port, database):
        """
        Initializes a MongoDBHelper object.

        Args:
            host (str): The MongoDB server's hostname or IP address.
            port (int): The MongoDB server's port number.
            database (str): The name of the MongoDB database to connect to.
        """
        self.client = MongoClient(host, port)
        self.db = self.client[database]

    def __init__(self, uri, database):
        """
        Initializes a MongoDBHelper object.

        Args:
            uri (str): The MongoDB connection URI string.
            database (str): The name of the MongoDB database to connect to.
        """
        self.client = MongoClient(uri)
        self.db = self.client[database]

    def insert_document(self, collection, document):
        """
        Inserts a document into the specified collection.

        Args:
            collection (str): The name of the collection to insert the document into.
            document (dict): The document to be inserted.

        Returns:
            pymongo.results.InsertOneResult: The result of the insertion operation.
        """
        return self.db[collection].insert_one(document)

    def insert_yaml_file(self, collection, file_path):
        """
        Inserts a YAML file into the MongoDB collection.

        Args:
            collection (str): The name of the collection to insert the document into.
            file_path (str): The path to the YAML file.

        Returns:
            str: The inserted document ID.
        """
        with open(file_path, 'r') as file:
            # yaml_data = yaml.load(file, Loader=yaml.Loader)
            yaml_data = file.read()
            doc = {'yaml_data': yaml_data, 'file_name': file_path}

        return str(self.db[collection].insert_one(doc).inserted_id)
    
    def update_yaml_file(self, collection, file_id, updated_data):
        """
        Updates a YAML file in the MongoDB collection.

        Args:
            collection (str): The name of the collection to insert the document into.
            file_id (str): The ID of the document representing the YAML file.
            updated_data (dict): The updated YAML data.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        result = self.db[collection].update_one({"_id": file_id}, {"$set": updated_data})
        return result.modified_count > 0
    
    def get_yaml_file(self, collection, file_id):
        """
        Retrieves a YAML file from the MongoDB collection.

        Args:
            collection (str): The name of the collection to insert the document into.
            file_id (str): The ID of the document representing the YAML file.

        Returns:
            dict: The YAML data.
        """
        return self.db[collection].find_one({"_id": file_id})

    def find_documents(self, collection, query):
        """
        Finds documents in the specified collection that match the query.

        Args:
            collection (str): The name of the collection to search.
            query (dict): The query to filter the documents.

        Returns:
            pymongo.cursor.Cursor: The cursor object containing the matching documents.
        """
        return self.db[collection].find(query)

    def update_documents(self, collection, filter_query, update_query):
        """
        Updates multiple documents in the specified collection.

        Args:
            collection (str): The name of the collection to update.
            filter_query (dict): The filter query to select the documents to update.
            update_query (dict): The update query specifying the changes to apply.

        Returns:
            pymongo.results.UpdateResult: The result of the update operation.
        """
        return self.db[collection].update_many(filter_query, update_query)

    def delete_documents(self, collection, filter_query):
        """
        Deletes multiple documents from the specified collection.

        Args:
            collection (str): The name of the collection to delete documents from.
            filter_query (dict): The filter query to select the documents to delete.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        return self.db[collection].delete_many(filter_query)

    def close_connection(self):
        """
        Closes the connection to the MongoDB server.
        """
        self.client.close()



# Examples

# # Create an instance of MongoDBHelper
# mongo = MongoDBHelper('localhost', 27017, 'your_database_name')

# # Example usage of insert_document()
# document = {'name': 'John', 'age': 30}
# result = mongo.insert_document('your_collection_name', document)
# # Document inserted. result.inserted_id contains the ID of the inserted document.

# # Example usage of find_documents()
# query = {'name': 'John'}
# documents = mongo.find_documents('your_collection_name', query)
# # documents is a cursor object containing the documents that match the query.
# # Iterate over the cursor to access each document.

# # Example usage of update_documents()
# filter_query = {'name': 'John'}
# update_query = {'$set': {'age': 31}}
# result = mongo.update_documents('your_collection_name', filter_query, update_query)
# # Multiple documents updated. result.modified_count contains the number of modified documents.

# # Example usage of delete_documents()
# filter_query = {'name': 'John'}
# result = mongo.delete_documents('your_collection_name', filter_query)
# # Multiple documents deleted. result.deleted_count contains the number of deleted documents.

# # Close the connection to the MongoDB server
# mongo.close_connection()




