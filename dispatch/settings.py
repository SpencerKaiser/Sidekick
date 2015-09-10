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

# Name of the field used to store the owner of each document
AUTH_FIELD = 'user_id'

# DB connection string in format dbusername:password@domain/databasename
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sidekick:halpme@localhost/sidekick_dev?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'
SQLALCHEMY_DATABASE_URI = 'postgresql://sidekick:halpme@localhost/sidekick_dev'

# Enable reads (GET) for resources/collections
RESOURCE_METHODS = ['GET', 'POST']

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
DOMAIN['shifts'].update({
	# 'url': 'users/<regex("[0-9]*"):user_id>/shifts',
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'item_methods': ['GET', 'PATCH', 'DELETE'],
	})
DOMAIN['deliveries'].update({
	'auth_field': 'sidekick_id',
	})


