from app.model import holiday
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

def InsertHoliday(_, info, period_id, description, date):
    return holiday.insert(period_id,description,date)

def DeleteHoliday(_, info, id):
    return holiday.delete(id)

def UpdateHoliday(_, info, id, description, date):
    return holiday.update(id,description,date)

def getHolidayByPeriodID(_, info, period_id):
    return holiday.getAllHolidayByPeriodID(period_id)