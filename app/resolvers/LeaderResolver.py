from app.model import leader
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


# @jwt_required
def InsertLeader(_,info,period_id, initial, name):
    return leader.insert(period_id, initial, name)

# @jwt_required
def DeleteLeader(_,info,id):
    return leader.delete(id)

# @jwt_required
def UpdateLeader(_,info,id, initial, name):
    return leader.update(id, initial, name)

# @jwt_required
def getAllLeader(_,info):
    res = leader.getAllLeader()
    return res

# @jwt_required
def getLeaderByID(_,info,id):
    return leader.getLeaderByID(id)