from flask_jwt_extended import jwt_required

from app.model import holiday
from app.database import query, mutation


@mutation.field("InsertHoliday")
@jwt_required
def InsertHoliday(_, info, period_id, description, date):
    return holiday.insert(period_id, description, date)


@mutation.field("DeleteHoliday")
@jwt_required
def DeleteHoliday(_, info, id):
    return holiday.delete(id)


@mutation.field("UpdateHoliday")
@jwt_required
def UpdateHoliday(_, info, id, description, date):
    return holiday.update(id, description, date)


@query.field("GetHolidayByPeriodId")
@jwt_required
def getHolidayByPeriodID(_, info, period_id):
    return holiday.getAllHolidayByPeriodID(period_id)
