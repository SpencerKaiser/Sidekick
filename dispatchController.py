import json
import datetime as dt
from sqlalchemy import func
from tables import Deliveries, Shifts

def createDeliveryForRequest(db, id):
	print "Create delivery for request", id

	default_time = dt.datetime(2001, 1, 1)

	# get list of sidekicks that are currently online 
	online_sidekicks = db.session.query(Shifts.user_id).filter(Shifts.clock_in<func.now(), Shifts.clock_out==default_time).all()
	# convert db query tuple format-- [(1,), (2,)] into an array of sidekick ids (1, 2)
	online_sidekicks = zip(*online_sidekicks)[0]

	# for each online sidekick, get their uncompleted deliveries
	sidekick_deliveries_array = db.session.query(Deliveries, func.count(Deliveries._id)).filter(Deliveries.completed==default_time, Deliveries.sidekick_id.in_(online_sidekicks)).group_by(Deliveries.sidekick_id).all()


	print "Incomplete Deliveries:"
	for sk in sidekick_deliveries_array:
		print "Sidekick", sk[0].sidekick_id
		print "Num deliveries:", sk[1]
		print "_________________"

		# delivery_counts = zip(*sidekick_deliveries_array)[1]
		# sk_with_least_incomplete_deliveries = delivery_counts.index(min(deliveries_counts))

	# todo: a sk without any deliveries will not be considered in the above min computation
