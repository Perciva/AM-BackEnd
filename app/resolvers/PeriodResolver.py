from app.model import period
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


# @jwt_required
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