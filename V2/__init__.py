from flask import Flask, request, render_template

from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import (
    jwt_required, JWTManager, create_access_token, get_jwt_identity,
    jwt_refresh_token_required, create_refresh_token
)
from .models import User, Ride, Request as RequestModel

import os
import re

from config import app_config

app = Flask(__name__)

MODE = os.getenv('MODE') if os.getenv('MODE') else 'development' # set development as default
app.config.from_object(app_config[MODE])
jwt = JWTManager(app)
api = Api(app) # creating Api instance with Flask app


def validate_str_field(string, name):
    """ Validates string field input"""
    if len(string.strip()) == 0:

        return {"message": f"{name} can't have empty values"}, 400

    elif not re.match("^[ A-Za-z0-9_-]*$", string):

        return {"message": f"{name} invalid datas"}, 400
    return None


def validate_username(string, name):
    """ Validates username input"""
    if len(string.strip()) == 0:

        return {"message": f"{name} can't have empty values"}, 400

    elif not re.match("^[A-Za-z0-9_-]*$", string):

        return {"message": f"{name} should only contain letters, numbers, underscores and dashes"}, 400

    return None


@app.route('/')
def index():
    """ Renders information about API"""
    return render_template('index.html')


class UserRegistration(Resource):
    """ User Registration Resource """
    parser = reqparse.RequestParser()

    parser.add_argument('username', required=True, type=str,
                        help="Username is required and can only be a string")
    parser.add_argument('email', required=True, type=str,
                        help="Email is required")
    parser.add_argument('password', required=True,
                        help="Password is required")
    parser.add_argument('confirm_password', required=True,
                        help="Password confirmation is required")

    def post(self):
        """ Create a new User Account"""
        args = UserRegistration.parser.parse_args()
        username = args.get("username").lower()

        if validate_username(username, 'Username'):
            return validate_username(username, 'Username')
        if not re.match(r'(?=.*?[0-9])(?=.*?[A-Z])(?=.*?[a-z]).{6}', args['password']):
            return {"message": " Password rule: 1 digit, 1 caps, 1 number and minimum of 6 chars"}, 400
        if not re.match('[^@]+@[^@]+\.[^@]+', args['email']):
            return {"message": "Provide a valid email"}, 400

        user = User(username=username,
                    email=args.get("email"), password=args.get("password"))
        username_taken = user.fetch_by_username(username)
        email_taken = user.fetch_by_email(args["email"])

        if username_taken:
            return {"message": "username already taken"}, 400
        elif email_taken:
            return {"message": "email already taken"}, 400
        elif args["password"] != args["confirm_password"]:
            return {
                "message": "password and confirm_password fields do not match"
            }, 400

        user.add()
        return {"message": "Account created successfully"}, 201


class UserSignin(Resource):
    """ User Signin Resource. User signs in if has an account """

    parser = reqparse.RequestParser()

    parser.add_argument('username', required=True, help="Username is required")

    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        """ Signin an existing User """
        args = UserSignin.parser.parse_args()
        username = args["username"].lower()
        password = args["password"]

        if validate_str_field(args["username"], 'Username'):
            
            return validate_str_field(args["username"], 'Username')

        new_user = User()
        user = new_user.fetch_by_username(username)

        if not user:
            return {"message": f"{username} does not have an account."}, 404
        if not new_user.check_password_hash(username, password):

            return {"message": "username or password do not match."}, 403

        access_token = create_access_token(identity=user)

        return {"access_token": access_token}, 200

# Adding resources to endpoints to enable api calls
api.add_resource(UserRegistration, '/api/v2/auth/register')
api.add_resource(UserSignin, '/api/v2/users/auth/login/')
# api.add_resource(UserSignout, '/api/v2/users/auth/signout/')
