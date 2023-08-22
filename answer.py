class Answer():
    def __init__(self, original_question, text, is_true):
        self.__text = text
        self.__is_true = is_true
        self.__original_question = original_question
        
    def getIsTrue(self):
        return self.__is_true
    
    def getOriginalQuestion(self):
        return self.__original_question
    
    def __str__(self) -> str:
        return self.__text
        