from flask import Flask
from flask_restful import Api
from users.user import Users,User, Login
#----------------------------------------------------------
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
#------------------------------------------------------------
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JWT_SECRET_KEY"] = "abcd1234"  # JWT token setting
#------------------------------------------------------------------------------------
app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Awesome Project",
            version="v1",
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0.0",
            # Swagger setting to set authorization
            securityDefinitions={
                "bearer": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                }
            },
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",  # URI to access API Doc JSON
        "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",  # URI to access UI of API Doc
    }
)
docs = FlaskApiSpec(app)
#--------------------------------------------------------------------------------------


api = Api(app)


api.add_resource(Users, "/users")
#--------------------------------
docs.register(Users)
#---------------------------------
api.add_resource(User, "/users/<int:id>")
docs.register(User)
#----------------------------------------
api.add_resource(Login, "/login")
docs.register(Login)

if __name__ == "__main__":
     # Remembet to initial JWTManger before running app
    jwt = JWTManager().init_app(app)
    app.run(host="127.0.0.1", port=10009, debug=True)