import time
import random

from script import dialog

class rdanymvp:
    def __init__(self):
        self.pause = False
        self.previous_level = "root"
        self.current_level = "root"
        self.user_input = None
        self.dialog = dialog
        self.answers = []
        self.questions = []

    def get_mars_time(self):
        millis = time.time()
        JDut = (millis / (8.64 * 1.e4)) + 2440587.5
        JDtt = JDut + (37 + 32.184) / 86400
        J2000 = JDtt - 2451545
        MSD = (((J2000 - 4.5) / 1.027491252) + 44796 - 0.00096)
        return MSD


    def process(self, current_level):
        answers = []
        questions = []
        letters = "a b c d e f g h i j k l m".split(" ")

        nq = 0
        for item in self.dialog[current_level]:
            if item[0] == "a":
                answer = item[1]
                if len(item) > 2:
                    condition = item[2]
                else:
                    condition = None
                if type(answer) == str:
                    answers.append([answer, condition])
                elif type(answer) == list:
                    answers.append([answer])
            else:
                question = item[0]
                letter = letters[nq]
                if len(item) > 1:
                    next_level = item[1]
                else:
                    next_level = None
                if len(item) > 2:
                    var_set = item[2]
                else:
                    var_set = None
                questions.append([question, letter, next_level, var_set])
                nq += 1

        return answers, questions, current_level


    def process_answers (self, answer):
        conditions_status = True
        if len(answer)>1 and answer[1] is not None:
            conditions = answer[1].split(",")
            for condition in conditions:
                #print (condition)
                if condition.find(":") != -1:
                    var_name = condition.split(":")[0]
                    var_value = condition.split(":")[1]
                    if self.dialog["variables"][var_name] != var_value:
                        conditions_status = False
                elif condition.find("==") != -1:
                    var_name = condition.split("==")[0]
                    var_value = int(condition.split("==")[1])
                    if self.dialog["variables"][var_name] != var_value:
                        conditions_status = False
        if not conditions_status:
            return None
        if self.dialog["variables"]["language"] != "":
            if self.dialog["variables"]["language"] == "en":
                text_answer = answer[0].split("::")[0]
            else:
                text_answer = answer[0].split("::")[1]
        return text_answer


    def replace_tokens (self, text):
        mars_date = "{:.5f}".format(self.get_mars_time())
        mars_wrongdate = "{:.5f}".format(self.get_mars_time()-20)
        mars_distance = "{}Km".format(397500000)
        text = text.replace("#date#", mars_date)
        text = text.replace("#distance#", mars_distance)
        text = text.replace("#wrongdate#", mars_wrongdate)

        return text


    def process_text(self, user_input):
        answers_text = []
        questions_text = []

        if user_input is not None and self.pause is not True:
            for question in self.questions:
                if user_input == question[1]:
                    self.previous_level = self.current_level
                    self.current_level = question[2]
                    if question[3] is not None:
                        modified_vars = question[3].split(",")
                        for modification in modified_vars:
                            var_name = modification.split(":")[0]
                            var_value = modification.split(":")[1]
                            #print ("Set {} var to {}".format(var_name, var_value))
                            self.dialog["variables"][var_name] = var_value
        if self.pause:
            self.pause = False
        self.answers, self.questions, self.current_level = self.process(self.current_level)
        if len(self.answers) > 0:
            posible_answers = []
            for answer in self.answers:
                if type(answer[0]) == list:
                    answers_list = []
                    for ans in answer[0]:
                        text_answer = self.process_answers(ans)
                        if text_answer is not None:
                            answers_list.append(text_answer)
                    posible_answers.append(answers_list)
                else:
                    text_answer = self.process_answers(answer)
                    if text_answer is not None:
                        posible_answers.append([text_answer])
            if len(posible_answers) > 0:
                random_answer = random.choice(posible_answers)
                for answer in random_answer:
                    answer = self.replace_tokens(answer)
                    #print ("{}".format(answer))
                    answers_text.append(answer)
        if len(self.questions) > 0:
            for question in self.questions:
                if self.dialog["variables"]["language"] != "":
                    if self.dialog["variables"]["language"] == "en":
                        text_question = question[0].split("::")[0]
                    else:
                        text_question = question[0].split("::")[1]
                else:
                    text_question = question[0]
                text_question = self.replace_tokens(text_question)
                #print ("{}: {}".format(question[1], text_question))
                questions_text.append("{}: {}".format(question[1], text_question))
        else:
            self.current_level = self.previous_level
            self.pause = True
        #print()
        return self.pause, answers_text, questions_text

text_processor = rdanymvp()
input_text = None
while 1:
    pause, answers, questions = text_processor.process_text(input_text)
    print (answers)
    print (questions)
    if not pause:
        input_text = input(">")
