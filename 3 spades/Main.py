import json
from difflib import get_close_matches

filePath = "Malfy_knowledge.json"
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

data = Load()

print("Note: Malphy giờ đã có não!")

while True:
    message = input("Bạn: ")
    
    best_match_question = find_best_match_question(message,[q["question"] for q in data["questions"]])
    if best_match_question:
        answer = find_answer(best_match_question,data)
        print("Malfy:",answer)
    else:
        user_answer = input("Malfy: Mình không hiểu bạn đang nói gì cả\nMalfy: Bạn có thể dạy mình câu trả lời được không? Nếu bạn không muốn thì có thể trả lời là 'không' nhé: ")
        if user_answer.lower() != "không":
            data["questions"].append({"question": message, "answer":user_answer})
            Save(data)
            print("Malfy: Cảm ơn bạn nhé :>")
        else:
            print("Tiếc quá nhỉ! Mong là lần tới có thể được bạn chỉ bảo thêm!")

