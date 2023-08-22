from question_generator import QuestionGenerator
from question_viewer import QuestionViewer


class WordLearningPlatform:
    def __init__(self) -> None:
        self.question_generator = QuestionGenerator()
        self.question_viewer = QuestionViewer(None)
    def run(self):
        self.question_generator.generate_question()
        self.question_viewer.set_questions(self.question_generator.get_all_questions())
        self.question_viewer.show_questions()