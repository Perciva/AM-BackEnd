from app.model import period
from app.database import query, mutation

@query.field("GetAllPeriods")
# @jwt_required
def getAllPeriods(_,info):
    res = period.getAllPeriod()
    return res

@mutation.field("InsertPeriod")
# @jwt_required
def InsertPeriod(_,info,description,start,end):
    period.insert(description, start, end)
    return True

@mutation.field("UpdatePeriod")
# @jwt_required
def UpdatePeriod(_,info, id, description, start, end):
    return period.update(id, description, start, end)

@mutation.field("DeletePeriod")
# @jwt_required
def DeletePeriod(_,info,id):
    period.delete(id)
    return True