from pymongo import MongoClient

CON_STR = "mongodb+srv://19294349:zJ89G0MBMxhdR1nf@base.vrtfupp.mongodb.net/?retryWrites=true&w=majority&appName=base"


def get_database(dbname):
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CON_STR)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client[dbname]
  
