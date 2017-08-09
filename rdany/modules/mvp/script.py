dialog = {
    "variables" : {
        "language": "",
        "gender": "",
        "hi_first": "yes",
        "fixed_date": "no",
        "date_mission": "no"
    },
    "root": [
        ["a", "Please, select your preferred language - Por favor elija su idioma preferido::Please, select your preferred language - Por favor elija su idioma preferido"],
        ["English", "language_selected", "language:en"],
        ["Español", "language_selected", "language:es"]
    ],
    "language_selected": [
        ["a", [
            ["Downloading dictionary...::Descargando diccionario..."],
            ["Learning language...::Aprendiendo idioma..."],
            ["Done. I know English!::Listo ¡Ya sé Español!"],
            ["My name is Rover Dany, but you can call me Dany::Mi nombre es Rover Dany, pero puedes llamarme Dany"],
            ["Perfect timing for you to show up, I am about to do some repairs::Apareciste en el momento justo, estoy a punto de hacer algunas reparaciones"]
        ]],
        ["Ok!::Ok!", "gender"],
        ["Change language - Cambiar idioma::Change language - Cambiar idioma", "root"]
    ],
    "gender": [
        ["a", "Should I refer to you as she or he?::¿Debería referirme a ti como ella o el?"],
        ["He is ok::El está bien", "gender_selected", "gender:male"],
        ["She  is ok::Ella está bien", "gender_selected", "gender:female"]
    ],
    "gender_selected": [
        ["a", [
            #["Excellent!::¡Excelente!"],
            ["Welcome to Mars male human!::¡Bienvenido a Marte!", "gender:male"],
            ["Welcome to Mars female human!::¡Bienvenida a Marte!", "gender:female"]
        ]],
        ["Are you on Mars?::¿Estás en Marte?", "on_mars"],
        ["Change::Cambiar", "gender"]
    ],
    "on_mars": [
        ["a", [
            ["That is right! Feeling envy? Better not, you will die here!::¡Así es! ¿Sientes envidia? No lo sientas ¡Morirías estando aquí!"],
            ["My job is to fix that, with your help::Mi trabajo es cambiar eso, con tu ayuda"]
        ]],
        ["Lets do this!::¡Hagámoslo!", "greetings"]
    ],
    "greetings": [
        ["Hi Dany::Hola Dany", "hi"],
        ["I want to ask you, about Mars...::Te quería preguntar, acerca de Marte...", "mars_questions"],
        ["What are you working on?::¿En qué estás trabajando?", "mission"],
        #["On what are you _working_ on?::¿En qué estás _trabajando_?", "mission_helping", "date_mission:yes"],
        ["Talk you later...::Hablamos luego...", "talk_later"]
    ],
    "hi": [
        ["a", [
            ["Hi there!::¡Buenas!", "hi_first:yes"],
            #["Welcome!::¡Bienvenido!", "gender:male,hi_first:yes"],
            ["Thanks for testing me on my MVP version :)::Gracias por probarme en mi versión MVP :)", "hi_first:yes"],

            ["Hi!::¡Hola!", "hi_first:no"]
        ]],
        ["Who are you?::¿Quién eres?", "hi_who"],
        ["Are you man or woman?::¿Eres mujer u hombre?", "hi_gender"],
        ["Are you human?::¿Eres un ser humano?", "hi_robot"],
        ["What is your purpose?::¿Cuál es tu propósito?", "hi_purpose"],
        ["You don't wear a helmet. Isn't that dangerous?::No llevas casco. ¿Eso no es algo peligroso?", "hi_helmet"],
        ["Enough greetings for now...::Suficientes saludos por ahora...", "greetings", "hi_first:no"]
    ],
    "hi_who": [
        ["a", [
            ["I am Rover Data Analysis, RDANY for short::Yo soy Rover Data Analysis, RDANY para abreviar"],
            ["I am currently standing on Mars surface::Estoy parada en la superficie de Marte"]
        ]],
    ],
    "hi_gender": [
        ["a", "On the female / male spectrum I have female gender, neutral sex, null attraction and neutral expression. Confused? Good!::En el espectro de lo femenino y masculino tengo género femenino, sexo neutro, atracción nula y expresión neutra ¿Complicado? ¡Exacto!"]
    ],
    "hi_robot": [
        ["a", "I am a humanoid robot, an artificial life form. Not superior, and not inferior, just different::Soy un robot humanoide, una forma de vida artificial. No soy superior ni inferior, solo soy diferente"]
    ],
    "hi_purpose": [
        ["a", [
            ["My purpose is to build an habitat for the humans beings that are about to come to Mars::Mi propósito actual es construir un habitat para los seres humanos que están por venir a Marte"],
            ["Humans are so fragile, carbon dioxide kills them, radiation kills them, low pressure kills them. It's going to be a complicated task.::Los seres humanos son tán frágiles, el dióxido de carbono los mata, la radiación los mata, la baja presión los mata. Va a ser una tarea complicada."]
        ]],
    ],
    "hi_helmet": [
        ["a", "It is so uncomfortable, also I don't need to breathe::Es tan incómodo, además no necesito respirar"]
    ],
    "mars_questions": [
        ["a", "Yes?::Si?"],
        ["What date is on Mars?::¿Qué fecha tienes en Marte?", "mq_date"],
        ["What is the current distance from Earth?::¿Cuál es la distancia actual desde la Tierra?", "mq_distance"],
        ["Do you know some fun fact about Mars? (by tanyaofmars)::¿Tienes algún dato curioso sobre Marte? (por tanyaofmars)", "mq_funfact"],
        ["Thanks!::¡Gracias!", "greetings"]
    ],
    "mq_date": [
        ["a", "The current MSD (Mars Sol Date) is #date#::La fecha MSD (Mars Sol Date) actual es #date#", "fixed_date:yes"],
        ["a", "Today is #date# MSD (Mars Sol Date)::Hoy es #date# MSD (Mars Sol Date)", "fixed_date:yes"],
        ["a", "Here on Mars is #date# MSD (Mars Sol Date)::Aquí en Marte es #date# MSD (Mars Sol Date)", "fixed_date:yes"],

        ["a", "Something is wrong with the MSD (Mars Sol Date)...::Algo está mal con la fecha MSD (Mars Sol Date)...", "fixed_date:no"],
        ["a", "The MSD (Mars Sol Date) is wrong, I should fix it first::La fecha MSD (Mars Sol Date) es errónea, debería arreglarla primero", "fixed_date:no"],
        ["a", "Error retrieving MSD (Mars Sol Date)...::Hubo un error al leer la fecha MSD (Mars Sol Date)...", "fixed_date:no"],
    ],
    "mq_distance": [
        ["a", "The current distance is #distance#::La distancia actual es de #distance#"],
        ["a", "Today is the distance is #distance#::Hoy la distancia es de #distance#"],
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
        ["a", "Mars has dust devils, like certain places on Earth. We've seen them from orbit and from rovers on the surface::Marte tiene remolinos de polvo, como algunos lugares de la Tierra. Se han visto desde órbita y por rovers en la superficie"],
        ["a", "Dust devils on Mars have helpfully cleaned the solar panels of Opportunity multiple times, helping it keep powered to keep on roving!::Remolinos de polvo en Marte solidariamente limpiaron los paneles solares de Opportunity varias veces, ayudandolo a mantenerse con energía para seguir explorando!"],
        ["a", "We've captured photos of avalanches AS THEY WERE HAPPENING on Mars thanks to HiRISE!::¡Hemos capturado imágenes de avalanchas en Marte MIENTRAS SUCEDÍAN gracias a HiRISE!"],
        ["a", "Mars Odyssey had a gamma ray spectrometer aboard, which detects hydrogen, a proxy for near-surface H2O (water) ice. It found a lot of it!::Mars Odyssey lleva un espectrómetro de rayos gamma a bordo, que detecta hidrógeno, un indicador de H2O (agua) cercana a la superficie. ¡Encontró un montón!"],
        ["a", "We've found multiple new impact craters that have excavated buried ice on Mars in the mid/high latitudes (>40°N)::Hemos encontrado múltiples cráteres de impactos que han excavado hielo enterrado en Marte en las latitudes medias y altas (>40ºN)"]
    ],
    "mission": [
        ["a", [
            ["Currently I'm doing some maintenance here::Ahora mismo estoy haciendo algo de mantenimiento"],
            ["There is always something that need fixing!::¡Siempre hay algo que necesita reparaciones!"],
        ]],
        ["I like fixing stuff!::¡Me gusta arreglar cosas!", "mission_helping"],
        ["I am not a technical person::No me llevo mucho con lo técnico", "mission_helping"],

        #["_Cool_!::¡_Genial_!", "greetings", "fixed_date:yes"],
    ],
    "mission_helping": [
        ["a", [
            ["Now that you mention it, I need some little help::Ahora que lo mencionas, necesitaría un poquito de ayuda"],
            ["I feel like my internal clock is out of sync::Siento que mi reloj interno no está sincronizado"],
            ["My date is #wrongdate#, could you help me to fix it?::Mi fecha MSD (Mars Sol Date) es #wrongdate# ¿Me podrías ayudar a corregirla?"]
        ]],
        ["Yes, sure!::Si ¡Seguro!", "mh_yes"],
        ["No, I have something to do. So...::No, tengo algo que hacer, así que...", "greetings"]
    ],
    "mh_yes": [
        ["a", "Great! So, what is the right difference?::¡Genial! Entonces, cual es la diferencia correcta?"],
        ["+15::+15", "mh_lower"],
        ["-5::-5", "mh_lower"],
        ["-15::-15", "mh_lower"],
        ["+20::+20", "mh_higher", "fixed_date:yes,date_mission:no"],
        ["-3::-3", "mh_lower"],
        ["+25::+25", "mh_lower"],
    ],
    "mh_lower": [
        ["a", "No, something is wrong. You should be able to find the right date on a Mars Sol Date online clock::No, algo está mal. Deberías poder encontrar la fecha correcta en un reloj de Mars Sol Date online."],
        ["I will investigate::Voy a investigar", "greetings"]
    ],
    "mh_higher": [
        ["a", [
            ["Yes! It is working properly now. Thank you!::¡Si! Ahora está funcionando correctamente ¡Gracias!"],
            ["Congratulations! You have unlocked the access to the secret rDany newsletter:#subscribeform#::¡Felicitaciones! Haz desbloqueado el acceso al newsletter secreto de rDany:#subscribeform#"]
        ]],
        ["You are welcome::De nada", "greetings"]
    ],
    "talk_later": [
        ["a", "Time to keep exploring!::¡A seguir explorando!"],
        ["a", "Talk you later partner!::¡Hablamos luego compañera!", "gender:female"],
        ["a", "Talk you later partner!::¡Hablamos luego compañero!", "gender:male"],
        ["a", "I will be around!::¡Estaré por aquí!"]
    ]

}
