import datetime
import sqlite3


class DbHelper:
    def __init__(self, db_name):
        self.db_name=db_name
        self.words_table = "words_table"
        self.learning_time_table = "learning_time_table"
        self.answer_table = "answer_table"
        self.db=sqlite3.connect(f"{db_name}.db")
        # create table
        sql_words = f"""CREATE TABLE IF NOT EXISTS {self.words_table} (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE ,
                        Word TEXT NOT NULL,
                        Meaning TEXT NOT NULL
                    )"""
        sql_learning_time = f"""CREATE TABLE IF NOT EXISTS {self.learning_time_table} (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE ,
                        WordID INTEGER,
                        LearningTime  int NOT NULL,
                        FOREIGN KEY (WordID) REFERENCES {self.words_table}(ID)
                    );"""
        user_answers = f"""CREATE TABLE IF NOT EXISTS {self.answer_table} (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE ,
                        QuestionCount  INTEGER NOT NULL DEFAULT 0,
                        TrueAnswerCount  INTEGER NOT NULL DEFAULT 0,
                        WordID INTEGER,
                        FOREIGN KEY (WordID) REFERENCES {self.words_table}(ID)
                    );"""
        cursor = self.db.cursor()
        cursor.execute(sql_words)
        self.db.commit()
        cursor.execute(sql_learning_time)
        self.db.commit()
        cursor.execute(user_answers)
        self.db.commit()
        
    def add_word(self, word, meaning):
        sql_stm = f"""INSERT INTO {self.words_table} (Word, Meaning) Values (?, ?)"""
        cursor = self.db.cursor()
        cursor.execute(sql_stm, (word, meaning))
        self.db.commit()
        
        
    def add_learning_time(self, word_id:int)->bool:
        
        sql_stm = f"""INSERT INTO {self.learning_time_table} (WordID, LearningTime) values (?, ?)"""
        cursor = self.db.cursor()
        cursor.execute(f"""SELECT COUNT(word) FROM {self.words_table} WHERE ID={word_id}""")
        count = cursor.fetchall()[0][0]
        if not count:
            return False
        cursor.execute(sql_stm,(word_id,int(datetime.datetime.now().timestamp())))
        self.db.commit()
        return True
        
    def add_answer(self, word_id:int)->bool:
        sql_stm = f"""INSERT INTO {self.answer_table} (WordID) values (?)"""
        cursor = self.db.cursor()
        cursor.execute(f"""SELECT COUNT(word) FROM {self.words_table} WHERE ID={word_id}""")
        count = cursor.fetchall()[0][0]
        if not count:
            return False
        cursor.execute(sql_stm,[word_id])
        self.db.commit()
        return True
    
    def get_words_count(self):
        """Returns the number of words in database."""
        sql_stm = "select Count(*) from {}".format(self.words_table)
        cursor = self.db.cursor()
        cursor.execute(sql_stm)
        data = cursor.fetchone()
        return data[0]
    
    def get_word_from_id(self, id:int):
        # TODO: check for correctness and raise exception when wrong input is given!
        sql_stm=  'Select Word, Meaning From {} Where Id=?'.format(self.words_table)
        cursor = self.db.cursor()
        cursor.execute(sql_stm , [id])
        row = cursor.fetchone()
        return row
        
    def get_meaning_from_word(self, word):
        sql_stm = f"""Select Word, Meaning From {self.words_table} Where Word = ?"""
        cursor = self.db.cursor()
        cursor.execute(sql_stm, (word, ))
        return cursor.fetchone()
    
    def get_word_from_meaning(self, meaning):
        sql_stm = f"""Select Word, Meaning From {self.words_table} Where Meaning = ?"""
        cursor = self.db.cursor()
        cursor.execute(sql_stm, (meaning, ))
        return cursor.fetchone()
        
    def get_words_where_startswith(self, word_part):
        sql_stm = f"""Select Word, Meaning From {self.words_table} Where Word Like ?"""
        cursor = self.db.cursor()
        cursor.execute(sql_stm, (word_part+"%", ))
        return cursor.fetchall()
    
    def get_word_learning_time(self, word):
        sql_stm = f"""SELECT l.LearningTime From {self.learning_time_table} l JOIN {self.words_table} w ON l.WordID = w.ID WHERE  w.ID = (SELECT ID FROM {self.words_table} WHERE Word = ? LIMIT 1) """
        cursor = self.db.cursor()
        cursor.execute(sql_stm, (word,))
        return cursor.fetchone()
        
    def get_user_answer(self, word):
        sql_stm = f"""SELECT u.QuestionCount, u.TrueAnswerCount From {self.answer_table} u JOIN {self.words_table} w ON u.WordID = w.ID WHERE  w.ID = (SELECT ID FROM {self.words_table} WHERE Word = ? LIMIT 1) """
        cursor = self.db.cursor()
        cursor.execute(sql_stm, (word,))
        return cursor.fetchone()
        
    
    def update_user_answer(self, word, true_answer = True):
        sql_stm1 = f"""SELECT ID from {self.words_table} WHERE Word = ?"""
        cursor = self.db.cursor()
        cursor.execute(sql_stm1, (word,))
        result = cursor.fetchone()
        self.db.commit()
        if not result:
            print("No such word")
            return False
        w_id=result[0]
        sql_stm2 = f"""SELECT COUNT(ID) FROM {self.add_answer} WHERE WordID = ?"""
        cursor.execute(sql_stm2, w_id)
        answerCount = int((cursor.fetchall())[0][0])
        self.db.commit()
        if not answerCount:
            self.add_answer(word_id=w_id)
        if true_answer:
            sql_stm3 = f"""UPDATE {self.answer_table} SET QuestionCount=QuestionCount+1 where WordID={w_id}"""
        else:
            sql_stm3 = f"""UPDATE {self.answer_table} SET QuestionCount=QuestionCount+1, TrueAnswerCount=TrueAnswerCount+1 where WordID={w_id}"""
        cursor.execute(sql_stm3)
        self.db.commit()