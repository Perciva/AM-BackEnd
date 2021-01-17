from app.model import leader
from app.database import query, mutation


@mutation.field("InsertLeader")
# @jwt_required
def InsertLeader(_,info,period_id, initial, name):
    return leader.insert(period_id, initial, name)

@mutation.field("DeleteLeader")
# @jwt_required
def DeleteLeader(_,info,id):
    return leader.delete(id)

@mutation.field("UpdateLeader")
# @jwt_required
def UpdateLeader(_,info,id, initial, name):
    return leader.update(id, initial, name)

@query.field("GetLeaderById")
# @jwt_required
def getLeaderByID(_,info,id):
    return leader.getLeaderByID(id)

@query.field("GetLeaderByPeriodId")
# @jwt_required
def getLeaderByPeriodID(_,info, period_id):
    l=leader.getLeaderByPeriodID(period_id)
    return l

@query.field("GetLeaderByInitialAndPeriodId")
# @jwt_required
def getLeaderByInitialAndPeriod(_,info, initial, period_id):
    l = leader.getLeaderByInitialAndPeriod(initial, period_id)
    return l