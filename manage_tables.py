import os
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

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
		conn = psycopg2.connect(DATABASE_URL, sslmode="require")
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
	commands = ["""DROP TABLE IF EXISTS Places"""] + [
	"""
	insert into Places (title, description, image_link, sentby, position, approved) 
		values ('{}', 'Test point', '', 'admin', POINT({},{}), {});
	"""
	]*1000
	try:
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		for i, command in enumerate(commands):
			x = round(random.uniform(55.9596691, 56.0423812), 7)
			y = round(random.uniform(92.666692, 93.2466611), 7)
			cur.execute(command.format("Point #{}".format(i), x, y, "true"))
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


def testingSelection():
	commands = [
	"""
	SELECT
	  *
	FROM 
	  Places
	WHERE
	  position <@ circle '((56.0092305, 92.8393127), 300)' and approved;
	"""
	]
	try:
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		for command in commands:
			cur.execute(command)
			records = cur.fetchall()
			for i, row in enumerate(records):
				print(i, row)
		cur.close()
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


if __name__ == "__main__":
	dev = os.environ["envir"] == "dev"
	print("[1/3] Creating tables...")
	createTables()
	print("[2/3] Populatinf database...")
	if dev:
		populateTables()
	print("[3/3] Populatinf database...")
	testingSelection()
	print("Done")
	