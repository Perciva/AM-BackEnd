from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 7200
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/testing'

from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from app.tools import color as c
import app.resolvers.resolver as r
from app.database import init_db, query, mutation

user = ObjectType('User')
login = ObjectType('LoginData')
period = ObjectType('Period')
leader = ObjectType('Leader')
assistant = ObjectType('Assistant')
special_shift = ObjectType('SpecialShift')
shift = ObjectType('Shift')

type = load_schema_from_path('./app/schema.graphql')


schema = make_executable_schema(type, [query, mutation, assistant, leader, login, user, period, shift, special_shift])

# app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

from app.model import period
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/attendance'


@app.route('/')
def index():
    init_db()
    return "hi RIG"

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True)
