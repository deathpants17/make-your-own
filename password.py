from tkinter import *
import os


def delete2():
    screen3.destroy()
def delete3():
    screen4.destroy()
def delete4():
    screen5.destroy()

def deleteMain():
    screen.destroy()






def login_success():
    global screen3
    screen3=Toplevel(screen)
    screen3.title("Login Success!")
    screen3.geometry("300x250")
    Label(screen3,text="Login Success").pack()
    Button(screen3, text="ok").pack()
def password_not_recognized():
    global screen4
    screen4=Toplevel(screen)
    screen4.title("Password failed!")
    screen4.geometry("300x250")
    Label(screen4,text="Password error").pack()
    Button(screen4, text="ok",command=delete3).pack()

def user_not_found():
    global screen5
    screen5=Toplevel(screen)
    screen5.title("User not recognized")
    screen5.geometry("300x250")
    Label(screen5,text="User not reconized").pack()
    Button(screen5, text="ok",command=delete4).pack()


def login_verify():
    username1=username_verify.get()
    password1=password_verify.get()
    username_entry1.delete(0,END)
    password_entry1.delete(0,END)

    list_of_files=os.listdir()
    if username1 in list_of_files:
        file1=open(username1,"r")
        verify=file1.read().splitlines()
        if password1 in verify:
             login_success()
        else:
            password_not_recognized()
    else:
        user_not_found()

def register_user():

    username_info=username.get()
    password_info=password.get()

    file=open(username_info,"w")
    file.write(username_info+"\n")
    file.write(password_info)
    file.close()
    #two entry below to clear the entry when registered
    username_entry.delete(0,END)
    password_entry.delete(0,END)

    Label(screen1, text="Regsiteration successful",fg="yellow",bg="red",font=("Calibri",11)).pack()



def register():

    global screen1
    screen1=Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("300x250")
    #we will need user name and password
    global username
    global password
    global username_entry
    global password_entry
    username=StringVar()
    password=StringVar()
    #Now create the entry
    Label(screen1,text="Please enter details below*").pack()
    Label(screen1,text=" ").pack()
    Label(screen1,text="Username *").pack()
    global username_entry
    global password_entry
    username_entry=Entry(screen1,textvariable=username)
    username_entry.pack()
    Label(screen1,text="Password *").pack()
    password_entry=Entry(screen1,textvariable=password)
    password_entry.pack()



    Label(screen1,text="Password *").pack()
    password_entry=Entry(screen1,textvariable=password)
    Button(screen1,text="Register",width=10,height=1,bg="green",command=register_user).pack()




def login():

    global screen2

    screen2=Toplevel(screen)
    screen2.title("Login")
    screen2.geometry("300x250")
    Label(screen2,text="Please enter details below to login in").pack()
    Label(screen2,text="").pack()
    global username_verify
    global password_verify
    username_verify=StringVar()

    password_verify=StringVar()

    global username_entry1
    global password_entry1




    Label(screen2,text="Username *").pack()
    username_entry1=Entry(screen2,textvariable=username_verify)
    username_entry1.pack()
    Label(screen2,text="Password").pack()
    password_entry1=Entry(screen2,textvariable=password_verify)
    password_entry1.pack()
    Label(screen2,text="").pack()
    Button(screen2,text="Login",width=10,height=1,command=login_verify).pack()



def main_screen():
    global screen
    screen=Tk()
    screen.geometry("300x250");
    screen.title("Helion");
    Label(text="Helion",bg="grey",width="300",height="2",font=("Calibri",13)).pack()
    Label(text="").pack()
    Button(text="Login",bg="yellow",height="2",width="30",command=login).pack()
    Label(text="").pack()
    Button(text="Register",bg="red",height="2",width="30",command=register).pack()
    screen.mainloop()
main_screen()