from flask import Flask, request, jsonify
from ariadne import graphql_sync, make_executable_schema, QueryType, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
import os
from app.tools import color as c
import app.resolver as r
from app.database import init_db


type = load_schema_from_path('./app/schema.graphql')

q = QueryType()

q.set_field('hello', r.hello_resolver)

schema = make_executable_schema(type, q)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/attendance'

init_db()

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
