# services/users/manage.py
import os
import unittest
from flask.cli import FlaskGroup
import coverage
from V2 import app
from V2.models import User


cli = FlaskGroup(app)


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def init_db():
    """ Creates tables """
    user = User(email="danielmutuba@gmail.com", username="daniel", password="baraka")
    #ride = Ride()
    #request = Request()

    user.create()
    #ride.create()
    #request.create()


@cli.command()
def drop_db():
    """ Drops tables """
    user = User(email="danielmutuba@gmail.com", username="daniel", password="baraka")
    #ride = Ride()
    #request = Request()

    user.drop()
    #ride.drop()
    #request.drop()


if __name__ == '__main__':
    cli()
