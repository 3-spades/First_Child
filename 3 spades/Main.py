import json
import random
from difflib import get_close_matches
from colorama import Fore, init

filePath = "Malfy_knowledge.json"
unknown = "Mình không hiểu! Bạn chỉ mình câu trả lời với!"

def Save(data: dict):
    with open(filePath,'w') as file:
        json.dump(data,file,indent=2)

def Load() -> dict:
    with open(filePath,'r') as file:
        data = json.load(file)
    return data

def find_best_match_question(user_question: str, questions: list) -> str | None:
    best_match = get_close_matches(user_question,questions,n=1)
    return best_match[0] if best_match else None

def find_answer(best_match: str, data: dict) -> str:
    for q in data["questions"]:
        if best_match==q["question"]:
            return q["answer"]
        
def user_refuse(user_answer: str, data: dict) -> bool:
    check_answer = get_close_matches(user_answer,data["confuses"],n=1)
    return True if len(check_answer)==1 else False

def user_leave(user_message: str, data: dict) -> str | None:
    check_message = get_close_matches(user_message,data["leave"]["bye"],n=1)
    return True if len(check_message)==1 else False

class conversion_manager:
    def Malfy_response(response: str):
        print(Fore.LIGHTMAGENTA_EX + "Malfy:",end=" ")
        print(Fore.YELLOW + response)
    def Get_user_message():
        print(Fore.LIGHTGREEN_EX + "Bạn:",end=" ")
        return input(Fore.BLUE)
    

#Main:
data = Load()
init(True)
while True:
    message = conversion_manager.Get_user_message()
    if user_leave(message.lower(),data):
        
        Malfy_response_list: list = data["leave"]["answer"]
        Malfy_response_text = Malfy_response_list[random.randrange(len(Malfy_response_list))]
        conversion_manager.Malfy_response(Malfy_response_text)
        break

    best_match_question = find_best_match_question(message,[q["question"] for q in data["questions"]])
    
    if best_match_question:
        answer = find_answer(best_match_question,data)
        conversion_manager.Malfy_response(answer)
    else:
        conversion_manager.Malfy_response(unknown)
        user_answer = conversion_manager.Get_user_message()
        if user_refuse(user_answer,data):
            conversion_manager.Malfy_response("Tiếc quá nhỉ! Mong là lần tới có thể được bạn chỉ bảo thêm!")
        else:
            data["questions"].append({"question": message, "answer":user_answer})
            Save(data)
            conversion_manager.Malfy_response("Cảm ơn bạn nhé <3")
            