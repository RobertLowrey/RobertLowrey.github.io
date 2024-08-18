# This file handles the connection between the application and the MongoDB Compass NoSQL database.

from pymongo import MongoClient  # Importing MongoClient from the Pymongo library.

mongoConnection = 'mongodb://localhost:27017/'  # Connecting to a local database using the default port.
databaseName = 'TravelDestinationDatabase'  # Connecting to the TravelDestinationDatabase database.
collection = 'userInfo'  # Collection within the database is called userInfo.


# Defining a function called get_database.
def get_travel_destination_database():
    client = MongoClient(mongoConnection)  # Establishing a connection to the MongoDB server.
    db = client[databaseName]  # Accessing the database called TravelDestinationDatabase.
    return db  # Returning the database values.


# Defining a function called get_collection.
def get_collection():
    db = get_travel_destination_database()  # Calling get_database method.
    return db[collection]  # Returning the collection named users of the MongoDB database.
