import json
import random
from difflib import get_close_matches
from colorama import Fore, init
from datetime import datetime




class Malfy_memories():
    filePath = "Malfy_knowledge.json"
    unknown = "Mình không hiểu! Bạn chỉ mình câu trả lời với!"
    def Save(data: dict):
        with open(Malfy_memories.filePath,'w') as file:
            json.dump(data,file,indent=2)
    def Load() -> dict:
        with open(Malfy_memories.filePath,'r') as file:
            data = json.load(file)
        return data

#Malfy xử lý thông tin từ người dùng đưa ra 
class Malfy_information_processing():
    #tìm câu hỏi gần đúng nhất với câu hỏi của người dùng trong trí nhớ
    def find_best_match_question(user_question: str, questions: list) -> str | None:
        best_match = get_close_matches(user_question,questions,n=1)
        return best_match[0] if best_match else None
    #tìm câu trả lời
    def find_answer(best_match: str, data: dict) -> str:
        for q in data["questions"]:
            if best_match==q["question"]:
                return q["answer"]
            
    #phản hồi lại lời chào từ người dùng
    def response():
        Malfy_response_list: list = data["leave"]["answer"]
        Malfy_response_text = Malfy_response_list[random.randrange(len(Malfy_response_list))]
        conversation_manager.Malfy_response(Malfy_response_text)
    
#Malfy xác định kiểu câu của người dùng đưa ra            
class Malfy_information_identification():
    accurate_default = 0.6
    def identification(user_message: str, data_list: list, accurrate: float | None) -> list:
        check_answer = get_close_matches(user_message,data_list,n=1,cutoff=accurrate)
        return check_answer
    def user_refuse(user_answer: str, data: dict) -> bool:
        return True if len(Malfy_information_identification.identification(user_answer,data["refuses"],Malfy_information_identification.accurate_default))==1 else False

    def user_leave(user_message: str, data: dict) -> str | None:
        return True if len(Malfy_information_identification.identification(user_message,data["leave"]["bye"],Malfy_information_identification.accurate_default))==1 else False
    def user_check_date(user_message: str, data: dict) -> bool:
        return True if len(Malfy_information_identification.identification(user_message,data["watch"]["date"],Malfy_information_identification.accurate_default)) else False
    def user_check_time(user_message: str, data: dict) -> bool:
        return True if len(Malfy_information_identification.identification(user_message,data["watch"]["time"],Malfy_information_identification.accurate_default)) else False

# Đồng hồ của Malfy và các hành động liên quan đến xem ngày giờ
class Malfy_watch():
    def see_date():
        conversation_manager.Malfy_response("Hôm nay là ngày " + datetime.now().strftime("%d/%m/%Y") + " nha!")
    def see_current_time():
        conversation_manager.Malfy_response("Bây giờ là "+str(datetime.now().hour)+" giờ "+str(datetime.now().minute)+" phút nhé!")
    
#class quản lý hộp hội thoại
class conversation_manager:
    def Malfy_response(response: str):
        print(Fore.LIGHTMAGENTA_EX + "Malfy:",end=" ")
        print(Fore.YELLOW + response)
    def user_message():
        print(Fore.LIGHTGREEN_EX + "Bạn:",end=" ")
        return input(Fore.BLUE)

#Main:
data = Malfy_memories.Load()
init(True)
while True:
    message = conversation_manager.user_message().lower()
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
            