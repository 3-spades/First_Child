import json
import random
from difflib import get_close_matches
from datetime import datetime


response = ""

class Malfy_memories():
    filePath = "Malfy_knowledge.json"
    unknown = "unknown"
    def Save(data: dict):
        with open(Malfy_memories.filePath,'w') as file:
            json.dump(data,file,indent=2)
    def Load() -> dict:
        with open(Malfy_memories.filePath,'r') as file:
            data = json.load(file)
        return data

#Malfy xử lý thông tin từ người dùng đưa ra 
class Malfy_information_processing():
    #Find the best match question in Malfy_knowledge.json
    def find_best_match_question(user_question: str, questions: list) -> str | None:
        best_match = get_close_matches(user_question,questions,n=1)
        return best_match[0] if best_match else None
    
    #tìm câu trả lời
    def find_answer(best_match: str, data: dict) -> str:
        for q in data["questions"]:
            if best_match==q["question"]:
                return q["answer"]
            
    #Response for user's leaving
    def response():
        Malfy_response_list: list = data["leave"]["answer"]
        Malfy_response_text = Malfy_response_list[random.randrange(len(Malfy_response_list))]
        response = Malfy_response_text
        return response
    
#Malfy xác định kiểu câu của người dùng đưa ra            
class Malfy_information_identification():
    accurate_default = 0.6
    #Identify the Response for the User's Message
    def identification(user_message: str, data_list: list, accurrate: float | None) -> list:
        check_answer = get_close_matches(user_message,data_list,n=1,cutoff=accurrate)
        return check_answer
    def user_refuse(user_answer: str, data: dict) -> bool:
        return True if len(Malfy_information_identification.identification(user_answer,data["refuses"],Malfy_information_identification.accurate_default))==1 else False
    def user_leave(user_message: str, data: dict) -> str | None:
        return True if len(Malfy_information_identification.identification(user_message,data["leave"]["bye"],Malfy_information_identification.accurate_default))==1 else False
   
    #If user check date and time
    def user_check_date(user_message: str, data: dict) -> bool:
        return True if len(Malfy_information_identification.identification(user_message,data["watch"]["date"],Malfy_information_identification.accurate_default)) else False
    
    def user_check_time(user_message: str, data: dict) -> bool:
        return True if len(Malfy_information_identification.identification(user_message,data["watch"]["time"],Malfy_information_identification.accurate_default)) else False


class Malfy_watch():
    def see_date():
        response = "Hôm nay là ngày " + datetime.now().strftime("%d/%m/%Y") + " nha!"
        return response
    def see_current_time():
        response = "Bây giờ là "+str(datetime.now().hour)+" giờ "+str(datetime.now().minute)+" phút nhé!"
        return response
        

#Main:
data = Malfy_memories.Load()

def getResponse(message):
    if Malfy_information_identification.user_leave(message,data):
        return Malfy_information_processing.response()
    
    if Malfy_information_identification.user_check_time(message,data):
        return Malfy_watch.see_current_time()
    
    if Malfy_information_identification.user_check_date(message,data):
        return Malfy_watch.see_date()
    
    best_match_question = Malfy_information_processing.find_best_match_question(message,[q["question"] for q in data["questions"]])
    if best_match_question:
        answer = Malfy_information_processing.find_answer(best_match_question,data)
        return answer
    else:
        return Malfy_memories.unknown


"""
while True:
    message = UI.message.lower()
    
    if Malfy_information_identification.user_leave(message,data):
        Malfy_information_processing.response()
        break
    if Malfy_information_identification.user_check_time(message,data):
        Malfy_watch.see_current_time()
        continue
    if Malfy_information_identification.user_check_date(message,data):
        Malfy_watch.see_date()
        continue
    best_match_question = Malfy_information_processing.find_best_match_question(message,[q["question"] for q in data["questions"]])
    
    if best_match_question:
        answer = Malfy_information_processing.find_answer(best_match_question,data)
        conversation_manager.Malfy_response(answer)
    else:
        conversation_manager.Malfy_response(Malfy_memories.unknown)
        user_answer = conversation_manager.user_message()
        if Malfy_information_identification.user_refuse(user_answer,data):
            conversation_manager.Malfy_response("Tiếc quá nhỉ! Mong là lần tới có thể được bạn chỉ bảo thêm!")
        else:
            data["questions"].append({"question": message, "answer":user_answer})
            Malfy_memories.Save(data)
            conversation_manager.Malfy_response("Cảm ơn bạn nhé <3")
"""