import requests
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.model import period


try:
    from app.resolvers.LeaderResolver import *
    from app.resolvers.PeriodResolver import *
    from app.resolvers.AssistantResolver import *
except ImportError:
    print ('importing modulename failed')
    
@jwt_required
def hello_resolver(_,info):
    print(info)
    return "Hello There!!!"

def getUser(_,info,username, password):
    URL = "https://laboratory.binus.ac.id/lapi/api/Account/LogOnQualification"

    access_token = create_access_token(identity=username)

    d ={
        "username" : username,
        "password" : password
    }

    x = requests.post(URL,data = d)
    if(x.text == 'null'):
        return 'null'
    else :
        resp = {
            "UserData": x.json(),
            "Token" :  access_token
        }
        return resp



   






