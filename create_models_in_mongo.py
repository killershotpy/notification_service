from pymongo import MongoClient

import global_parameters as g


MongoClient(host=g.DB.address_db, port=g.DB.port_db).get_database(g.DB.name_db)

g.ConnectMongo.for_update.drop_collection(g.DB.notifications)
g.ConnectMongo.for_update.create_collection(g.DB.notifications)
g.ConnectMongo.for_update.get_collection(g.DB.notifications).create_index(g.KV.uuid, unique=True)
g.ConnectMongo.for_update.get_collection(g.DB.notifications).create_index([(f'{g.KV.system_title}', 'text')])

g.ConnectMongo.for_update.drop_collection(g.DB.users)
g.ConnectMongo.for_update.create_collection(g.DB.users)
g.ConnectMongo.for_update.get_collection(g.DB.users).create_index(g.KV.uuid, unique=True)
g.ConnectMongo.for_update.get_collection(g.DB.users).create_index(f'{g.KV.notifications}.{g.KV.uuid}')
