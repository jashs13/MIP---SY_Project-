from tkinter import *
from tkinter.messagebox import *
import psycopg2
from memory import *  

 

def adjustWindow(window):
    w = 600 
    h = 600 
    ws = screen.winfo_screenwidth() 
    hs = screen.winfo_screenheight() 
    x = (ws/2) - (w/2) 
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y)) 
    window.resizable(True, True) 

def update_user_in_db():
    connection = None
    try:
        connection = psycopg2.connect(user = "postgres",
        password = "1314", host = "127.0.0.1", port = "5432", 
        database = "Mini Project")
        print("Connected to PostgreSQL.")
        cursor = connection.cursor()
        sql = "insert into Gamifyit_users(username,password) values('%s','%s')"
        user_name = nEntry.get()
        password = pwEntry.get()
        args = (user_name, password)
        cursor.execute(sql % args)
        connection.commit()    
        print("The query is executed and 1 new row inserted.")
        showinfo("Congrats!", "You have registered successfully. Now login again to enjoy!")
    except (Exception, psycopg2.DatabaseError) as e:
        connection.rollback()
        print("issue  ", e)	
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

def password_check(password):
	x = password
	if  (len(x)>8) and (len(x)<15) and any(
	char.isdigit() for char in x) and any(
	char.isalpha() for char in x) and any(
	char.isalnum() for char in x) and any(
	char.isupper() for char in x) and any(
	char.islower() for char in x):
		return True
	else:
		return False

# Validating for each input 
def validate(event, input):
    if (input == "Name"):
        if all(x.isalpha() or x.isspace() for x in name.get()) and (len(name.get()) > 1): 
            pwEntry.focus_set() 
            pwEntry.config(state='normal') 
        else: 
            showwarning("Invalidate!" ,"Name cannot contain digits or special characters. Spaces are allowed and length should be greater than 1.") 
            nEntry.focus_set()  
    elif (input == "Password"):
        password = pw.get()
        if password_check(password):
            showinfo("Validated!", "The user can click on save to complete the registeration process")
        else:
            showwarning("Invalid!", "The pw length should be 8-15. It should have atleast a digit, an alphabet, a lowercase letter, an uppercase letter and a special character.")    


def f2():
    gaop.withdraw()
    screen.deiconify()

def callMemory():
    if __name__ == '__main__':
        main()

def callDino():
    from Dino_runGame import main
    


def game_option():
    global gaop
    gaop = Toplevel(screen)
    adjustWindow(gaop)
    screen.withdraw()
    gaop.title("Games")
    
    frame = Frame(gaop, bg='#80c1ff', bd=5)
    frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    # 2 Game option buttons
    btnmemory = Button(frame, bg='#174873', font=30, bd=10, text="Memory Game", fg='white',command=callMemory)
    btnmemory.place(relx=0.25, rely=0.1, relwidth=0.45, relheight=0.2)

    btnDino = Button(frame, bg='#174873', font=30, bd=10, text="Dino - Run Game", fg='white',command=callDino)
    btnDino.place(relx=0.25, rely=0.4, relwidth=0.45, relheight=0.2)

    # Lower Frame
    lower_frame = Frame(gaop, bg='#00bfff', bd=5)
    lower_frame.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)
    
    btnback = Button(lower_frame, text='Back', font='20', bd=5, command=f2)
    btnback.place(relx=0.33, rely=0.18, relwidth=0.35, relheight=0.5)

    gaop.mainloop()


def f1():
    regusr.withdraw()
    screen.deiconify()

