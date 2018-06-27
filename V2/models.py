from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import uuid
import jwt
import os

from flask import current_app


class Base():
    """base Model """

    def __init__(self):
        self.db_name = current_app.config['DB_NAME']
        self.db_host = current_app.config['DB_HOST']
        self.db_username = current_app.config['DB_USERNAME']
        self.db_password = current_app.config['DB_PASSWORD']
        self.conn = psycopg2.connect(
            database=self.db_name,
            host=self.db_host,
            user=self.db_username,
            password=self.db_password)
        self.cur = self.conn.cursor()

    def create_table(self, schema):
        self.cur.execute(schema)
        self.save()

    def drop_table(self, name):
        self.cur.execute('DROP TABLE IF EXISTS ' + name)
        self.save()

    def save(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class User(Base):
    """ User Model """

    def __init__(self, email, username, password):
        # Class Constructor
        super().__init__()
        self.email = email
        self.username = username
        self.password = "" if not password else generate_password_hash(
            password)

    def create(self):
        self.create_table(
            """
            CREATE TABLE users(
                id serial PRIMARY KEY,
                email VARCHAR NOT NULL UNIQUE,
                username VARCHAR NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
            """
        )

    def drop(self):
        self.drop_table("users")

    def add(self):
        self.cur.execute(
            """
            INSERT INTO users (email, username, password)
            VALUES (%s , %s, %s)
            """,
            (self.email, self.username, self.password))

        self.save()

    def fetch_all(self):
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()

        if users:
            return [self.serializer(user) for user in users]
        return None

    def fetch_by_username(self, username):
        self.cur.execute(
            "SELECT * FROM users where username=%s", (username, ))

        user = self.cur.fetchone()

        if user:
            return self.serializer(user)
        return None

    def fetch_by_email(self, email):
        self.cur.execute(
            "SELECT * FROM users where email=%s", (email, ))

        user = self.cur.fetchone()

        if user:
            return self.serializer(user)
        return None

    def check_password_hash(self, username, password):
        user = self.fetch_by_username(username)
        return check_password_hash(user["password"], password)

    def serializer(self, user):
        return dict(
            id=user[0],
            email=user[1],
            username=user[2],
            password_hash=user[3]
        )


class Ride(Base):
    """ Request Model """

    def __init__(
            self, user_id, cateogory, pick_up,
            drop_off, id, date_time, price, requested=False):
        super().__init__()
        self.id = id
        self.user_id = user_id
        self.public_id = str(uuid.uuid4())
        self.cateogory = cateogory
        self.pick_up = pick_up
        self.drop_off = drop_off
        self.date_time = date_time,
        self.price = price,
        self.requested = requested

    def create(self):
        self.create_table(
            """
            CREATE TABLE rides(
                id serial PRIMARY KEY,
                user_id integer NOT NULL,
                public_id varchar NOT NULL UNIQUE,
                category varchar NOT NULL UNIQUE,
                pick_up varchar NOT NULL,
                drop_off varchar NOT NULL,
                date_time text NOT NULL,
                price text NOT NULL,
                requested BOOLEAN NOT NULL
            """
        )

    def drop(self):
        self.drop_table("rides")

    def add(self):
        self.cur.execute(
            """
            INSERT INTO rides(
                user_id, public_id, category, pick_up, drop_off, date_time, price, requested)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                self.user_id, self.public_id, self.category,
                self.pick_up, self.drop_off,
                self.date_time, self.price, self.requested
            ))
        self.save()

    def fetch_all(self):
        self.cur.execute("SELECT * FROM rides")
        rides_tuple = self.cur.fetchall()
        rides = [self.serializer(ride) for ride in rides_tuple]
        return rides

    def fetch_by_id(self, public_id):
        self.cur.execute(
            "SELECT * FROM rides WHERE public_id=%s", (public_id, ))
        rides_tuple = self.cur.fetchone()
        if rides_tuple:
            return self.serializer(rides_tuple)
        return None

    def fetch_by_user(self, user_id):
        self.cur.execute(
            "SELECT * FROM rides WHERE user_id=%s", (user_id, ))
        rides_tuple = self.cur.fetchall()
        if rides_tuple:
            return [self.serializer(ride) for ride in rides_tuple]
        return None

    def update(self, public_id):
        self.cur.execute(
            """
            UPDATE rides
            SET
            category = (%s),
            pick_up = (%s),
            drop_off = (%s),
            date_time = (%s),
            price = (%s)
            WHERE public_id = (%s)
             """,
            (self.category, self.pick_up, self.drop_off,
             self.date_time, self.price, public_id)
        )
        self.save()

    def delete(self, public_id):
        self.cur.execute(
            "DELETE FROM rides WHERE public_id=%s", (public_id, ))
        self.save()

    def serializer(self, ride):
        return dict(
            id=ride[0],
            user_id=ride[1],
            public_id=ride[2],
            pick_up=ride[3],
            drop_off=ride[4],
            date_time=ride[5],
            price=ride[6],
            requested=ride[7]
        )


####
class Request(Base):
    """ Request Model """

    def __init__(
            self, user_id, ride_id, public_id, passenger_name, accepted=False,
            rejected=False):
        super().__init__()
        self.id = id
        self.user_id = user_id,
        self.public_id = str(uuid.uuid4())
        self.passenger_name = passenger_name
        self.accepted = accepted
        self.rejected = rejected

    def create(self):
        self.create_table(
            """
            CREATE TABLE requests(
                id serial PRIMARY KEY,
                user_id integer NOT NULL,
                ride_id integer NOT NULL,
                public_id varchar NOT NULL UNIQUE,
                passenger_name text NOT NULL,
                acccepted BOOLEAN NOT NULL,
                rejected BOOLEAN NOT NULL
            """
        )

    def drop(self):
        self.drop_table("requests")

    def add(self):
        self.cur.execute(
            """
            INSERT INTO requets(
                user_id, ride_id, public_id, passenger_name, accepted, rejected)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                self.user_id, self.ride_id, self.public_id,
                self.passenger_name, self.accepted, self.rejected
            ))
        self.save()

    def fetch_all(self):
        self.cur.execute("SELECT * FROM requests")
        requests_tuple = self.cur.fetchall()
        requests = [self.serializer(request) for request in requests_tuple]
        return requests

    def fetch_by_id(self, public_id):
        self.cur.execute(
            "SELECT * FROM requests WHERE public_id=%s", (public_id, ))
        requests_tuple = self.cur.fetchone()
        if requests_tuple:
            return self.serializer(requests_tuple)
        return None

    def fetch_by_user(self, user_id):
        self.cur.execute(
            "SELECT * FROM requests WHERE user_id=%s", (user_id, ))
        requests_tuple = self.cur.fetchall()
        if requests_tuple:
            return [self.serializer(request) for request in requests_tuple]
        return None

    def update(self, public_id):
        self.cur.execute(
            """
            UPDATE requests
            SET
            accepted = (%s),
            rejected = (%s),
            WHERE public_id = (%s)
             """,
            (self.accepted, self.rejected)
        )
        self.save()

    def delete(self, public_id):
        self.cur.execute(
            "DELETE FROM requests WHERE public_id=%s", (public_id, ))
        self.save()

    def serializer(self, request):
        return dict(
            id=request[0],
            user_id=request[1],
            ride_id=request[2],
            public_id=request[3],
            passenger_name=request[4],
            accepted=request[5],
            rejected=request[6],
        )

