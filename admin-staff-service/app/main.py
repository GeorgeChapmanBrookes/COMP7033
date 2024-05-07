from fastapi import FastAPI
from bson.objectid import ObjectId
import httpx

app = FastAPI()

from pymongo import MongoClient

CON_STR = "mongodb+srv://19294349:zJ89G0MBMxhdR1nf@base.vrtfupp.mongodb.net/?retryWrites=true&w=majority&appName=base"
URL_ADMIN_AUTH = "http://localhost:8001/"
URL_TEACHER_STUB = "http://34.42.225.123:55000/"

#permissions:
#0=can do anything
#1=cannot archive, can create, edit, read
#2=cannot archive, create, or edit, can read

def get_admin_auth():
    record = ADMIN_DB['comp7033ip'].find_one({'adminauth' : 'adminauth'})
    return record['url']


def get_database(dbname):
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CON_STR)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client[dbname]

#get username from token
async def get_username(token :str):
    client = httpx.AsyncClient()
    response = await client.get(get_admin_auth() + "username", params = {"token" : token})
    return response.json()

    
  
#find and return the permission level of a given admin
async def get_auth(token : str):
    try:
        username = await get_username(token)
        staff = ADMIN_DB['adminstaff'].find_one({'username' : username})
    except Exception as e:
        return "auth check failed"
    return staff['adminPermission']


ADMIN_DB = get_database('adminservice')

async def validate_token(token : str):
    client = httpx.AsyncClient()
    response = await client.get(get_admin_auth() + "validate", params = {"token" : token})
    return response.json()


#return all archived staff
@app.get("/archive")
async def get_archived_admin_staff(token : str):
    if not await validate_token(token):
        return "Invalid Token"
    try:
        if await get_auth(token) not in range(0,1):
            return "Insufficient Privileges"
    except Exception as e:
        return "auth check failed"

    dict_to_return = {}

    try: 
        i = 1
        for x in ADMIN_DB['adminstaffarchive'].find():
            x['_id'] = str(x['_id']) #caste _id from bson objectID to python str
            dict_to_return.update({i:x})
            i += 1
    except Exception as e:
        return "archive db error"

    return dict_to_return

#use teacher stub to test
@app.get("/teachers/one")
async def get_one_admin_staff(username : str, token : str):
    if not await validate_token(token):
        return "Invalid Token"
    if await get_auth(token) not in range(0,3):
        return "Insufficient Privileges"
    
    try: 
        client = httpx.AsyncClient()
        response = await client.get(URL_TEACHER_STUB + username)
        return response.json()
    except Exception as e:
        return "failed to get teacher from api"
    
#use teacher stub to test
@app.get("/teachers/all")
async def get_one_admin_staff(token : str):
    if not await validate_token(token):
        return "Invalid Token"
    if await get_auth(token) not in range(0,3):
        return "Insufficient Privileges"
    
    try: 
        client = httpx.AsyncClient()
        response = await client.get(URL_TEACHER_STUB)
        return response.json()
    except Exception as e:
        return "failed to get all teachers from api"
    
#use teacher stub to test
@app.put("/teachers/{username}/")
async def get_one_admin_staff(username : str, course : str, token : str):
    if not await validate_token(token):
        return "Invalid Token"
    if await get_auth(token) not in range(0,1):
        return "Insufficient Privileges"
    
    try: 
        client = httpx.AsyncClient()
        response = await client.put(URL_TEACHER_STUB + username, params={'course' : course})
        return response.json()
    except Exception as e:
        return "failed to update teacher in api"

#return admin staff record for specified id
@app.get("/{username}")
async def get_one_admin_staff(username : str, token : str):
    if not await validate_token(token):
        return "Invalid Token"
    if await get_auth(token) not in range(0,3):
        return "Insufficient Privileges"
    try:
        staff = ADMIN_DB['adminstaff'].find_one({'username' : username})
        staff['_id'] = str(staff['_id']) #caste _id from bson objectID to python str
        return staff
    except Exception as e:
        return "adminstaff find db error"




#return all admin staff in db, returns false if error
@app.get("/")
async def get_all_admin_staff(token : str):
    if not await validate_token(token):
        return "Invalid Token"
    if await get_auth(token) not in range(0,3):
        return "Insufficient Privileges"
    
    dict_to_return = {}

    try: 
        for x in ADMIN_DB['adminstaff'].find():
            x['_id'] = str(x['_id']) #caste _id from bson objectID to python str
            dict_to_return.update({x['username']:x})
    except Exception as e:
        return "admin staff update db error"

    return dict_to_return


#create new record for given admin member, returns their id, false if error
@app.post("/")
async def create_new_admin_staff(username :str, password :str, admin_name : str, admin_permission : int, token : str):
    if not await validate_token(token):
        return "Invalid Token"
    if await get_auth(token) not in range(0,2):
        return "Insufficient Privileges"

    try:
        client = httpx.AsyncClient()
        response = await client.get(get_admin_auth() + "register/newuser", params = {'username' : username, 'password' : password})
        insert = ADMIN_DB['adminstaff'].insert_one({'username' : username, 'name' : admin_name, 'adminPermission' : admin_permission})
        return username
    except Exception as e:
        return "adminstaff insert db error"

#update record for given admin member, returns their id, false if error
@app.put("/{username}")
async def update_admin_staff(username : str, token : str, admin_name : str | None = None, admin_permission : int | None = None):
    if not await validate_token(token):
        return "Invalid Token"
    if await get_auth(token) not in range(0,2):
        return "Insufficient Privileges"
    
    query_filter = {'username' : username}
    update_operation = { '$set' : {'name' : admin_name}}

    if admin_name != None :
        try:
            ADMIN_DB['adminstaff'].update_one(query_filter, update_operation)
        except Exception as e:
            return "name update error"
        
    update_operation = { '$set' : {'adminPermission' : admin_permission}}

    if admin_permission != None :
        try:
            ADMIN_DB['adminstaff'].update_one(query_filter, update_operation)
        except Exception as e:
            return "permission update error"
        
    return username

#archives given record, returns id, false if error
@app.delete("/{username}")
async def archive_admin_staff(username : str, token : str):
    if not await validate_token(token):
        return "Invalid Token"
    if await get_auth(token) not in range(0,1):
        return "Insufficient Privileges"

    
    try:
        staff = ADMIN_DB['adminstaff'].find_one({'username' : username})
        staff['_id'] = str(staff['_id']) #caste _id from bson objectID to python str
    except Exception as e:
        return "admin staff find db error"
    
    try:
        ADMIN_DB['adminstaffarchive'].insert_one({'username' : staff['username'], 'name' : staff['name'], 'adminPermission' : staff['adminPermission'], 'oldId' : staff['_id']})
    except Exception as e:
        return "archive insert db error"

    try:
        ADMIN_DB['adminstaff'].delete_one({'username' : username})
    except Exception as e:
        return "admin staff delete db error"



    return username

@app.put("/url/admin/auth")
async def assign_url_admin_auth(url : str):
    global URL_ADMIN_AUTH
    ADMIN_DB['comp7033ip'].update_one({'adminauth' : 'adminauth'}, {'$set' : {'url' : url}}, upsert = True)
    URL_ADMIN_AUTH = url
    return True