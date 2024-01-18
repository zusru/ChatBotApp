import json
from difflib import get_close_matches

def load_KnowledgeBase(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data



def save_KnowledgeBase(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_questions: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_questions, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None
        

def get_answer_for_questions(questions: str, KnowledgeBase: dict) -> str | None:
    for q in KnowledgeBase["questions"]:
        if q["questions"] == questions:
            return q["answer"]
                
    
def ChatBot():
    KnowledgeBase: dict = load_KnowledgeBase('KnowledgeBase.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["questions"] for q in KnowledgeBase["questions"]])

        if  best_match:
            answer: str = get_answer_for_questions(best_match, KnowledgeBase)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                KnowledgeBase["questions"].append({"questions": user_input, "answer": new_answer})
                save_KnowledgeBase('KnowledgeBase.json', KnowledgeBase)
                print('Bot: Thank you! I learned anew response!')



if __name__ == '__main__':
    ChatBot()