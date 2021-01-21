from app.model import shift
from app.database import query, mutation


@mutation.field("InsertShift")
def insertShift(_, info, assistant_id, day, _in, _out):
    return shift.insert(assistant_id, day, _in, _out)

@mutation.field("InsertShiftByAssistantInitial")
def insertShiftByAssistantInitial(_, info, assistant_initial, period_id, day, _in, _out):
    return shift.insertByAssistatInitial(assistant_initial,period_id, day, _in, _out)


@mutation.field("UpdateShift")
def updateShift(_, info, id, assistant_id, day, _in, _out):
    return shift.update(id, assistant_id, day, _in, _out)


@mutation.field("DeleteShift")
def deleteShift(_, info, id):

    shift.delete(id)
    return True


@mutation.field("DeleteAllAssistantShifts")
def deleteAllAssistantShift(_, info, assistant_id):
    return shift.deleteAllAssistantShift(assistant_id)


@query.field("GetAssistantShifts")
def getAssistantShift(_, info, assistant_id):
    return shift.getAssistantShifts(assistant_id)
