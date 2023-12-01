from customtkinter import *
import tkinter as tk
from PIL import Image
import Core


#Define Mode
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

"""Core"""
#Create main Window
root = CTk()
root.title("Chatbot Malfy")

#Create Frame
startFrame = CTkFrame(root)
mainFrame = CTkFrame(root)
settingFrame = CTkFrame(mainFrame)
chatFrame = CTkFrame(mainFrame)

#Create global variables
message = ""
switch_var = StringVar(value="on")

class Message:
    def __init__(self, message_frame: CTkFrame, title_frame: CTkFrame, text_name: CTkLabel, text_message: CTkLabel) -> None:
        self.message_frame = message_frame
        self.title_frame = title_frame
        self.text_name = text_name
        self.text_message = text_message
        

class Static:
    user_name = ""
    size_of_text = 15
    font = "Courier"
    dark_color = "gray20"
    light_color = "white"
    recent_color = "gray20"

    def __init__(self, name, size_of_text, font) -> None:
        self.name=name
        self.size_of_text=size_of_text
        self.font = font
        
malfy_responses = []
user_messages = []

"""Funtions"""
#Set_appearance_mode
def modifierColorMessage(color):
    positive_color = ""
    if color==Static.dark_color: positive_color=Static.light_color
    else : positive_color=Static.dark_color
    for index in range(0,len(malfy_responses)):
        malfy_response = malfy_responses[index]
        user_message = user_messages[index]

        malfy_response.message_frame.configure(fg_color=color, bg_color=color)
        malfy_response.title_frame.configure(fg_color=positive_color, bg_color="transparent", corner_radius=10)
        malfy_response.text_name.configure(text_color=color)
        malfy_response.text_message.configure(text_color=color)

        user_message.message_frame.configure(fg_color=color, bg_color=color)
        user_message.title_frame.configure(fg_color=positive_color, bg_color="transparent", corner_radius=10)
        user_message.text_name.configure(text_color=color)
        user_message.text_message.configure(text_color=color)

def setApperanceMode():
    if switch_var.get()=="on":
        set_appearance_mode("dark")
        modifierColorMessage(Static.dark_color)
        textbox.configure(bg=Static.dark_color)
        Static.recent_color = Static.dark_color
    elif switch_var.get()=="off":
        set_appearance_mode("light")
        modifierColorMessage(Static.light_color)
        textbox.configure(bg=Static.light_color)
        Static.recent_color = Static.light_color

#Get user's name from user name field
def getUserName(event):
    #Get username
    Static.user_name = userNameInput.get()
    startFrame.grid_forget()
    mainFrame.grid(row=0, column=0, sticky="nsew")
    
#Message Manager
def create_messagebox(side, message):
    image_path = ""
    name = ""
    icon_column_side = 0
    title_column_side = 0
    if side=="left":
        name="Malfy"
        image_path = "8943377.png"
        icon_column_side = 0
        title_column_side = 1
    else:
        image_path = "9131529.png"
        name=Static.user_name
        icon_column_side = 1
        title_column_side = 0

    #Create frame to contain icon and message
    message_frame = CTkFrame(master=textbox, fg_color=Static.recent_color, bg_color=Static.recent_color)

    icon_image = CTkImage(light_image=Image.open(image_path))
    icon = CTkLabel(master=message_frame, text="", image=icon_image, width=10, height=10)
    icon.grid(row=0, column=icon_column_side, sticky="w")

    void_label = CTkLabel(master=message_frame, text="")
    void_label.grid(row=1, column=icon_column_side, sticky="w")

    
    title_frame = CTkFrame(master=message_frame, bg_color="transparent", corner_radius=10)
    if Static.recent_color==Static.dark_color: title_frame.configure(fg_color=Static.light_color)
    else: title_frame.configure(fg_color=Static.dark_color)
    title_frame.grid(row=0, column=title_column_side, rowspan=2, padx=5, pady=5, sticky="nsew")
    title_frame.grid_columnconfigure(0,weight=1)
    title_frame.grid_rowconfigure(0, weight=1)

    text_name = CTkLabel(master=title_frame, text=name, text_color=Static.recent_color)
    text_name.grid(row=0, column=0, padx=3, pady=3)
    if side=="left": text_name.grid_configure(sticky="w")
    else: text_name.grid_configure(sticky="e")

    #Create Message text to contain message
    text_message = CTkLabel(master=title_frame, text=message, text_color=Static.recent_color, justify="left", font=(Static.font, Static.size_of_text))
    text_message.grid(row=1, column=0, padx=8, pady=2, sticky="w")

    message = Message(message_frame,title_frame,text_name,text_message)
    if side=="left":
        malfy_responses.append(message)
    else:
        user_messages.append(message)

    #Add Messagebox to textbox
    textbox.insert("end", "\n ", side)
    textbox.window_create("end", window=message_frame)

def sendMessage(event, side, message):
    textbox.configure(state="normal")
    messageInput.delete(0,tk.END)
    create_messagebox(side, message)
    textbox.configure(state="disabled")
    
def conversation(event, message):
    sendMessage(event,"right",message)
    if Core.getResponse(message.lower())!="unknown":
        sendMessage(event,"left",Core.getResponse(message.lower()))
    else:
        sendMessage(event,"left", "Mình chưa có đủ kiến thức để phản hồi bạn!\nBạn có thể chỉ cho mình cách phản hồi chứ?")
        unknownInput.grid(row=1, column=0, sticky="nsew")
        messageInput.grid_forget()
        unknownInput.bind("<Return>", lambda event: unknownMessage(event, message, unknownInput.get()))
        
