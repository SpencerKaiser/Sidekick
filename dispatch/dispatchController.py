import json
import datetime as dt
from sqlalchemy import func, asc
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import nullsfirst
from tables import Deliveries, Shifts, Users

def assignAuthFieldForUser(db, userId):
	user = db.session.query(Users).filter(Users._id == userId).first()
	user.user_id = userId
	db.session.commit()

def createDeliveryForRequest(db, id):
	default_time = dt.datetime(2001, 1, 1)

	# get list of sidekicks that are currently online 
	# online_sidekicks = db.session.query(Shifts.user_id)\
	# 	.filter(Shifts.clock_in<func.now(), Shifts.clock_out==default_time)\
	# 	.all()
	# # convert db query tuple format-- [(1,), (2,)] into an array of sidekick ids (1, 2)
	# print online_sidekicks
	# online_sidekicks = zip(*online_sidekicks)[0]

	deliveries = db.session.query(Deliveries.sidekick_id, func.count('*')\
		.label('delivery_count'))\
		.filter(Deliveries.completed==default_time)\
		.group_by(Deliveries.sidekick_id).subquery()

	sidekick_deliveries_array = db.session.query(Users, deliveries.c.delivery_count)\
		.outerjoin(deliveries, Users._id==deliveries.c.sidekick_id)\
		.filter(Users.type=='sidekick')\
		.filter(Users.online==True)\
		.order_by(nullsfirst(asc(deliveries.c.delivery_count)))

	# if there is an online sidekick, assign delivery to new request
	if (sidekick_deliveries_array.count() > 0):
		[sk, count] = sidekick_deliveries_array[0]
		print "Assigning delivery for request", id, "to sidekick", sk._id
		delivery = Deliveries(id, sk._id)
		db.session.add(delivery)
		db.session.commit()
	else:
		print "No sidekicks currently online. No Delivery created for Request", id