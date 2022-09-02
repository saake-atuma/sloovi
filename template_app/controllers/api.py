import json
from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from functools import wraps
from bson import ObjectId
from template_app.model.db_utils import db
from template_app.middleware.middlewares import error_handlers as e
from template_app.middleware.middlewares import (
    drop_none,
    check_for_token,
    create_token,
    harsh_password
)
from template_app.model.schema import (
    resource_fields,
    login_fields,
    user_details,
    login_details,
    template_details,
    template_put_details,
    register_fields 
    
)

class register(Resource):
    @marshal_with(register_fields)
    def post(self):
        args = user_details.parse_args()
        e.abort_wrong_email(args.email)
        e.abort_user_exist(args.email)
        args.password = harsh_password(args.password)
        created_user = db.user.insert_one(args)
        retrive_user = db.user.find_one({"_id": ObjectId(created_user.inserted_id)}, {'password':0})

        return retrive_user
        
class login(Resource):
    @marshal_with(login_fields)
    def post(self):
        args = login_details.parse_args()
        e.abort_wrong_email(args.email)
        e.abort_wrong_login(args.email, args.password)
        current_user = db.user.find_one({'email':args.email}, {'password':0})
        token= create_token(f'{current_user["_id"]}')
        current_user['token'] = token
        return current_user


class template(Resource):
    
    @check_for_token
    @marshal_with(resource_fields)
    def get(self):
        id = request.data['id']
        return [doc for doc in db.templates.find({'id':id, 'unusable':{'$ne': True}})]

    @check_for_token
    def post(self):
        args = template_details.parse_args()
        args['id'] = request.data['id']
        db.templates.insert_one(args)
        return Response(json.dumps("Successful"), status=201)

class template_1(Resource):
    @check_for_token
    @marshal_with(resource_fields)
    def get(self, temp_id):
        e.abort_template_doesnt_exist(temp_id, request.data['id'])
        result = db.templates.find_one({'_id': ObjectId(temp_id)})
        return result
    
    @check_for_token
    def put(self, temp_id):
        args = template_put_details.parse_args()
        e.abort_template_doesnt_exist(temp_id, request.data['id'])
        args = drop_none(args)
        db.templates.update_one({'_id':ObjectId(temp_id)}, {'$set': args})
        return Response(json.dumps("Successful"), status=204)
    

    @check_for_token
    def delete(self, temp_id):
        e.abort_template_doesnt_exist(temp_id, request.data['id'])
        db.templates.delete_one({'_id':ObjectId(temp_id)})
        return Response(json.dumps("Deleted"), status=204)

