import requests
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.model import period
from app.database import query

try:
    from app.resolvers.LeaderResolver import *
    from app.resolvers.PeriodResolver import *
    from app.resolvers.AssistantResolver import *
    from app.resolvers.HolidayResolver import *
    from app.resolvers.ShiftResolver import *
    from app.resolvers.SpecialShiftResolver import *
    from app.resolvers.AttendanceResolver import *
except ImportError:
    print('importing modulename failed')


@query.field("GetUser")
def getUser(_, info, username, password):
    URL = "https://laboratory.binus.ac.id/lapi/api/Account/LogOnQualification"

    access_token = create_access_token(identity=username)

    d = {
        "username": username,
        "password": password
    }
    # temporary = {
    #     "Major" : "asd",
    #     "Name" : "asd",
    #     "Role" : "asd",
    #     "UserId": 1,
    #     "UserName" : "asdasd"
    # }
    # resp = {
    #         "UserData": None,
    #         "Token" :  access_token
    #     }

    x = requests.post(URL, data=d)
    x = x.json()
    print(x)
    if x is None:
        return 'null'
    # elif "Software Assistant Supervisor" not in x["Role"]:
    #     return "null"
    else:
        resp = {
            "UserData": x,
            "Token": access_token
        }
    return resp
