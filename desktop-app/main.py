import tkinter as tk
from fastapi import FastAPI
import httpx
from pymongo import MongoClient

CON_STR = "mongodb+srv://19294349:zJ89G0MBMxhdR1nf@base.vrtfupp.mongodb.net/?retryWrites=true&w=majority&appName=base"

def get_database(dbname):
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CON_STR)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client[dbname]

ADMIN_DB = get_database('adminservice')

URL_ADMIN_AUTH = ADMIN_DB['comp7033ip'].find_one({'adminauth' : 'adminauth'})['url']
print(URL_ADMIN_AUTH)
URL_ADMIN_SERVICE = ADMIN_DB['comp7033ip'].find_one({'adminservice' : 'adminservice'})['url']
print(URL_ADMIN_SERVICE)

token = ""



window = tk.Tk()

def make_button(btn_txt, btn_master, btn_cmd):
    return tk.Button(
    master=btn_master,
    text=btn_txt,
    width=20,
    height=3,
    command=btn_cmd
    )

def manage_admin():
    return

def login_event(username_entry, password_entry):
    print("logging in")
    username = username_entry.get()
    password = password_entry.get()
    print("found username and password")
    client = httpx.Client()
    try:
        response = client.get(URL_ADMIN_AUTH + "login", params = {"username" : username, "password" : password})
    except Exception as e:
        goto_login("login failed, please try again")
    global token
    token = response.json()
    main_screen()

def show_single_admin(user):
    global frame4
    global window
    frame4.destroy()
    frame4 = tk.Frame(master=window, width=50, bg="orange")
    frame4.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    admin_label = tk.Label(text="name: " + user['name'] + " - Permissions: " + str(user['adminPermission']) + " - username: " + user['username'], master=frame4)
    admin_label.pack()

def register_event(u_e, pa_e, n_e, pe_e):
    username = u_e.get()
    password = pa_e.get()
    name = n_e.get()
    permission = pe_e.get()

    client = httpx.Client()
    try:
        response = client.post(URL_ADMIN_SERVICE, params = {"username" : username, "password" : password, 'admin_name' : name, 'admin_permission': permission, 'token' : token})
    except Exception as e: 
        print('registration failed')
    main_screen()

def create_new_admin():
    create_admin_window = tk.Tk()
    register_frame = tk.Frame(master=create_admin_window).pack()
    login_label = tk.Label(master=register_frame, text="register new admin: ")
    login_label.pack()
    username_entry = tk.Entry(master=register_frame)
    username_entry.insert(0,"unique username")
    username_entry.pack()
    password_entry = tk.Entry(master=register_frame)
    password_entry.insert(0,"password")
    password_entry.pack()
    name_entry = tk.Entry(master=register_frame)
    name_entry.insert(0, "name")
    name_entry.pack()
    permission_entry = tk.Entry(master=register_frame)
    permission_entry.insert(0,"permission level")
    permission_entry.pack()
    login_btn = tk.Button(master=window, text="register new admin", command= lambda : register_event(username_entry, password_entry, name_entry, permission_entry))
    login_btn.pack()
    create_admin_window.mainloop()

def show_all_admins():
    global frame3
    global frame4
    global window
    frame3.destroy()
    frame4.destroy()
    frame3 = tk.Frame(master=window, width=50, bg="blue")
    frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    frame4 = tk.Frame(master=window, width=50, bg="orange")
    frame4.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    print("show all admins: " + token)
    client = client = httpx.Client()
    try:
        response = client.get(URL_ADMIN_SERVICE , params = {"token" : token})
    except Exception as e:
        print("error in getting all admins")
    all_admins = response.json()
    for admin in all_admins:
        frame5 = tk.Frame(master=frame3, width=100)
        admin_label = tk.Label(text="name: " + all_admins[admin]['name'] + " - Permissions: " + str(all_admins[admin]['adminPermission']) + " - username: " + all_admins[admin]['username'], master=frame5)
        button = make_button(all_admins[admin]['name'], frame5, lambda : show_single_admin(all_admins[admin]))
        admin_label.pack()
        button.pack()
        frame5.pack()
    

def goto_login(fail : str = 'log in'):
    #clean and set up login screen
    global window
    window.destroy()
    window = tk.Tk()
    login_frame = tk.Frame(master=window).pack()
    login_label = tk.Label(master=login_frame, text=fail)
    login_label.pack()
    username_label = tk.Label(master=login_frame, text="Please enter your username:")
    username_label.pack()
    username_entry = tk.Entry(master=login_frame, textvariable="username")
    username_entry.pack()
    passwork_label = tk.Label(master=login_frame, text="Please enter your password:")
    passwork_label.pack()
    password_entry = tk.Entry(master=login_frame, textvariable="password")
    password_entry.pack()
    login_btn = tk.Button(master=window, text="login", command= lambda : login_event(username_entry, password_entry))
    login_btn.pack()
    window.mainloop()

def main_screen():
    #clean and the set up main usage mode
    global window
    window.destroy()
    window = tk.Tk()
    frame1 = tk.Frame(master=window, width=100, height=100)
    frame1.pack(fill=tk.BOTH, side=tk.LEFT)
    frame2 = tk.Frame(master=window, width=100, bg="yellow")
    frame2.pack(fill=tk.BOTH, side=tk.LEFT)
    global frame3
    frame3 = tk.Frame(master=window, width=50, bg="blue")
    frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    global frame4
    frame4 = tk.Frame(master=window, width=50, bg="orange")
    frame4.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    button1 = make_button("Managing Adminstration Staff", frame1, manage_admin)
    button1.pack()
    button2 = make_button("Click me!", frame1, manage_admin)
    button2.pack()
    btn_show_admins = make_button("Show All Admins", frame2, show_all_admins)
    btn_show_admins.pack()
    btn_new_admin = make_button("Create New Admin", frame2, create_new_admin)
    btn_new_admin.pack()
    window.mainloop()


    



def handle_click():
    btn_new_admin.pack()






goto_login()