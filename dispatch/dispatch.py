from dispatchController import createDeliveryForRequest, assignAuthFieldForUser
from eve import Eve
from eve.auth import BasicAuth
from eve_docs_test import eve_docs
from eve_sqlalchemy import SQL
from eve_sqlalchemy.decorators import registerSchema
from eve_sqlalchemy.validation import ValidatorSQL
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from tables import Users, Shifts, Requests, Deliveries, Base
import bcrypt
import datetime as dt
import json

class BCryptAuth(BasicAuth):
	def check_auth(self, username, password, allowed_roles, resource, method):
		if resource == 'users' and method in ['POST', 'GET']:
			print 'Checking sidkick auth'
			return username == 'sidekick' and password == 'halpme'
		else:
			print 'Checking user auth for', username
			user = app.data.driver.session.query(Users).filter(Users.email == username).first()
			self.set_request_auth_value(user._id)
			return user and bcrypt.hashpw(password, user.password) == user.password

app = Eve(validator=ValidatorSQL, data=SQL, auth=BCryptAuth)
Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base

def post_requests_post_callback(request, lookup):
	data = json.loads(lookup.data)
	if data['_status'] == 'OK':
		createDeliveryForRequest(db, data['_id'])

def after_inserting_user(items):
	try:
		userId = items[0]['_id']
		assignAuthFieldForUser(db, userId)
		print 'Successfully updated auth field (user_id) for new user', userId
	except:
		print 'Error in updating auth field for new user from insert', items


def after_updating_users(updates, original):
	try:
		if updates[u'online'] == True:
			print 'user', original[u'_id'], 'is online.'
	except:
		print 'User info updated, not going online', updates

# add custom route
@app.route("/x")
def hello():
    return "Hello World!"

# attach event hooks
app.on_post_POST_requests += post_requests_post_callback

# attach database event hooks
app.on_inserted_users += after_inserting_user
app.on_updated_users += after_updating_users

if __name__ == '__main__':
	
	# drop and create tables in the database
	db.drop_all()
	db.create_all()

	# Insert some example data in the db
	masterPassword = bcrypt.hashpw('password123', bcrypt.gensalt())
	test_data = [
	    (u'Austin', u'Wells', u'a@w.com', masterPassword, u'1231231234', u'sidekick', u'1'),
	    (u'Spencer', u'Kaiser', u's@k.com', masterPassword, u'1231231234', u'sidekick', u'2'),
	    (u'Carly', u'Kubacak', u'c@k.com', masterPassword, u'1231231234', u'user', u'3'),
	    (u'Irisa', u'Ona', u'i@o.com', masterPassword, u'1231231234', u'admin', u'4'),
	]

	test_data_shifts = [
		(u'1'),
		(u'2'),
		(u'3'),
	]

	test_data_requests = [
		(u'3', u'Fondren', u'Umbrella', u'Deliver it in person'),
		(u'3', u'CM', u'iPhone charger', u'Deliver it in person'),
		(u'3', u'DG Tent', u'Throw away camera', u'Deliver it in person'),
	]

	test_data_deliveries = [
		(u'1', u'1'),
		(u'2', u'2'),
		(u'3', u'1'),
	]

	if not db.session.query(Users).count():
	    for item in test_data:
	        db.session.add(Users.from_tuple(item))
	    db.session.commit()

	if not db.session.query(Shifts).count():
	    for item in test_data_shifts:
	        db.session.add(Shifts.from_tuple(item))
	    db.session.commit()

	if not db.session.query(Requests).count():
	    for item in test_data_requests:
	        db.session.add(Requests.from_tuple(item))
	    db.session.commit()

	if not db.session.query(Deliveries).count():
	    for item in test_data_deliveries:
	        db.session.add(Deliveries.from_tuple(item))
	    db.session.commit()
	# run the app
	app.run(debug=True)