from pydantic import ValidationError
import datetime
from typing import Union, Any
from flask import Flask, jsonify, request, Response
from flask_restful import abort
from functools import wraps
import json
import hashlib
from template_app.model.db_utils import db
from template_app.model.schema import PyObjectId
from dotenv import load_dotenv
import jwt
import os
from bson import ObjectId
# loading .env
load_dotenv()

JWT_KEY = os.getenv('jwt_key')

def drop_none(args: dict) -> dict:
    valid = {}
    for key, val in args.items():
        if val is not None:
            valid[key] = val
    return valid

# Check for token
def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        auth = request.headers.get('authorization')
        if not auth:
            return Response(json.dumps({'message': 'no token'}), status = 400)
        
        token = auth.split(' ')[1]
        try:
            data = jwt.decode(token, b'SECRET_KEY', algorithms=[JWT_KEY])
            setattr(request, 'data', data)
        except:
            return Response(json.dumps({'message': 'Invalid token'}), status = 403)
        return func(*args, **kwargs)
    return wrapped
    
def create_token(id):
    token = jwt.encode({ 'id' : id, 'exp': datetime.datetime.now() + datetime.timedelta(seconds=60*60*24*30)}, b'SECRET_KEY', algorithm='HS256')
    return token

def harsh_password(text:str) -> str:
    return hashlib.pbkdf2_hmac('sha256', text.encode(), b'SECRET', 100000).hex()

def verify_password(text:str, hash:str) -> bool:
    actual:str = harsh_password(text)
    return actual == hash

class error_handlers:
    '''' Raises Exceptions '''

    def abort_wrong_email(text:str):
        if '@' not in text:
            return abort(403, message='Email format not vailid')


    def abort_wrong_login(email:str, password:str):
        user = db.user.find_one({'email': email})
        if not user or not verify_password(password, user['password']):
            return abort(403, message='Could not validate credentials')
    

    def abort_user_exist(text:str):
        text:str = text.strip()
        user = db.user.find_one({'email': text})
        if user:
            return abort(400, message='User already exist')
    

    def abort_template_doesnt_exist(temp_id:PyObjectId, user_id:str):
        template = db.templates.find_one({'_id': ObjectId(temp_id), 'id': user_id})
        if not template:
            return abort(400, message="Template doesn't exist")
