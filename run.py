from V2 import app
from db import init, drop
from V2.models import User


@app.cli.command()
def init_db():
    """ Creates tables """
    init()


@app.cli.command()
def drop_db():
    """ Drops tables """
    drop()


