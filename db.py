from V2.models import User, Ride, Request


def init():
    user = User('email', 'username', 'password')
    ride = Ride()
    request = Request()

    user.create()
    ride.create()
    request.create()


def drop():
    user = User()
    ride = Ride()
    request = Request()

    user.drop()
    ride.drop()
    request.drop()
