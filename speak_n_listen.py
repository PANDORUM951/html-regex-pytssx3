import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 150)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[2].id)

r = sr.Recognizer()


def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Escuchando... ")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="es-ES")
            print("He entendido: {}".format(text))
            return text
        except Exception:
            return


if __name__ == "__main__":
    speak("Probando si funciona todo")
    print(listen())
