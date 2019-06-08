import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = None


def createTables():
	commands = [
	"""
	create table Places (
		id serial primary key,
		title text NOT NULL,
		description text NULL,
		image_link text NULL,
		sentby text,
		position point NOT NULL,
		approved bool
	);
	"""
	]
	try:
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		for command in commands:
			cur.execute(command)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


def populateTables():
	commands = [
	"""
	insert into Places (title, description, image_link, sentby, position, approved) 
		values 
			('Красная площадь', '', 'admin', POINT(56.0088264,92.8400713), false),
			('Красная площадь', '', 'admin', POINT(56.0088264,92.8400713), true),
			('Красная площадь', '', 'admin', POINT(56.0088264,92.8400713), true),
			('Красная площадь', '', 'admin', POINT(56.0088264,92.8400713), false);
	"""
	]
	try:
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		for command in commands:
			cur.execute(command)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


if __name__ == "__main__":
	print("[1/2] Creating tables...")
	createTables()
	connect()
	print("[2/2] Populatinf database...")
	populateTables()
	print("Done")
	