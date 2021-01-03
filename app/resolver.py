import requests
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask import jsonify
from app.model import period, leader

@jwt_required
def hello_resolver(_,info):
    print(info)
    return "Hello There!!!"

def getUser(_,info,username, password):
    URL = "https://laboratory.binus.ac.id/lapi/api/Account/LogOnQualification"

    access_token = create_access_token(identity=username)

    d ={
        "username" : username,
        "password" : password
    }

    x = requests.post(URL,data = d)
    if(x.text == 'null'):
        return 'null'
    else :
        resp = {
            "UserData": x.json(),
            "Token" :  access_token
        }
        return resp

@jwt_required
def getAllPeriods(_,info):
    res = period.getAllPeriod()
    return res

@jwt_required 
def InsertPeriod(_,info,description,start,end):
    period.insert(description, start, end)
    return True

@jwt_required
def UpdatePeriod(_,info, id, description, start, end):
    return period.update(id, description, start, end)

@jwt_required
def DeletePeriod(_,info,id):
    period.delete(id)
    return True

@jwt_required
def InsertLeader(_,info,period_id, initial, name):
    return leader.insert(period_id, initial, name)

@jwt_required
def DeleteLeader(_,info,id):
    return leader.delete(id)

@jwt_required
def UpdateLeader(_,info,id, period_id, initial, name):
    return leader.update(id, period_id, initial, name)

@jwt_required
def getAllLeader(_,info):
    res = leader.getAllLeader()
    return res

@jwt_required
def getLeaderByID(_,info,id):
    return leader.getLeaderByID(id)
   






