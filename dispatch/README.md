# Sidekick Dispatch Service

## Dependencies
* eve: ``pip install eve ``
* SQLAlchemy: `` pip install SQLAlchemy``


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