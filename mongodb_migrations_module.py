from pymongo import MongoClient

import global_parameters as g


MongoClient(host=g.DB.localhost, port=g.DB.mongo_port).get_database(g.DB.db_name)
