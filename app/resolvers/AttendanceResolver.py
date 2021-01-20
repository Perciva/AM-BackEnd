from app.model import attendance
from app.database import query, mutation

@mutation.field("InsertAttendance")
def insertAttendance(_, info, assistant_initial, date, _in, _out):
    return attendance.insert(assistant_initial, date, _in, _out)

@query.field("GetAllAttendanceByDate")
def getAllAttendanceByDate(_, info, start_date, end_date, assistant_id):
    return attendance.getAllAttendanceByDate(start_date, end_date, assistant_id)









