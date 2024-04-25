import json
from difflib import get_close_matches

def  load_bot_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_bot_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, bot_knowledge_base: dict) -> str | None:
    for q in bot_knowledge_base["questions"]:
        if q ["question"] == question:
            return q ["answer"]
        
def chat_bot():
    bot_knowledge_base: dict = load_bot_knowledge_base('bot_knowledge_base.json')

    while True:
        user_input: str = input('Users: ')

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in bot_knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, bot_knowledge_base)
            print(f'Robot: {answer}')
        else:
            print('Robot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                bot_knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_bot_knowledge_base('bot_knowledge_base.json', bot_knowledge_base)
                print('Robot: Thank you! I learned a new words!')

if __name__ == '__main__':
    chat_bot()