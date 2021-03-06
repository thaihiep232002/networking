import socket
import json
from threading import Thread
from tkinter import *
from tkinter import messagebox
from datetime import date, timedelta
from datetime import datetime as dt
import time

SERVER_HOST = input("Input IP: ")
SERVER_PORT = int(input("Input Port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER_HOST,SERVER_PORT))

welcome = client.recv(1024).decode("utf-8")
print(welcome)

window = Tk()
icon = PhotoImage(file='logo_client.png')
window.iconphoto(True, icon)
window.geometry("1150x720")
window.title("Forex Rate")
cnt = 0
user = {}
date_ = {}
# user : name; pass; msg(thay đổi)

#                  ======= GUI - Login ========
background_image= PhotoImage(file = "br_client.png")
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
# =====LOGO=====
frame_logo = Frame(window, bg = "white", bd = 5)
frame_logo.place(x = 75, y = 125, height = 250, width = 350)
logo = Label(frame_logo, text = "FOREX RATE", font =("Impact", 75, "bold"), fg = "#D2691E")
logo.place(x = 10, y = 20)
# =====Frame-LOGIN======
frame_login = Frame(window, bg = "white", bd = 5)
frame_login.place(x = 75, y = 275, height = 250, width = 350)
title_login = Label(frame_login, text = "Log In", font =("Impact", 45), fg = "#488AC7")
title_login.place(x = 10, y = 0)
user_label = Label(frame_login, text = "Username :")
user_label.place(x = 10, y = 70)
user_entry = Entry(frame_login, width = 20)
user_entry.place(x = 10, y = 90)
pass_label = Label(frame_login, text = "Password :")
pass_label.place(x = 10, y = 120)
pass_entry = Entry(frame_login,width = 20, show="*")
pass_entry.place(x = 10, y = 140)
login_button = Button(frame_login,
    text="Log In",
    padx = 5,
    fg = "#488AC7",
    relief=RAISED,\
        cursor="fleur",
    command = lambda: (
    Handle_login(user, user_entry, pass_entry)
    )
)
login_button.place(x = 10, y = 180)
signup_button = Button(frame_login,
    text="Sign Up",
    padx = 5,
    fg = "#488AC7",
    relief=RAISED,\
        cursor="fleur",
    command = lambda: (
    Handle_signup(user, user_entry, pass_entry)
    )
)
signup_button.place(x = 70, y = 180)

class Table:
    # array entry
    def __init__(self,root,data_server,total_rows,total_columns):
        for i in range(total_rows - 1):
            for j in range(total_columns):
                self.e = Entry(root, width=20, font=('Arial',16))
                self.e.grid(row=i, column=j)
                self.e.insert(END, data_server[i][j])
        self.t = Entry(root, width=20, font=('Arial',16))
        self.t.insert(END,data_server[total_rows - 1])
        self.t.grid(row=total_rows,column = 4)

class Table_Current:
    # array entry
    def __init__(self,root,data_server,total_rows,total_columns):
        for i in total_rows:
            for j in range(total_columns):
                self.e = Entry(root, width=20, font=('Arial',16))
                self.e.grid(row=i, column=j)
                self.e.insert(END, data_server[i][j])

def Accept_login(user):
    client.sendall(json.dumps(user).encode("utf-8"))
    recv_str = client.recv(1024).decode("utf-8")
    if recv_str == "login_success":
        return True
    elif recv_str == "login_fail":
        return False
    if recv_str == "": 
        messagebox.showwarning('Forex Rate', 'Server Disconnected!') 
        return False

def Accept_signup(user):
    client.sendall(json.dumps(user).encode("utf-8"))
    recv_str = client.recv(1024).decode("utf-8")
    if recv_str == "sign_up_success":
        return True
    elif recv_str == "sign_up_fail":
        return False  
    if recv_str == "":
        messagebox.showwarning('Forex Rate', 'Server Disconnected!') 
        return False

def Handle_login(user, user_entry, pass_entry):
    client.sendall("login".encode("utf-8"))
    user["name"] = user_entry.get()
    user["password"] = pass_entry.get()
    if Accept_login(user):
        global root
        root = Toplevel()
        root.geometry("1100x850")
        root.title("Forex Rate")
        Start(True, True)
    else:
        messagebox.showerror('Forex Rate', 'Your Account Not Approved Yed!')

def Enter_login(event):
    Handle_login(user, user_entry, pass_entry)

def Handle_signup(user, user_entry, pass_entry):
    client.sendall("sign_up".encode("utf-8"))
    user["name"] = user_entry.get()
    user["password"] = pass_entry.get()
    if Accept_signup(user):
        messagebox.showinfo('Forex Rate', 'Sign Up Successful!')
    else:
        messagebox.showwarning('Forex Rate', 'Account Already Exists!')

def getOne():
    global cnt
    cnt += 1

def Compare_day(day1, day2):
    try:
        a = dt.strptime(day1, "%Y-%m-%d")
        b = dt.strptime(day2, "%Y-%m-%d")
        if a > b:
            return True
        elif a < b:
            return False
    except:
        return -1

def One():
    global cnt
    cnt += 1

def on_closing():
    user["msg"] = "quit"
    client.sendall(json.dumps(user).encode("utf-8"))
    root.destroy()

def clear_frame(param):
   for widgets in param.winfo_children():
      widgets.destroy()

def Search_date_main(date_, search_date_entry):
    date_["search"] = search_date_entry.get()

def Start(flag, day_cur):
    if (flag == True):
        frame_logo_root = Frame(root, bg = "white", bd = 5)
        frame_logo_root.place(x = 0, y = 0, height = 250, width = 350)
        logo_root = Label(frame_logo_root, text = "FOREX RATE", font =("Impact", 50, "bold"), fg = "#D2691E")
        logo_root.place(x = 10, y = 10)
        name_user = Label(root, text = "Welcome {}!".format(user["name"]), font =("Impact", 25, "bold"), fg = "#488AC7")
        name_user.place(x = 700, y = 20)
        search_root = Frame(root, bg = "white", bd = 5)
        search_root.place(x = 700, y = 60, height = 40, width = 300)
        global search_entry
        search_entry = Entry(search_root, width=20)
        search_entry.grid(row =1, column = 1)
        # 
        search_date_root = Frame(root, bg = "white", bd = 5)
        search_date_root.place(x = 750, y = 790, height = 40, width = 300)
        global search_date_entry
        search_date_entry = Entry(search_date_root, width=15)
        search_date_entry.grid(row =1, column = 1)
        search_date_button = Button(search_date_root, text = "Get", padx = 5, fg = "#488AC7", bg = "white",
            command = lambda: (
                Search_date_main(date_, search_date_entry),
                Start(False, False)
            )
        )
        search_date_button.grid(row =1, column = 2)
        # 
        global frame_table_array
        global frame_table_current
        frame_table_array = []
        frame_table_current = Frame(root, bg = "white", bd = 5)
        global search_button
        search_button = Button(search_root, text = "Search", padx = 5, fg = "#488AC7", bg = "white",
            command = lambda: (
            frame_table_array.append(frame_table_current),
            Search_main(data_server, search_entry, root, frame_table_array, frame_table),
        ))
        search_button.grid(row= 1, column = 2)
    global data_server
    data_server = []
    if day_cur == True:
        user["msg"] = date.today().strftime('%Y-%m-%d')
    else:
        # if current day > input day
        handle_date = Compare_day(date.today().strftime('%Y-%m-%d'), date_["search"])
        if handle_date == True:
            user["msg"] = date_["search"]
        # if current day < input day
        if handle_date == False:
            messagebox.showwarning('Forex Rate', 'Date Fail!')
            return
        if handle_date == -1:
            messagebox.showwarning('Forex Rate', '{} ??? :D ???'.format(date_["search"]))
            return
    client.sendall(json.dumps(user).encode("utf-8"))
    data_server_json = client.recv(40000).decode("utf-8")
    # data_main
    data_server = json.loads(data_server_json)
    # ======= GUI - main =======
    if day_cur == True:
        global frame_table
        frame_table = Frame(root, bg = "white", bd = 5)
        frame_table.place(x = 10, y = 110)
        global table_data
        table_data = Table(frame_table,data_server, len(data_server), len(data_server[0]))
        refresh_button = Button(root, text = "Refresh", padx = 5,pady = 5, fg = "#488AC7", bg = "white",
            command = lambda: (
                frame_table.destroy(),
                # frame_table_current.destroy(),
                Start(False, True)
            )
        )
        refresh_button.place(x = 20, y = 790)
    else:
        root1 = Toplevel()
        root1.geometry("420x750")
        root1.title("Forex Rate")
        frame_logo_root_ = Frame(root1, bg = "white", bd = 5)
        frame_logo_root_.place(x = 0, y = 0, height = 250, width = 400)
        logo_root_ = Label(frame_logo_root_, text = "FOREX RATE", font =("Impact", 50, "bold"), fg = "#D2691E")
        logo_root_.place(x = 10, y = 10)
        text_date_ = Label(frame_logo_root_, text = "{}".format(date_["search"]), font =("Impact", 15, "bold"), fg = "#D2691E")
        text_date_.place(x = 280, y = 20)
        frame_table_ = Frame(root1, bg = "white", bd = 5)
        frame_table_.place(x = 10, y = 110)
        table_data_ = Table(frame_table_,data_server, len(data_server), len(data_server[0]))
    root.bind('<Return>', Enter_search)
    # global search_button
    root.protocol("WM_DELETE_WINDOW", on_closing)
        

def Search_main(data_server, search_entry, root, frame_table_array, frame_table):
    frame_table.place_forget()
    frame_table_array[cnt].place_forget()
    frame_table_current = Frame(root, bg = "white", bd = 5)
    frame_table_array.append(frame_table_current)
    getOne()
    frame_table_array[cnt].place(x = 10, y = 110)
    search_target = search_entry.get()
    if search_target == "":
        frame_table.place(x = 10, y = 110)
        return
    total_rows = []
    total_rows.append(0)
    searched = False
    for i in range(1, len(data_server), 1):
        if (data_server[i][0].find(search_target) != -1):
            total_rows.append(i)
            searched = True

    if (searched == False):
        messagebox.showwarning('Forex Rate', 'Not Found!')
    Table_Current(frame_table_array[cnt], data_server, total_rows, len(data_server[0]))


def Enter_search(event):
    frame_table_array.append(frame_table_current),
    Search_main(data_server, search_entry, root, frame_table_array, frame_table)

window.bind('<Return>', Enter_login)

window.mainloop()

client.close()