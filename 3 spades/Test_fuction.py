from customtkinter import *

root = CTk()
class Static:
    name = ""

def A(event):
    Static.name = a.get()
    a.delete(0,END)
    
def C(event, message):
    print(message, Static.name)

def B():
    a.bind("<Return>", lambda event: C(event, a.get()))

a = CTkEntry(root)
a.pack()

a.bind("<Return>", A)

B()



root.mainloop()