from fastapi import FastAPI
from bson.objectid import ObjectId
import httpx

app = FastAPI()

from pymongo import MongoClient

CON_STR = "mongodb+srv://19294349:zJ89G0MBMxhdR1nf@base.vrtfupp.mongodb.net/?retryWrites=true&w=majority&appName=base"


def get_database(dbname):
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CON_STR)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client[dbname]


TEACHER_DB = get_database('teacherstub')

#return teacher staff record for specified teacher username
@app.get("/{username}")
async def get_one_teacher(username : str):
    try:
        staff = TEACHER_DB['teacherservice'].find_one({'username' : username})
        staff['_id'] = str(staff['_id']) #caste _id from bson objectID to python str
        return staff
    except Exception as e:
        return "adminstaff find db error"

#return all teaching staff in db, returns false if error
@app.get("/")
async def get_all_teachers(): 
    dict_to_return = {}
    try: 
        for x in TEACHER_DB['teacherservice'].find():
            x['_id'] = str(x['_id']) #caste _id from bson objectID to python str
            dict_to_return.update({x['username']:x})
    except Exception as e:
        return "admin staff update db error"
    return dict_to_return


#update record for given teacher, returns their username, false if error
@app.put("/{username}")
async def update_teacher(username : str, course : str):  
    query_filter = {'username' : username}
    try:
        teacher = TEACHER_DB['teacherservice'].find_one(query_filter)
        courses = teacher['courses']
    except Exception as e:
        return "falied to find teacher to update"

    update_operation = { '$set' : {'courses' : courses + "," + course}}
    try:
        TEACHER_DB['teacherservice'].update_one(query_filter, update_operation)
    except Exception as e:
        return "name update error"       
    return username
