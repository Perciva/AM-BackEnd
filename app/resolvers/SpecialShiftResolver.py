from app.model import special_shift
from app.database import query, mutation


@mutation.field("InsertSpecialShift")
def insertSpecialShift(_, info, period_id, description, assistant_ids, date, _in, _out):
    special_shift.insert(period_id, description, assistant_ids, date, _in, _out)
    return "HEHE"
