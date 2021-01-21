from app.model import attendance
from app.database import query, mutation


@mutation.field("InsertAttendance")
def insertAttendance(_, info, assistant_initial, period_id, date, _in, _out):
    return attendance.insert(assistant_initial, period_id, date, _in, _out)


@query.field("GetAllAttendanceByDate")
def getAllAttendanceByDate(_, info, start_date, end_date, assistant_id):
    return attendance.getAllAttendanceByDate(start_date, end_date, assistant_id)

@mutation.field("UpdateAttendance")
def updateAttendance(_, info, id, in_permission, out_permission, special_permission,
                     in_permission_description,
                     out_permission_description, special_permission_description):

    return attendance.update(id, in_permission, out_permission, special_permission,
                             in_permission_description,
                             out_permission_description, special_permission_description)

@query.field("GetAttendanceSummary")
def getAssistantAttendanceSummary(_, info, assistant_id, period_id, start_date, end_date):
    return attendance.getAttendanceSummary(assistant_id, period_id, start_date, end_date)

# @query.field("GetAllAssistantAttendanceSummary")
def getAllAssistantAttendanceSummary(_, info, period_id, start_date, end_date):
    return

def getAllAssistantAttendanceSummaryByLeader(_, info, period_id, leader_id, start_date, end_date):
    return
