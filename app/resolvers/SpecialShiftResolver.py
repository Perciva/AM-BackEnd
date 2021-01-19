from app.model import special_shift
from app.database import query, mutation


@mutation.field("InsertSpecialShift")
def insertSpecialShift(_, info, period_id, description, assistant_ids, date, _in, _out):
    res = special_shift.insert(period_id, description, assistant_ids, date, _in, _out)
    return res

@mutation.field("UpdateSpecialShift")
def updateSpecialShift(_, info, id, period_id, description, assistant_ids, date, _in, _out):
    res = special_shift.update(id,period_id, description, assistant_ids, date, _in, _out)
    return res

@mutation.field("DeleteSpecialShift")
def deleteSpecialShift(_, info, id):
    return special_shift.delete(id)

@query.field("GetSpecialShiftByPeriodId")
def getSpecialShiftByPeriodId(_, info, period_id):
    return special_shift.getAllSpecialShiftByPeriodId(period_id)
