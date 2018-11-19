import pymongo

class Database(object):

    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize(db_name):
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client[db_name]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def find(collection, query, **options):
        if options['order_by'] == None and options['limit_number'] == 0:
            return Database.DATABASE[collection].find(query)
        elif options['order_by'] and options['limit_number'] == 0:
            return Database.DATABASE[collection].find(query).sort(options['order_by'], options['order_direction'])
        elif options['order_by'] == None and options['limit_number'] > 0:
            return Database.DATABASE[collection].find(query).skip(options['page']*options['limit_number']).limit(options['limit_number'])
        elif options['order_by'] and options['limit_number'] > 0:
            return Database.DATABASE[collection].find(query).sort(options['order_by'], options['order_direction']).skip(options['page']*options['limit_number']).limit(options['limit_number'])

    @staticmethod
    def count(collection, query):
        return Database.DATABASE[collection].find(query).count()

    @staticmethod
    def test(collection, search):
        return Database.DATABASE[collection].find_one(search)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)