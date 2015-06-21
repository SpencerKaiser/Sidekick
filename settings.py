from eve_sqlalchemy.decorators import registerSchema
from tables import Users, Requests, Deliveries, Shifts

registerSchema('users')(Users)
registerSchema('requests')(Requests)
registerSchema('deliveries')(Deliveries)
registerSchema('shifts')(Shifts)

DEBUG = True

# Exclude links to parent and sibling pages in server responses
HATEOAS = False

# Disable etag attribute 
IF_MATCH=False

# DB connection string in format dbusername:password@domain/databasename
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sidekick:halpme@localhost/testDB?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'

# Enable reads (GET) for resources/collections
RESOURCE_METHODS = ['GET']

# Enable reads (GET) and edits (PATCH) of individual items.
ITEM_METHODS = ['GET', 'PATCH']

# Register schemas defined in tables.py
DOMAIN = {
    'users': Users._eve_schema['users'],
    'requests': Requests._eve_schema['requests'],
    'deliveries': Deliveries._eve_schema['deliveries'],
    'shifts': Shifts._eve_schema['shifts']
    }

# Customize methods allowed for each resource
DOMAIN['users'].update({
	'resource_methods': ['GET', 'POST']
	})
DOMAIN['shifts'].update({
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'item_methods': ['GET', 'PATCH', 'DELETE']
	})

