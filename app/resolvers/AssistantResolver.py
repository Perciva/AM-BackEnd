from flask_jwt_extended import jwt_required

from app.model import assistant
from app.database import query, mutation


@mutation.field("InsertAssistant")
@jwt_required
def InsertAssistant(_, info, period_id, leader_id, initial, name):
    return assistant.insert(period_id, leader_id, initial, name)


@mutation.field("DeleteAssistant")
@jwt_required
def DeleteAssistant(_, info, id):
    return assistant.delete(id)


@mutation.field("UpdateAssistant")
@jwt_required
def UpdateAssistant(_, info, id, period_id, leader_id, initial, name):
    return assistant.update(id, period_id, leader_id, initial, name)

@mutation.field("InsertAssistantByLeaderInitial")
@jwt_required
def InsertAssistantByLeaderInitial(_,info, period_id, leader_initial, initial, name):
    return assistant.insertByLeaderInitial(period_id, leader_initial, initial, name)


@query.field("GetAllAssistant")
@jwt_required
def getAllAssistant(_, info):
    res = assistant.getAllAssistant()
    return res


@query.field("GetAssistantById")
@jwt_required
def getAssistantByID(_, info, id):
    return assistant.getAssistantByID(id)

@query.field("GetAssistantByLeaderId")
@jwt_required
def getAssistantByLeaderId(_, info, leader_id, period_id):
    return assistant.getAssistantByLeaderId(leader_id, period_id)

@query.field("GetAssistantByPeriodId")
@jwt_required
def getAssistantByPeriodID(_, info, period_id):
    # for fnode in info.field_nodes:
    #     print([f.name.value for f in fnode.selection_set.selections])
    return assistant.getAssistantByPeriodID(period_id)
