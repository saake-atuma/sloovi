from pydantic import BaseModel, Field
from flask_restful import fields, reqparse
from bson import ObjectId
from typing import Union, Optional
from uuid import UUID
# from midwares import db



class PyObjectId(ObjectId):
    ''' Object to handle mongodb objectID'''
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


resource_fields = {
    '_id':fields.String,
    'template_name': fields.String,
    'subject': fields.String,
    'body': fields.String

}

login_fields = {
    '_id':fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'token': fields.String

}

register_fields = {
    '_id':fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
}

user_details = reqparse.RequestParser()
user_details.add_argument("first_name", type=str, help="Input first name of user", required=True)
user_details.add_argument("last_name", type=str, help="Input last name of user", required=True)
user_details.add_argument("email", type=str, help="Input user email", required=True)
user_details.add_argument("password", type=str, help="Input user password", required=True)

login_details = reqparse.RequestParser()
login_details.add_argument("email", type=str, help="Input user email", required=True)
login_details.add_argument("password", type=str, help="Input user password", required=True)

template_details = reqparse.RequestParser()
template_details.add_argument("template_name", type=str, help="Input template name", required=True)
template_details.add_argument("subject", type=str, help="Input template subject", required=True)
template_details.add_argument("body", type=str, help="Input template body", required=True)

template_put_details = reqparse.RequestParser()
template_put_details.add_argument("template_name", type=str, help="Input template name")
template_put_details.add_argument("subject", type=str, help="Input template subject")
template_put_details.add_argument("body", type=str, help="Input template body")



