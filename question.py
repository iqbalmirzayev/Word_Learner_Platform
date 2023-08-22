from answer import Answer
import random


class Question():
    def __init__(self, question_text):
        self.question = question_text
        self.answers = []
            
    def add_answer(self, answer:Answer):
        self.answers.append(answer)
        random.shuffle(self.answers)
        
        
        
    def __str__(self):
        return f"{self.question} \n\n\t"+("\n\t".join([f"{n}).\t{a}" for n,a in enumerate(self.answers, 1)]))