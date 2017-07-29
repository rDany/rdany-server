import random


dialog = {
    "variables" : {
        "language": "",
        "gender": "",
        "hi_count": 0
    },
    "root": [
        ["_English_", "language_selected", "language:en"],
        ["_Español_", "language_selected", "language:es"]
    ],
    "language_selected": [
        ["a", "Nice, we will talk in English then::Excelente, hablaremos en Español entonces"],
        ["_Ok_!::_Ok_!", "gender"],
        ["_Cancel_::_Cancelar_", "root"]
    ],
    "gender": [
        ["I prefer to be referred as _HE_::Prefiero que se dirigan a mi como _EL_", "gender_selected", "gender:male"],
        ["I prefer to be referred as _SHE_::Prefiero que se dirigan a mi como _ELLA_", "gender_selected", "gender:female"]
    ],
    "gender_selected": [
        ["a", [
            ["I am thinking: ::Estoy pensando: "],
            ["He is smart::Él es inteligente", "gender:male"],
            ["She is smart::Ella es inteligente", "gender:female"]
        ]],
        ["_Thank_ you!::_Gracias_!", "greetings"],
        ["_Change_::_Cambiar_", "gender"]
    ],
    "greetings": [
        ["_Hi_ Dany::_Hola_ Dany", "hi"],
        ["I want to ask you about _Mars_...::Te quería preguntar, acerca de _Marte_...", "mars_questions"],
        ["On what are you _working_ on?::¿En qué estás _trabajando_?", "mission"],
        ["Talk you _later_...::_Hablamos_ luego...", "talk_later"]
    ],
    "hi": [
        ["a", [
            ["Welcome!::¡Bienvenida!", "gender:female,hi_count==0"],
            ["Welcome!::¡Bienvenido!", "gender:male,hi_count==0"],
            ["Thanks for testing me on my MVP version :)::Gracias por probarme en mi versión MVP :)", "hi_count==0"]
        ]]
    ],
    "mars_questions": [
        ["a", "Yes?::Si?"],
        ["What _date_ is it there?::¿Qué _fecha_ tienes allí?", "mq_date"],
        ["What is the current _distance_ from Earth?::¿Cuál es la _distancia_ actual desde la Tierra?", "mq_distance"],
        ["Do you know some fun _fact_ about Mars?::¿Tienes algún _dato_ curioso sobre Marte?", "mq_funfact"]
    ],
    "mission": [
        ["a", "Working hard!::¡Trabajando duro!"]
    ],
    "talk_later": [
        ["a", "Time to keep exploring!::¡A seguir explorando!"],
        ["a", "Talk you later partner!::¡Hablamos luego compañera!", "gender:female"],
        ["a", "Talk you later partner!::¡Hablamos luego compañero!", "gender:male"],
        ["a", "I will be around!::¡Estaré por aquí!"]
    ]

}


def process(dialog, current_level):
    answers = []
    questions = []
    letters = "a b c d e f g h i j k l m".split(" ")

    nq = 0
    for item in dialog[current_level]:
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


def process_answers (dialog, answer):
    conditions_status = True
    if len(answer)>1 and answer[1] is not None:
        conditions = answer[1].split(",")
        for condition in conditions:
            #print (condition)
            if condition.find(":") != -1:
                var_name = condition.split(":")[0]
                var_value = condition.split(":")[1]
                if dialog["variables"][var_name] != var_value:
                    conditions_status = False
            elif condition.find("==") != -1:
                var_name = condition.split("==")[0]
                var_value = int(condition.split("==")[1])
                if dialog["variables"][var_name] != var_value:
                    conditions_status = False
    if not conditions_status:
        return None
    if dialog["variables"]["language"] != "":
        if dialog["variables"]["language"] == "en":
            text_answer = answer[0].split("::")[0]
        else:
            text_answer = answer[0].split("::")[1]
    return text_answer


pause = False
previous_level = "root"
current_level = "root"
user_input = None
while 1:
    if user_input is not None and pause is not True:
        for question in questions:
            if user_input == question[1]:
                previous_level = current_level
                current_level = question[2]
                if question[3] is not None:
                    modified_vars = question[3].split(",")
                    for modification in modified_vars:
                        var_name = modification.split(":")[0]
                        var_value = modification.split(":")[1]
                        #print ("Set {} var to {}".format(var_name, var_value))
                        dialog["variables"][var_name] = var_value
    if pause:
        pause = False
    answers, questions, current_level = process(dialog, current_level)
    if len(answers) > 0:
        posible_answers = []
        for answer in answers:
            if type(answer[0]) == list:
                answers_list = []
                for ans in answer[0]:
                    text_answer = process_answers(dialog, ans)
                    if text_answer is not None:
                        answers_list.append(text_answer)
                posible_answers.append(answers_list)
            else:
                text_answer = process_answers(dialog, answer)
                if text_answer is not None:
                    posible_answers.append([text_answer])
        if len(posible_answers) > 0:
            random_answer = random.choice(posible_answers)
            for answer in random_answer:
                print ("{}".format(answer))
    if len(questions) > 0:
        for question in questions:
            if dialog["variables"]["language"] != "":
                if dialog["variables"]["language"] == "en":
                    text_question = question[0].split("::")[0]
                else:
                    text_question = question[0].split("::")[1]
            else:
                text_question = question[0]
            print ("{}: {}".format(question[1], text_question))
    else:
        current_level = previous_level
        pause = True
    print()
    if not pause:
        user_input = input("> ")
