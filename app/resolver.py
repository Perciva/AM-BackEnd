import requests

def hello_resolver(_,info):
    print(info)
    return "Hello There!!!"

def getUser(_,info,username, password):
    URL = "https://laboratory.binus.ac.id/lapi/api/Account/LogOnQualification"

    d ={
        "username" : username,
        "password" : password
    }

    x = requests.post(URL,data = d)
    return x.json()
    