def unknownMessage(event, question, answer):
    unknownInput.delete(0,END)
    if Core.Malfy_information_identification.user_refuse(answer, Core.data):
        sendMessage(event, "left", "Tiếc quả nhỉ!")
    else:
        Core.data["questions"].append({"question": question, "answer":answer})
        Core.Malfy_memories.Save(Core.data)
        sendMessage(event,"left", "Cảm ơn ban nhiều nha!")
    messageInput.grid(row=1, column=0, sticky="nsew")
    unknownInput.grid_forget()

def changeSizeText(value):
    Static.size_of_text = int(value)
    for index in range(0,len(malfy_responses)):
        malfy_responses[index].configure(font=(Static.font,Static.size_of_text))
        if len(user_messages)>index: user_messages[index].configure(font=(Static.font,Static.size_of_text))
    recent_size.configure(text=f"Size: {Static.size_of_text}")

"""Setup Frame:"""
#Start Frame
startingLabel = CTkLabel(master=startFrame,text="Malfy: Mình có thể gọi bạn là gì?")
startingLabel.grid(sticky="nsew")
startingLabel.columnconfigure(0,weight=1)

userNameInput = CTkEntry(master=startFrame)
userNameInput.grid(sticky="nsew")
startingLabel.columnconfigure(0,weight=1)

"<Main Frame>"
#Setup Setting:

#Change messagebox color
color_message_frame = CTkFrame(master=settingFrame, width=200, height=100, corner_radius=10, border_color=Static.dark_color, border_width=2)
color_message_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

color_message_label = CTkLabel(color_message_frame, text="Malfy's message color")
color_message_label.grid(row=0, column=0, padx=5, pady=5,sticky="w")

malfy_response_color_options = CTkOptionMenu(color_message_frame)
malfy_response_color_options.grid(row=0, column=1, padx=5, pady=5, sticky="e")

color_message_label = CTkLabel(color_message_frame, text="User's message color")
color_message_label.grid(row=1, column=0, padx=5, pady=5,sticky="w")

malfy_response_color_options = CTkOptionMenu(color_message_frame)
malfy_response_color_options.grid(row=1, column=1, padx=5, pady=5, sticky="e")

#Change size text slider
size_text_frame = CTkFrame(master=settingFrame,corner_radius=10, border_color=Static.dark_color, border_width=2)
size_text_frame.grid(row=1, column=0, sticky="nsew")
size_text_frame.grid_columnconfigure(0,weight=1)
size_text_frame.grid_rowconfigure(0,weight=1)

size_text_label = CTkLabel(master=size_text_frame, text="Change size text")
size_text_label.grid(columnspan=2, padx=5, pady=5, sticky="nsew")

size_text=CTkSlider(master=size_text_frame, from_=8, to=20, command=changeSizeText)
size_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

recent_size = CTkLabel(master=size_text_frame, text=f"Size: {Static.size_of_text}")
recent_size.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

#Dark mode switch
dark_mode_frame = CTkFrame(master=settingFrame, corner_radius=10, border_color=Static.dark_color, border_width=2)
dark_mode_frame.grid(row=2, column=0, padx=10, pady=5, sticky="w")
dark_mode_frame.grid_columnconfigure(0,weight=1)
dark_mode_frame.grid_rowconfigure(0,weight=1)

darkModeSwitch = CTkSwitch(master=dark_mode_frame,text="Dark mode", variable=switch_var, onvalue="on", offvalue="off", command=setApperanceMode,)
darkModeSwitch.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")


#Setup Chat Frame
textbox = tk.Text(master=chatFrame, bg=Static.dark_color, fg="white", borderwidth=0, state="disabled")
textbox.tag_configure("left", justify="left")
textbox.tag_configure("right", justify="right")
textbox.grid(row=0, column=0, sticky="nsew")

chatbox_scrollbar = CTkScrollbar(master=chatFrame, command=textbox.yview)
chatbox_scrollbar.grid(row=0,column=1,sticky="ns")

messageInput = CTkEntry(master=chatFrame, placeholder_text="Mình có thể giúp gì cho bạn nhỉ?")
messageInput.grid(row=1, column=0, sticky="nsew")

unknownInput = CTkEntry(master=chatFrame, placeholder_text="Nhập câu trả lời cho Malfy hoặc nhập 'Không' để từ chối trả lời...")
unknownInput.grid_forget()

#Connect textbox and chatbox together
textbox.configure(yscrollcommand=chatbox_scrollbar.set)


"""Display"""
#Configure Window
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=1)

#Display and configure Start Frame
startFrame.grid(sticky="nsew", padx=20, pady=20)
startFrame.grid_columnconfigure(0,weight=1)
startFrame.grid_rowconfigure(0,weight=1)
userNameInput.bind("<Return>", getUserName)

#Display and configure Main Frame
mainFrame.grid_columnconfigure(0, weight=1)
mainFrame.grid_columnconfigure(1, weight=4)

mainFrame.grid_rowconfigure(0, weight=1)

settingFrame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
settingFrame.grid_columnconfigure(0,weight=1)
settingFrame.grid_rowconfigure(0, weight=1)

chatFrame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
chatFrame.grid_columnconfigure(0,weight=1)
chatFrame.grid_rowconfigure(0,weight=1)

messageInput.bind("<Return>", lambda event:conversation(event, messageInput.get()))

"""
dark_mode_frame.grid_forget()
color_message_frame.grid_forget()
"""
#Run root
#root.bind("<Configure>", keepScreen)
root.mainloop()
