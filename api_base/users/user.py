import json
from flask import jsonify
from flask_restful import Resource, reqparse
import pymysql
import util
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from . import user_router_model
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta



def db_init():
    db = pymysql.connect(
        host="127.0.0.1", user="root", password="root", port=3306, db="api_learn"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

def get_access_token(user):
    token = create_access_token(
        identity={"user": user}, expires_delta=timedelta(days=1)
    )
    return token

# Swagger setting for auto bring token in API
security_params = [{"bearer": []}]

class Login(MethodResource):
    @doc(description="login API", tags=["Login"])
    @use_kwargs(user_router_model.LoginSchema, location="form")
    @marshal_with(user_router_model.LoginResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account = kwargs["account"]
        sql = f"SELECT * FROM api_learn.api_use WHERE name = '{account}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(account)
            return util.success({"token": token})

        return util.failure()

class Users(MethodResource):
    # Get all User
    @doc(description="Get Users info.", tags=["User"])
    @use_kwargs(user_router_model.UserGetSchema, location="query")
    @marshal_with(user_router_model.UserGetResponse, code=200)
    def get(self, **kwargs):
        db, cursor = db_init()

        name = kwargs.get("name")

        if name is not None:
            sql = f"SELECT * FROM api_learn.api_use WHERE name LIKE '%{name}%';"
        else:
            sql = "SELECT * FROM api_learn.api_use;"

        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return util.success(users)
    
    #create user
    @doc(description="Create User.", tags=["User"],security=security_params)
    @use_kwargs(user_router_model.UserPostSchema, location="form")
    @marshal_with(user_router_model.UserCommonResponse, code=200)
    @jwt_required()
    def post(self, **kwargs):
        db, cursor = db_init()

        # user = {
        #     "name": kwargs["name"],
        #     "gender": kwargs["gender"],
        #     "birth": kwargs.get("birth") or "1900-01-01",
        #     "note": kwargs.get("note"),
        # }
        sql = """

        INSERT INTO api_learn.api_use (`name`,`gender`,`birth`,`note`)
        VALUES ('{}','{}','{}','{}');

        """.format(
            kwargs["name"], kwargs["gender"], kwargs["birth"], kwargs["note"]
        )

        result = cursor.execute(sql)

        db.commit()
        db.close()

        if result == 0:
            return util.failure()

        return util.success()
    
    
class User(MethodResource):
    
    @doc(description="Get Single user info.", tags=["User"])
    @marshal_with(user_router_model.UserGetResponse, code=200)
    def get(self ,id):
        db, cursor = db_init()
        sql = f"SELECT * FROM api_learn.api_use WHERE id={id};"
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return util.success(users)
    
    
    
    
    @doc(description="Update User info.", tags=["User"],security=security_params)
    @use_kwargs(user_router_model.UserPatchSchema, location="form")
    @marshal_with(user_router_model.UserCommonResponse, code=201)
    @jwt_required()
    def patch(self, id,**kwargs):
        db, cursor = db_init()

        user = {
            "name": kwargs.get("name"),
            "gender": kwargs.get("gender"),
            "birth": kwargs.get("birth") or "1900-01-01",
            "note": kwargs.get("note"),
        }

        query = []
       
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        
        sql = """
            UPDATE api_learn.api_use
            SET {}
            WHERE id = {};
        """.format(
            query, id
        )

        result = cursor.execute(sql)
        db.commit()
        db.close()
        if result == 0:
            return util.failure()
        return util.success()
    
    @doc(description="Delete User info.", tags=["User"],security=security_params)
    @marshal_with(None, code=204)
    @jwt_required()
    def delete(self, id):
        db, cursor = db_init()
        sql = f"DELETE FROM `api_learn`.`api_use` WHERE id = {id};"
        
        cursor.execute(sql)
        db.commit()
        db.close()











# # # class Users(Resource):
# #     # Get all User
# #     def get(self):
# #         db, cursor = db_init()
# #         parser = reqparse.RequestParser()
# #         parser.add_argument("name", type=str, location="args")
# #         args = parser.parse_args()

# #         name = args.get("name")

# #         if name is not None:
# #             sql = f"SELECT * FROM api_learn.api_use WHERE name LIKE '%{name}%';"
# #         else:
# #             sql = "SELECT * FROM api_learn.api_use;"

# #         cursor.execute(sql)
# #         users = cursor.fetchall()
# #         db.close()
# #         return jsonify(users)
    
# #     def post(self):
# #         db, cursor = db_init()
        
# #         parser = reqparse.RequestParser()
# #         parser.add_argument("name", type=str, required=True, location="form")
# #         parser.add_argument("gender", type=str, required=True, location="form")
# #         parser.add_argument("birth", type=str, required=True, location="form")
# #         parser.add_argument("note", type=str, location="form")

# #         args = parser.parse_args()
# #         user = {
# #             "name": args["name"],
# #             "gender": args["gender"],
# #             "birth": args.get("birth") or "1900-01-01",
# #             "note": args.get("note"),
# #         }
# #         sql = """

# #         INSERT INTO `api_learn`.`api_use` (`name`,`gender`,`birth`,`note`)
# #         VALUES ('{}','{}','{}','{}');

# #         """.format(
# #             user["name"], user["gender"], user["birth"], user["note"]
# #         )
# #         result = cursor.execute(sql)
# #         message = "success" if result == 1 else "failure"
# #         db.commit()
# #         db.close()

# #         return jsonify({"message": message})

# # # class User(Resource):
#     def get(self ,id):
#         db, cursor = db_init()
#         sql = f"SELECT * FROM api_learn.api_use WHERE id={id};"
#         cursor.execute(sql)
#         users = cursor.fetchall()
#         db.close()
#         return jsonify(users)
    
#     def delete(self, id):
#         db, cursor = db_init()
#         sql = f"DELETE FROM `api_learn`.`api_use` WHERE id = {id};"
#         result = cursor.execute(sql)
#         message = "success" if result == 1 else "failure"
#         db.commit()
#         db.close()

#         return jsonify({"message": message})
    
#     def patch(self, id):
#         db, cursor = db_init()
#         parser = reqparse.RequestParser()
#         parser.add_argument("name", location="form")
#         parser.add_argument("gender", location="form")
#         parser.add_argument("birth", location="form")
#         parser.add_argument("note", location="form")
#         args = parser.parse_args()
#         user = {
#             "name": args.get("name"),
#             "gender": args.get("gender"),
#             "birth": args.get("birth"),
#             "note": args.get("note"),
#         }

#         query = []
#         """{'name': None, 'gender': 'Double', 'birth': None, 'note': None}"""
#         for key, value in user.items():
#             if value is not None:
#                 query.append(f"{key} = '{value}'")
#         query = ",".join(query)
#         """
#         UPDATE table_name
#         SET column1=value1, column2=value2, column3=value3···
#         WHERE some_column=some_value;

#         """
#         sql = """
#             UPDATE api_learn.api_use
#             SET {}
#             WHERE id = {};
#         """.format(
#             query, id
#         )

#         result = cursor.execute(sql)
#         message = "success" if result == 1 else "failure"
#         db.commit()
#         db.close()

#         return jsonify({"message": message})