def register_user():
    global regusr, name, pw
    global nEntry, pwEntry
    regusr = Toplevel(screen)
    adjustWindow(regusr)
    screen.withdraw()
    regusr.title("Add User")
    
    frame = Frame(regusr, bg='#80c1ff', bd=5)
    frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    # Labels
    lblentname = Label(frame, text='Enter Name', font=20)
    lblentname.place(relx=0.35, rely=0.01, relwidth=0.3, relheight=0.1)

    lblentpw = Label(frame, text='Enter Password', font=20)
    lblentpw.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.1)

    # Entry
    name = StringVar()
    pw = StringVar()  

    nEntry = Entry(frame, font=20, textvariable=name)
    nEntry.place(relx=0.15, rely=0.14, relwidth=0.7, relheight=0.08)
    nEntry.bind("<Return>", lambda event: validate(event, "Name")) 
    nEntry.bind("<Tab>", lambda event: validate(event, "Name")) 

    pwEntry = Entry(frame, font=20, textvariable=pw)
    pwEntry.place(relx=0.15, rely=0.37, relwidth=0.7, relheight=0.08)
    pwEntry.bind("<Return>", lambda event: validate(event, "Password")) 
    pwEntry.bind("<Tab>", lambda event: validate(event, "Password")) 
 
    # First is enabled rest 2 inputs will be disabled for checking validation 
    pwEntry.config(state='disabled')
    
    # Lower Frame
    lower_frame = Frame(regusr, bg='#00bfff', bd=5)
    lower_frame.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)
    
    btnback = Button(lower_frame, text='Back', font='20', bd=5, command=f1)
    btnback.place(relx=0.12, rely=0.15, relwidth=0.2, relheight=0.5)

    btnsave = Button(lower_frame, text='Save', font='20', bd=5, command=update_user_in_db)
    btnsave.place(relx=0.65, rely=0.15, relwidth=0.2, relheight=0.5)

    regusr.mainloop()



def login_verify():
    connection = None
    try:
        connection = psycopg2.connect(user = "postgres",
        password = "1314", host = "127.0.0.1", port = "5432", 
        database = "Mini Project")
        print("Connected to PostgreSQL.")
        cursor = connection.cursor()
        sql = "select * from Gamifyit_users"
        cursor.execute(sql)
        data = cursor.fetchall()  # list of tuples of row
        # [('username','pw'),('','')]
        connection.commit()
        good = 0
        for d in data:
            if ((username_verify.get() == d[0]) and (password_verify.get() == d[1])):
                print("The username and password matches.")
                print("Therefore, the row exists.") 	
                showinfo("Welcome!","Login successful...") 
                btnlogin.configure(state=NORMAL)
                good = good + 1
                break
        if (good == 0):
                print("Username and pw not found")
                showerror("Error!","User not found. Please register!")
                 		     
        print("The query is executed and the credentials are checked.")
        
    except (Exception, psycopg2.DatabaseError) as e:
        connection.rollback()
        print("issue  ", e)	
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")


# login window
def main_screen():
    global screen, username_verify, password_verify, btnlogin
    screen = Tk() # initializing the tkinter window
    username_verify = StringVar()
    password_verify = StringVar()
    screen.title("LOGIN TO PLAY") # mentioning title of the window
    adjustWindow(screen) # configuring the window
    Label(screen, text="GamifyIt", width="500", height="2", font=("Calibri", 22, 'bold'), fg='white', bg='#d9660a').pack()
    Label(text="", bg='white').pack() # for leaving a space in between
    Label(screen, text="", bg='#174873',width='73', height='27').place(x=45, y=120) # blue background in middle of window
    Label(screen, text="Please enter details below to login", bg='#174873', fg='white').pack()
    Label(screen, text="", bg='#174873').pack() # for leaving a space in between
    Label(screen, text="Username * ", font=("Open Sans", 10, 'bold'), bg='#174873', fg='white').pack()
    Entry(screen, textvar=username_verify).pack()
    Label(screen, text="", bg='#174873').pack() # for leaving a space in between
    Label(screen, text="Password * ", font=("Open Sans", 10, 'bold'), bg='#174873', fg='white').pack()
    
    loginpw_ent = Entry(screen, textvar=password_verify, show="*")
    loginpw_ent.pack()
    loginpw_ent.bind("<Return>", lambda event: login_verify()) 
    
    
    Label(screen, text="", bg='#174873').pack() # for leaving a space in between
    
    btnlogin = Button(screen, text="LOGIN", bg="#e79700", width=15, height=1, font=("Open Sans", 13, 'bold'), fg='white', command=game_option)
    btnlogin.config(state = DISABLED)
    btnlogin.pack()

    Label(screen, text="", bg='#174873').pack() # for leaving a space in between
    Button(screen, text="New User? Register Here", height="2", width="30", bg='#e79700', font=("Open Sans", 10, 'bold'), fg='white', command=register_user).pack()
    screen.mainloop()

main_screen()      