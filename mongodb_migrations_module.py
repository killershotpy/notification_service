from pymongo import MongoClient

import global_parameters as g


MongoClient(host=g.DB.localhost, port=g.DB.mongo_port).get_database(g.DB.db_name)

g.ConnectMongo.for_update.drop_collection(g.DB.logging_admins)
g.ConnectMongo.for_update.create_collection(g.DB.logging_admins)
g.ConnectMongo.for_update.get_collection(g.DB.logging_admins).create_index(g.KV.type_p, unique=False)
g.ConnectMongo.for_update.get_collection(g.DB.logging_admins).create_index(g.KV.action_admin, unique=False)
g.ConnectMongo.for_update.get_collection(g.DB.logging_admins).create_index(g.KV.language_p, unique=False)
