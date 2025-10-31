from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from ..extensions import db
from ..models.user import User, UserSchema
from ..utils.decorators import handle_api_errors
from ..utils.validators import validate_email, validate_password


user_schema = UserSchema()


class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json() or {}
            print(f"Received data: {data}")  # Debug log
            
            # Validation
            required_fields = ['fullName', 'email', 'password', 'role']
            for field in required_fields:
                if not data.get(field):
                    return {"message": f"{field} is required"}, 400

            if data['role'] not in ['artist', 'collector']:
                return {"message": "Role must be 'artist' or 'collector'"}, 400

            if not validate_email(data['email']):
                return {"message": "Invalid email format"}, 400

            if not validate_password(data['password']):
                return {"message": "Password must be at least 8 characters with uppercase, lowercase, and numbers"}, 400

            # Check for existing user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return {"message": "User with this email already exists"}, 409

            # Create user
            user = User(
                username=data['email'].split('@')[0],
                email=data['email'],
                full_name=data['fullName'],
                role=data['role']
            )
            user.set_password(data['password'])

            db.session.add(user)
            db.session.commit()
            print(f"User created: {user.id}")  # Debug log

            # Create access token
            access_token = create_access_token(identity=str(user.id))

            return {
                "user": user_schema.dump(user),
                "access_token": access_token,
                "message": "Account created successfully"
            }, 201
            
        except Exception as e:
            print(f"Registration error: {str(e)}")  # Debug log
            db.session.rollback()
            return {"message": f"Registration failed: {str(e)}"}, 500


class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json() or {}
            print(f"Login attempt: {data.get('email')}")  # Debug log
            
            if not data.get('email') or not data.get('password'):
                return {"message": "Email and password are required"}, 400

            user = User.query.filter_by(email=data['email'], is_active=True).first()
            
            if not user or not user.check_password(data['password']):
                return {"message": "Invalid email or password"}, 401

            access_token = create_access_token(identity=str(user.id))
            
            return {
                "user": user_schema.dump(user),
                "access_token": access_token,
                "message": "Login successful"
            }, 200
            
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug log
            return {"message": f"Login failed: {str(e)}"}, 500