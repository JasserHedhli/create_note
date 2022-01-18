from neuralintents import GenericAssistant
import pyttsx3 as tts
import speech_recognition as sr
import sys

recognizer = sr.Recognizer()

engine = tts.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


todo_list = ["Go shopping", "Clean Room", "Record video"]


def create_note():
    global recognizer

    engine.say("What do you want to write into your note?")
    engine.runAndWait()
    done = False

    while not done:
        try:
            with sr.Microphone() as source:
                recognizer.energy_threshold = 10000
                recognizer.adjust_for_ambient_noise(source, 1.2)
                audio = recognizer.listen(source)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                engine.say('Choose a filename!')
                engine.runAndWait()

                recognizer.energy_threshold = 10000
                recognizer.adjust_for_ambient_noise(source, 1.2)
                audio = recognizer.listen(source)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(f"{filename}.txt", 'w') as file:
                file.write(note)
                done = True
                engine.say(f"I successfully created the note{filename}")
                engine.runAndWait()
        except sr.UnknownValueError():
            recognizer = sr.Recognizer()
            engine.say('I did not understand you! Please try again!')
            engine.runAndWait()


def add_todo():
    while not done:
        try:
            with sr.Microphone() as source:
                recognizer.energy_threshold = 10000
                recognizer.adjust_for_ambient_noise(source, 1.2)
                audio = recognizer.listen(source)

                todo = recognizer.recognize_google(audio)
                todo = todo.lower()
                todo_list.append(todo)

                done = True

                engine.say(f"I added {todo} to the todo list")
                engine.runAndWait()

        except sr.UnknownValueError():
            recognizer = sr.Recognizer()
            engine.say('I did not understand you! Please try again!')
            engine.runAndWait()


def show_todos():
    engine.say("The todos on your todo list are the following")
    for todo in todo_list:
        engine.say(todo)
    engine.runAndWait()


def hello():
    engine.say("Hello, what can  do for you?")
    engine.runAndWait()


def quit():
    engine.say('Peace')
    engine.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "goodbye": quit
}


assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with sr.Microphone() as source:
            recognizer.energy_threshold = 10000
            recognizer.adjust_for_ambient_noise(source, 1.2)
            audio = recognizer.listen(source)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request()
    except sr.UnknownValueError():
        recognizer = sr.Recognizer()
