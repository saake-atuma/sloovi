from flask import Flask
from flask_restful import Api


from template_app.controllers.api import (
    register,
    login,
    template,
    template_1
)

app = Flask(__name__)
api = Api(app)

api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(template,'/template')
api.add_resource(template_1,'/template/<string:temp_id>')

# if __name__ == '__main__':
#     app.run(debug = True)