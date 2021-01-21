from flask_jwt_extended import jwt_required

from app.model import attendance
from app.database import query, mutation, sess


@mutation.field("InsertAttendance")
@jwt_required
def insertAttendance(_, info, assistant_initial, period_id, date, _in, _out):
    return attendance.insert(assistant_initial, period_id, date, _in, _out)


@query.field("GetAllAttendanceByDate")
@jwt_required
def getAllAttendanceByDate(_, info, start_date, end_date, assistant_id):
    return attendance.getAllAttendanceByDate(start_date, end_date, assistant_id)


@mutation.field("UpdateAttendance")
@jwt_required
def updateAttendance(_, info, id, in_permission, out_permission, special_permission,
                     in_permission_description,
                     out_permission_description, special_permission_description):
    return attendance.update(id, in_permission, out_permission, special_permission,
                             in_permission_description,
                             out_permission_description, special_permission_description)


@query.field("GetAttendanceSummary")
@jwt_required
def getAssistantAttendanceSummary(_, info, assistant_id, period_id, start_date, end_date):
    return attendance.getAttendanceSummary(assistant_id, period_id, start_date, end_date, "")


@query.field("GetAllAssistantAttendanceSummary")
@jwt_required
def getAllAssistantAttendanceSummary(_, info, period_id, start_date, end_date):
    from app.model.assistant import Assistant
    from app.model.leader import Leader

    result = list()

    leaders = sess.query(Leader).filter(Leader.period_id == period_id).all()

    for l in leaders:
        assistants = sess.query(Assistant).filter(Assistant.period_id == period_id).filter(
            Assistant.leader_id == l.id).all()
        for s in assistants:
            result.append(attendance.getAttendanceSummary(s.id, period_id, start_date, end_date, l.initial))

    return result

@query.field("GetAllAssistantAttendanceSummaryByLeader")
@jwt_required
def getAllAssistantAttendanceSummaryByLeader(_, info, period_id, leader_id, start_date, end_date):
    from app.model.assistant import Assistant

    assistants = sess.query(Assistant).filter(Assistant.leader_id == leader_id).filter(
        Assistant.period_id == period_id).all()

    result = list()
    for s in assistants:
        result.append(attendance.getAttendanceSummary(s.id, period_id, start_date, end_date, ""))

    return result
