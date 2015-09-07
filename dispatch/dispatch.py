import json
import datetime as dt
from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from tables import Users, Shifts, Requests, Deliveries, Base
from dispatchController import createDeliveryForRequest

app = Eve(validator=ValidatorSQL, data=SQL)

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base

def post_requests_post_callback(request, lookup):
	data = json.loads(lookup.data)
	if data['_status'] == 'OK':
		print "Assign request", data['_id'], "to a sidekick"
		createDeliveryForRequest(db, data['_id'])

# add custom route
@app.route("/x")
def hello():
    return "Hello World!"

# attach event hooks
app.on_post_POST_requests += post_requests_post_callback

if __name__ == '__main__':
	
	# drop and create tables in the database
	db.drop_all()
	db.create_all()

	# Insert some example data in the db
	test_data = [
	    (u'George', u'Washington', u'gwash@money.com', u'1231231234', u'user'),
	    (u'John', u'Adams', u'jadams@money.com', u'1231231234', u'sidekick'),
	    (u'Thomas', u'Jefferson', u'tjefferson@money.com', u'1231231234', u'admin'),
	]

	test_data_shifts = [
		(u'1'),
		(u'2')
	]

	test_data_requests = [
		(u'3', u'Fondren', u'Umbrella', u'Deliver it in person'),
		(u'3', u'CM', u'iPhone charger', u'Deliver it in person'),
		(u'3', u'DG Tent', u'Throw away camera', u'Deliver it in person'),
	]

	test_data_deliveries = [
		(u'1', u'1'),
		(u'2', u'2'),
		(u'3', u'1')
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