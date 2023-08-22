import random
from answer import Answer
from db_helper import DbHelper
from question import Question


class QuestionGenerator():
    def __init__(self):
        self.dbHelper = DbHelper("database")
        self.questions = []
    def generate_question(self):
        words_count = self.dbHelper.get_words_count()
        qroup_index = int(input(f"Bazamizda {words_count//10} qrup var.\nOyrenmek istediyiniz soz qrupunu secin: "))
        if qroup_index not in range(words_count//10):
            raise Exception("Invalid group index exception")
        for index in range((qroup_index-1)*10+1, qroup_index*10+1):
          
            word_row =  self.dbHelper.get_word_from_id(index)
            question = Question(word_row[0])
            tru_answer = Answer(question, word_row[1], True)
            question.add_answer(tru_answer)
            like_this_words = [x for x in self.dbHelper.get_words_where_startswith(word_row[0][0]) if x[0]!=word_row[0]]
            for like_this in like_this_words[:(3 if len(like_this_words)>3 else len(like_this_words))]:
                false_answer = Answer(like_this[0],like_this[1], False)
                question.add_answer(false_answer)
            self.questions.append(question)
    def get_all_questions(self):
        return self.questions
    
        
                