from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from ariadne import graphql_sync, make_executable_schema, QueryType, load_schema_from_path, ObjectType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from app.tools import color as c
import app.resolver as r
from app.database import init_db


type = load_schema_from_path('./app/schema.graphql')

q = QueryType()
user = ObjectType('User')
login = ObjectType('LoginData')
period = ObjectType('Period')
leader = ObjectType('Leader')

q.set_field('hello', r.hello_resolver)
q.set_field('GetUser', r.getUser)

q.set_field('GetAllPeriods', r.getAllPeriods)
q.set_field('GetAllLeader', r.getAllLeader)
q.set_field('GetLeaderById', r.getLeaderByID)

m = MutationType()
m.set_field('InsertPeriod', r.InsertPeriod)
m.set_field('DeletePeriod',r.DeletePeriod)
m.set_field('UpdatePeriod', r.UpdatePeriod)

m.set_field('InsertLeader',r.InsertLeader)
m.set_field('DeleteLeader', r.DeleteLeader)
m.set_field('UpdateLeader', r.UpdateLeader)

schema = make_executable_schema(type, [q,m,user,login,period,leader])

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

from app.model import period
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
    app.run(debug=True)
