from fastapi import FastAPI
from bson.objectid import ObjectId
import bcrypt
from datetime import datetime, timedelta
import secrets
import httpx
from contextlib import asynccontextmanager
import os
import socket




from pymongo import MongoClient

CON_STR = "mongodb+srv://19294349:zJ89G0MBMxhdR1nf@base.vrtfupp.mongodb.net/?retryWrites=true&w=majority&appName=base"

URL_ADMIN_SERVICE = "http://localhost:8000/"

#permissions:
#0=can do anything
#1=cannot archive, can create, edit, read
#2=cannot archive, create, or edit, can read


#return db object to use
def get_database(dbname):
   client = MongoClient(CON_STR)
 
   return client[dbname]

#creates, saves and returns token for session for user
def valid_login(username : str):
    token = username + secrets.token_urlsafe(20)
    try:
        ADMIN_DB['adminlogin'].update_one({'username' : username}, { '$set' : {'token': token, 'timestamp' : datetime.now()}})
        return token
    except Exception as e:
        return e


#check if given token is still within valid time window
async def check_valid_token(token : str):
    one_day = timedelta(days=1)
    current_time = datetime.now()

    try:
        user = ADMIN_DB['adminlogin'].find_one({'token' : token})
        timestamp = user['timestamp']
        if (timestamp + one_day) < current_time:
            ADMIN_DB['adminlogin'].update_one({'token' : token}, { '$set' : {'token': '', 'timestamp' : datetime.now()}})            
            return False
        else:
            return True
    except Exception as e:
        return False





# Hash a password
def hash_password(raw_password : str):
    hashed_password = bcrypt.hashpw(raw_password.encode(encoding = 'UTF-8'), bcrypt.gensalt())
    return hashed_password

# Verify a password
def verify_password(raw_password : str, hashed_password : str):
    if bcrypt.checkpw(raw_password.encode(encoding = 'UTF-8'), hashed_password):
        return True
    else:
        return False
  
ADMIN_DB = get_database('adminservice')


def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
        print(get_ip())

@asynccontextmanager
async def lifespan(app: FastAPI):
    #TODO: things to do at launch
    print(get_ip())
    ADMIN_DB['comp7033ip'].update_one({'adminauth' : 'adminauth'}, {'$set' : {'ip' : get_ip()}}, upsert = True)
    yield

app = FastAPI(lifespan=lifespan)

#register new suer and return token for session valid for a day
@app.get("/register/newuser")
async def register(username : str, password : str):
    already_exists = False
    try:
        staff = ADMIN_DB['adminlogin'].find_one({'username' : username})
        staff['_id'] = str(staff['_id'])
        already_exists = True
    except Exception as e:
        already_exists = False
    if already_exists:
        return "username already exists"
    #add user to db
    try:
        ADMIN_DB['adminlogin'].insert_one({'username' : username, 'password' : hash_password(password), 'token': '', 'timestamp' : datetime.now()})
        token = valid_login(username)
    except Exception as e:
        return "failed creating new user entry/token"
    return token

    
        

#login and set token for a day
@app.get("/login")
async def login(username : str, password : str):
    #check if valid username
    try:
        staff = ADMIN_DB['adminlogin'].find_one({'username' : username})
        staff['_id'] = str(staff['_id'])
    except Exception as e:
        return "username or password incorrect"
    #username exists, now check password
    if verify_password(password, staff['password']):
        token = valid_login(username)
    else:
        return "username or password incorrect"    
    return token

#check if token is still valid, returns true if so, false if not
@app.get("/validate")
async def validate(token : str):
    return await check_valid_token(token)


@app.get("/username")
async def return_username(token :str):
    try:
        staff = ADMIN_DB['adminlogin'].find_one({'token' : token})
    except Exception as e:
        return False
    return staff['username']


@app.put("/url/admin/service")
async def assign_url_admin_service(url : str):
    global URL_ADMIN_SERVICE
    ADMIN_DB['comp7033ip'].update_one({'adminservice' : 'adminservice'}, {'$set' : {'url' : url}}, upsert = True)
    URL_ADMIN_SERVICE = url
    return True
