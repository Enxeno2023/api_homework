from marshmallow import Schema, fields


# Schema

class LoginSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)

class UserGetSchema(Schema):
    name = fields.Str(example="string")
    
class UserPostSchema(Schema):
    name = fields.Str(doc="name", example="string", required=True)
    gender = fields.Str(doc="gender", example="string", required=True)
    birth = fields.Str(doc="birth", example="string", required=True)
    note = fields.Str(doc="note", example="string", required=True)
    
class UserPatchSchema(Schema):
    name = fields.Str(doc="name", example="string")
    gender = fields.Str(doc="gender", example="string")
    birth = fields.Str(doc="birth", example="string")
    note = fields.Str(doc="note", example="string")
    
# Response
class UserGetResponse(Schema):
    message = fields.Str(example="success")
    datetime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())
    
class UserCommonResponse(Schema):
    message = fields.Str(example="success")

class LoginResponse(Schema):
    message = fields.Str(example="success")
    datetime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.Dict()
