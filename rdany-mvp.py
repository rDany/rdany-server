import time
import random


dialog = {
    "variables" : {
        "language": "",
        "gender": "",
        "hi_first": "yes",
        "fixed_date": "no",
        "date_mission": "no"
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
        ["I prefer to be referred as _he_::Prefiero que se dirigan a mi como _el_", "gender_selected", "gender:male"],
        ["I prefer to be referred as _she_::Prefiero que se dirigan a mi como _ella_", "gender_selected", "gender:female"]
    ],
    "gender_selected": [
        ["a", [
            ["Excelent!::¡Excelente!"],
            ["You are a welcomed he::¡Bienvenido!", "gender:male"],
            ["You are a welcomed she::¡Bienvenida!", "gender:female"]
        ]],
        ["_Thank_ you!::_Gracias_!", "greetings"],
        ["_Change_::_Cambiar_", "gender"]
    ],
    "greetings": [
        ["_Hi_ Dany::_Hola_ Dany", "hi"],
        ["I want to ask you about _Mars_...::Te quería preguntar, acerca de _Marte_...", "mars_questions"],
        ["On what are you _working_ on?::¿En qué estás _trabajando_?", "mission"],
        #["On what are you _working_ on?::¿En qué estás _trabajando_?", "mission_helping", "date_mission:yes"],
        ["Talk you _later_...::_Hablamos_ luego...", "talk_later"]
    ],
    "hi": [
        ["a", [
            ["Welcome!::¡Bienvenida!", "gender:female,hi_first:yes"],
            ["Welcome!::¡Bienvenido!", "gender:male,hi_first:yes"],
            ["Thanks for testing me on my MVP version :)::Gracias por probarme en mi versión MVP :)", "hi_first:yes"],

            ["Hi!::¡Hola!", "hi_first:no"]
        ]],
        ["_Who_ are you?::¿_Quién_ eres?", "hi_who"],
        ["What is your _purpose_?::¿Cuál es tu _propósito_?", "hi_purpose"],
        ["Enough greetings for now...::_Suficientes_ saludos por ahora...", "greetings", "hi_first:no"]
    ],
    "hi_who": [
        ["a", "I am Rover Data Analysis, RDANY for short::Yo soy Rover Data Analysis, RDANY para abreviar"]
    ],
    "hi_purpose": [
        ["a", "To explore::Explorar"]
    ],
    "mars_questions": [
        ["a", "Yes?::Si?"],
        ["What _date_ is it there?::¿Qué _fecha_ tienes allí?", "mq_date"],
        ["What is the current _distance_ from Earth?::¿Cuál es la _distancia_ actual desde la Tierra?", "mq_distance"],
        ["Do you know some fun _fact_ about Mars? (by tanyaofmars)::¿Tienes algún _dato_ curioso sobre Marte? (por tanyaofmars)", "mq_funfact"],
        ["Thanks!::¡Gracias!", "greetings"]
    ],
    "mq_date": [
        ["a", "The current date is #date#::La fecha actual es #date#", "fixed_date:yes"],
        ["a", "Today is #date#::Hoy es #date#", "fixed_date:yes"],
        ["a", "Here on Mars is #date#::Aquí en Marte es #date#", "fixed_date:yes"],

        ["a", "Something is wrong with the date...::Algo está mal con la fecha...", "fixed_date:no"],
        ["a", "The date is wrong, I should fix it first::La fecha es erronea, debería arreglarla primero", "fixed_date:no"],
        ["a", "Error retrieving the date...::Hubo un error al leer la fecha...", "fixed_date:no"],
    ],
    "mq_distance": [
        ["a", "The current distance is #distance#::La distancia actual es #distance#"],
        ["a", "Today is #distance#::Hoy es #distance#"],
        ["a", "From Earth to Mars the distance is #distance#::Desde la Tierra hasta Marte la distancia es de #distance#"]
    ],
    "mq_funfact": [
        ["a", "Mars doesn't appear to have had plate tectonics. Earth seems to be the only place in the Solar System that does!::Marte no parece haber tenido placas tectónicas ¡La Tierra parece ser el único lugar en el Sistema Solar que tiene!"],
        ["a", "Mars has huge volcanoes, including Olympus Mons, the tallest in the Solar System. But none have been active for >100 million years::Marte tiene volcanes inmensos, incluyendo el Monte Olimpo, el mas alto del Sistema Solar. Pero ninguno ha estado activo por >100 millones de años"],
        ["a", [
            ["Valles Marineris is often called the largest \"canyon\" in the Solar System. But it's actually a series of \"chasmata\"::Al Valles Marineris se le suele llamar el \"cañón\" mas grande del Sistema Sola. Pero es en realidad una serie de \"chasmas\""],
            ["These chasmata likely formed separately & then coalesced as they grew over time ::Esos chasmas probablemente se formaron por separado y luego se fusionaron a medida que crecieron a lo largo del tiempo"]
        ]],
        ["a", "Valles Marineris was named for the mission that discovered it, Mariner 9, which arrived at Mars in 1971::Valles Marineris fue nombrado por la misión que lo descubrió, Mariner 9, que arrivó a Marte en 1971"],
        ["a", "The first successful mission to Mars, Mariner 4, flew by in 1965. Mariner Crater is named in its honour::La primera misión exitosa a Marte, Mariner 5, pasó sobrevolando en 1965. El crater Mariner fue nombrado en su honor"],
        ["a", "You can see a surprising amount of detail on Mars with even a poor quality telescope. Huygens spotted Syrtis Major & S polar cap in 1659!::Puedes ver una sorprendente cantidad de detalle en Marte incluso con un telescopio de mala calidad ¡Huygens vió Syrtis Major y casquete polar sur en 1659!"],
        ["a", "While Lowell is famous for his \"canals\" on Mars, the idea of them wasn't widely accepted by the scientific community in his day::Mientras que Lowell es famoso por sus \"canales\" en Marte, su idea no era ampliamente aceptada por la comunidad científica en su tiempo"],
        ["a", "Gale Crater, where Mars Curiosity currently lives, is an example of a buried -> exhumed (un-buried) crater::Gale Crater, donde Mars Curiosity vive actualmente, es un ejemplo de un crater enterrado -> exhumado (desenterrado)"],
        ["a", "Mars's surface is red due to iron oxide. But if you get below the rusty dust, it's often not red at all!::La superficie de Marte es roja debido al óxido de hierro. Pero si buscas bajo la superficie ¡Normalmente no es para nada rojo!"],
        ["a", "When Spirit's right front wheel stopped working, it serendipitously dug a trench that exposed nearly pure silica, evidence of past water::Cuando la rueda delantera derecha de Spirit dejó de funcionar, afortunadamente escarvó un zurco que expuso silicio en estado casi puro, evidencia de agua en el pasado"],
        ["a", "The Phoenix lander dug a small trench at its northern high latitude landing site on Mars, revealing buried ice!::Phoenix lander escarvó un pequeño zurco en su sitio de aterrizaje en las altas latitudes nortes de Marte ¡Revelando hielo enterrado!"],
        ["a", "Newly-formed impact craters on Mars blast away the dust on the surface around them, revealing the underlying darker nature of Mars::Cráteres de impacto formados recientemente en Marte lanzan lejos el polvo en la superficie a su alrededor, revelando la oscura naturaleza interior de Marte"],
        ["a", "The south polar cap of Mars, made of CO2 ice, is mysteriously eroding away. The northern polar cap, made of water ice, seems stable::La casquete polar sur de Marte, hecha de CO2 congelado, se está erocionando misteriosamente. El casquete polar norte, compuesta de agua congelada, parece mantenerse estable"],
        ["a", "Junocam aboard Juno is based on Mars Curiosity's Mars Descent Imager (MARDI)::Junocam a bordo de Juno está basada en Mars Descent Imager (MARDI) de Mars Curiosity"],
        ["a", "The HiRISE camera aboard NASA's Mars Reconnaissance Orbiter captured Mars Curiosity as it was landing!::¡La cámara HiRISE a bordo de Mars Reconnaissance Orbiter de la NASA capturó a Mars Curiosity mientras aterrizaba!"],
        ["a", "We've sent ground penetrating radar instruments to Mars, which see the internal structure of the polar caps::Hemos enviado a Marte instrumentos de radar capaces de penetrar el suelo, capaz de ver la estructura interna de los casquetes polares"],
        ["a", "Mars Global Surveyor and Mars Reconnaissance Orbiter have been monitoring Mars' weather for years! Weekly weather reports: http://www.msss.com/msss_images/latest_weather.html::¡Mars Global Surveyor y Mars Reconnaissance Orbiter han estado monitoreando el clima de Marte por años! Reporte de clima semanal: http://www.msss.com/msss_images/latest_weather.html"],
        ["a", [
            ["In May of 2003, Mars Global Surveyor imaged Jupiter and some of its moons from orbit around Mars::En Mayo de 2003, Mars Global Surveyor tomó una fotografía de Jupiter y de algunas de sus lunas desde la órbita alrededor de Marte"],
            ["On the same day, Mars Global Surveyor also imaged Earth and the Moon from orbit around Mars::En el mismo día, Mars Global Surveyor también fotografió la Tierra y la Luna desde la órbita de Marte"],
        ]],
        ["a", "Mars Global Surveyor managed to snap a pic of a fellow orbiter, Mars Odyssey, in 2005!::¡Mars Global Surveyor logró tomar una imagen de su compañero orbitador, Mars Odyseey, en 2005!"],
        ["a", "Mars has dust devils, like certain places on Earth. We've seen them from orbit and from rovers on the surface::Marte tiene remolinos de polvo, como algunos lugares de la Tierra. Se han visto desde órbita y po rovers en la superficie"],
        ["a", "Dust devils on Mars have helpfully cleaned the solar panels of Opportunity multiple times, helping it keep powered to keep on roving!::Remolinos de polvo en Marte solidariamente limpiaron los paneles solares de Opportunity varias veces, ayudandolo a mantenerse con energía para seguir explorando!"],
        ["a", "We've captured photos of avalanches AS THEY WERE HAPPENING on Mars thanks to HiRISE!::¡Hemos capturado imágenes de avalanchas en Marte MIENTRAS SUCEDÍAN gracias a HiRISE!"],
        ["a", "Mars Odyssey had a gamma ray spectrometer aboard, which detects hydrogen, a proxy for near-surface H2O (water) ice. It found a lot of it!::Mars Odyssey lleva un espectrómetro de rayos gamma a bordo, que detecta hidrógeno, un indicador de H2O (agua) cercana a la superficie. ¡Encontró un montón!"],
        ["a", "We've found multiple new impact craters that have excavated buried ice on Mars in the mid/high latitudes (>40°N)::Hemos encontrado múltiples cráteres de impactos que han excavado hielo enterrado en Marte en las latitudes medias y altas (>40ºN)"]
    ],
    "mission": [
        ["a", [
            ["Working hard! But it has its rewards::¡Trabajando duro! Pero tiene sus recompensas"],
            ["The landscape is unique!::¡El paisaje es único!"],
        ]],
        ["Sounds _exhousting_!::Suena _cansador_...", "mission_helping"],
        ["_Not_ for me!::¡Suena a que _no_ es para mi!", "mission_helping"],

        #["_Cool_!::¡_Genial_!", "greetings", "fixed_date:yes"],
    ],
    "mission_helping": [
        ["a", [
            ["Now that you mention it, I need some little help::Ahora que lo mensionas, necesitaría un poquito de ayuda"],
            ["I feel like my internal clock is out of sync::Siento que mi reloj interno no está sincronizado"],
            ["My date is #wrongdate#, could you tell me if the value should be lower or higher?::Mi fecha es #wrongdate# ¿Me podrías decir si el valor debería ser mas bajo o mas alto?"]
        ]],
        ["_Yes_, sure!::_Si_ ¡Seguro!", "mh_yes"],
        ["_No_, I have something to do. So...::_No_, tengo algo que hacer, así que...", "greetings"]
    ],
    "mh_yes": [
        ["a", "Great! So, should be lower or higher?::¡Genial! Entonces, debería ser mas bajo, o mas alto?"],
        ["_Lower_::Mas _bajo_", "mh_lower"],
        ["_Higher_::Mas _alto_", "mh_higher", "fixed_date:yes,date_mission:no"]
    ],
    "mh_lower": [
        ["a", "No, something is wrong. You should be able to find the right date on a Martian online clock::No, algo está mal. Deberías poder encontrar la fecha correcta en un reloj de Marte online."],
    ],
    "mh_higher": [
        ["a", "Yes! Now is working properly. Thank you!::¡Si! Ahora está funcionando correctamente ¡Gracias!"],
        ["You are _welcome_::De _nada_", "greetings"]
    ],
    "talk_later": [
        ["a", "Time to keep exploring!::¡A seguir explorando!"],
        ["a", "Talk you later partner!::¡Hablamos luego compañera!", "gender:female"],
        ["a", "Talk you later partner!::¡Hablamos luego compañero!", "gender:male"],
        ["a", "I will be around!::¡Estaré por aquí!"]
    ]

}


def get_mars_time():
    millis = time.time()
    JDut = (millis / (8.64 * 1.e4)) + 2440587.5
    JDtt = JDut + (37 + 32.184) / 86400
    J2000 = JDtt - 2451545
    MSD = (((J2000 - 4.5) / 1.027491252) + 44796 - 0.00096)
    return MSD


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


def replace_tokens (text):
    mars_date = "{:.5f}".format(get_mars_time())
    mars_wrongdate = "{:.5f}".format(get_mars_time()-20)
    mars_distance = "{}Km".format(397500000)
    text = text.replace("#date#", mars_date)
    text = text.replace("#distance#", mars_distance)
    text = text.replace("#wrongdate#", mars_wrongdate)

    return text


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
                answer = replace_tokens(answer)
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
            text_question = replace_tokens(text_question)
            print ("{}: {}".format(question[1], text_question))
    else:
        current_level = previous_level
        pause = True
    print()
    if not pause:
        user_input = input("> ")
        print ()
        print ()
