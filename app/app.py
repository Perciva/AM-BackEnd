from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from ariadne import graphql_sync, make_executable_schema, QueryType, load_schema_from_path, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from app.tools import color as c
import app.resolver as r
from app.database import init_db


type = load_schema_from_path('./app/schema.graphql')

q = QueryType()
user = ObjectType('User')
login = ObjectType('LoginData')
q.set_field('hello', r.hello_resolver)
q.set_field('GetUser', r.getUser)

schema = make_executable_schema(type, [q,user,login])

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/attendance'
# init_db()


@app.route('/')
def index():
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
    app.run(debug=true)
