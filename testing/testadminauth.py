from fastapi import FastAPI
from bson.objectid import ObjectId
import bcrypt
from datetime import datetime, timedelta
import secrets
import httpx
from contextlib import asynccontextmanager
import os
import socket
import asyncio
import time

token = "testuserP9rvxGnBfMsbwYAEaBUJMzZMTek"

async def get_num_admins():
    client = httpx.AsyncClient()
    print(f"Started: {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')}")
    response = await client.get("http://108.59.80.98:50050/" + "", params = {'token' : token})
    print(f"Ended: {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')}")
    return len(response.json())


async def main(min, max):  
    print(await get_num_admins())
    permission = 0
    start = datetime.now()
    print(f"Started: {start.isoformat(sep=' ', timespec='milliseconds')}")
    #make 1000 register new user requests
    for i in range(min,max):
        username = "testregisternewusers" + str(i)
        password = username
        name = username
        client = httpx.AsyncClient()
        response = await client.post("http://108.59.80.98:50050/", params = {'username' : username, 'password' : password, 'admin_name' : name, 'admin_permission' : permission, 'token' : token})
    #see how many admins we have
    print(await get_num_admins())

    #archive the created admins
    for i in range(min,max):
        username = "testregisternewusers" + str(i)
        client = httpx.AsyncClient()
        response = await client.delete("http://108.59.80.98:50050/" + username, params = {'token' : token})
    #see how many admins we have
    print(await get_num_admins())

    end = datetime.now()
    print(f"Ended: {end.isoformat(sep=' ', timespec='milliseconds')}")
    delta = end - start
    avg_delta = delta / (max-min-1)
    print(f"delta = {delta}")
    print(f"avg. delta = {avg_delta}")



async def get_test(min,max):
    start = datetime.now()
    print(f"Started: {start.isoformat(sep=' ', timespec='milliseconds')}")

    for i in range(min,max):
        client = httpx.AsyncClient()
        response = await client.get("http://108.59.80.98:50050/" + "testuser", params = {'token' : token})
    end = datetime.now()
    print(f"Ended: {end.isoformat(sep=' ', timespec='milliseconds')}")
    delta = end - start
    avg_delta = delta / (max-min-1)
    print(f"delta = {delta}")
    print(f"avg. delta = {avg_delta}")

async def validate_test(min,max):
    start = datetime.now()
    print(f"Started: {start.isoformat(sep=' ', timespec='milliseconds')}")

    for i in range(min,max):
        client = httpx.AsyncClient()
        response = await client.get("http://35.223.174.9:50055/" + "validate", params = {'token' : token})
    end = datetime.now()
    print(f"Ended: {end.isoformat(sep=' ', timespec='milliseconds')}")
    delta = end - start
    avg_delta = delta / (max-min-1)
    print(f"delta = {delta}")
    print(f"avg. delta = {avg_delta}")

    


async def heavy_load():
    task_1 = asyncio.create_task(main(0,50))
    task_2 = asyncio.create_task(main(50,100))
    task_3 = asyncio.create_task(main(100,150))
    task_4 = asyncio.create_task(main(150,200))
    task_5 = asyncio.create_task(main(200,250))
    task_6 = asyncio.create_task(main(250,300))
    task_7 = asyncio.create_task(main(300,350))
    task_8 = asyncio.create_task(main(350,400))
    task_9 = asyncio.create_task(main(400,450))
    task_10 = asyncio.create_task(main(450,500))
    task_11 = asyncio.create_task(main(500,550))
    task_12 = asyncio.create_task(main(550,600))
    task_13 = asyncio.create_task(main(600,650))

    print(f"Started: {time.strftime('%X')}")
    await task_1
    await task_2
    await task_3
    await task_4
    await task_5
    await task_6
    await task_7
    await task_8
    await task_9
    await task_10
    await task_11
    await task_12
    await task_13                               
    print(f"Ended: {time.strftime('%X')}")

