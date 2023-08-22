import sys

class QuestionViewer():
    def __init__(self, questions):
        self.questions = questions
        self.answers = []
        
    def set_questions(self, questions):
        self.questions=questions
        
    def show_questions(self):
        self.answers.clear()
        for question in self.questions:
            selected_variant = int(input(f"{question}\n\nBir variant secin: "))
            user_answer = question.answers[selected_variant-1].getIsTrue()
            if user_answer:
                self.answers.append(user_answer)
            else:
                original_true_answer = None
                for a in question.answers:
                    if a.getIsTrue():
                        original_true_answer = a
                
                explanation = {
                    "original_true_answer": original_true_answer,
                    "user_answer": question.answers[selected_variant-1]
                }
                self.answers.append(explanation)
        for n, v in enumerate(self.answers, 1):
            print(f"{n}\t{v if isinstance(v, bool) else False}")
        
        print(f"sizin dogru cavablarinizin sayi: {len([x for x in self.answers if isinstance(x, bool)])}")
        f = open("oyrenilesi.txt","w")
        f, sys.stdout = sys.stdout, f
        for a in self.answers:
            
            if not isinstance(a, bool):
                print(f"{a['original_true_answer'].getOriginalQuestion()} sozu ucun {str(a['original_true_answer'])} secmeli idiniz\n\n")
                print(f"{a['user_answer'].getOriginalQuestion()} --> {str(a['user_answer'])} demekdir\n\n")
        f, sys.stdout = sys.stdout, f
        f.close()

        