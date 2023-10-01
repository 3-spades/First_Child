import json
from difflib import get_close_matches
filePath = "Malfy_knowledge.json"
def Save(Path: str, data: dict):
    with open(Path,'w') as file:
        json.dump(data, file, indent=2)
def Load(Path: str) -> dict:
    with open(Path,'r') as file:
        data: dict = json.load(file)
    return data

def find(user_input: str, questions: list[str]) -> str | None:
    best_match: list = get_close_matches(user_input,questions,n=1, cutoff=0.6)
    
    if best_match:
        return best_match[0]
    else:
        None

def get_answer(question: str, knowledge: dict) -> str:
    for q in knowledge["questions"]:
        if q["question"] == question:
            return q["answer"]
        
knowledge = Load(filePath)

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit": break
    best_match: str | None = find(user_input,[q["question"] for q in knowledge["questions"]])
    if best_match:
        answer = get_answer(best_match,knowledge)
        print("Malfy: ", answer)
    else:
        print("Malfy: Get a answer:")
        new_answer = input("You: ")
        knowledge["questions"].append({"question": user_input, "answer": new_answer})
        Save(filePath,knowledge)
        print("Thanks!")

