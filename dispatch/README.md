# Sidekick Dispatch Service

## Dependencies
* eve: ``pip install eve ``
* SQLAlchemy: `` pip install SQLAlchemy``
* bcrpyt ``pip install py-bcrypt``
* flask bootstrap ``pip install flask-bootstrap``


## Database Stuff
To install postgres, follow the instructions [here](https://www.codefellows.org/blog/three-battle-tested-ways-to-install-postgresql#macosx)

After that, install a database adapter for postgres

	pip install psycopg2

And create a database and new user for that db
	
	createdb sidekick
	createuser -P sidekick
	GRANT ALL PRIVILEGES ON sidekick_dev TO sidekick;

To run

	python dispatch.py

To view documentation for all endpoints, hit the url serverRoot/docs!