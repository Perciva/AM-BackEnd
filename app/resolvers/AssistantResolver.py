from app.model import assistant
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

@jwt_required
def InsertAssistant(_,info,period_id,leader_id, initial, name):
    return assistant.insert(period_id, leader_id, initial, name)

@jwt_required
def DeleteAssistant(_,info,id):
    return assistant.delete(id)

@jwt_required
def UpdateAssistant(_,info,id, period_id,leader_id, initial, name):
    return assistant.update(id, period_id, leader_id, initial, name)

@jwt_required
def getAllAssistant(_,info):
    res = assistant.getAllAssistant()
    return res

@jwt_required
def getAssistantByID(_,info,id):
    return assistant.getAssistantByID(id)