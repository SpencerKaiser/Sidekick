from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from tables import Users, Shifts, Base

app = Eve(validator=ValidatorSQL, data=SQL)

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base

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

	if not db.session.query(Users).count():
	    for item in test_data:
	        db.session.add(Users.from_tuple(item))
	    db.session.commit()

	if not db.session.query(Shifts).count():
	    for item in test_data_shifts:
	        db.session.add(Shifts.from_tuple(item))
	    db.session.commit()

	# run the app
	app.run(debug=True)