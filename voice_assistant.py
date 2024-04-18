import re
from speak_n_listen import speak, listen


def identify_name(text):
    name = None

    patterns = ["me llamo ([A-Za-z]+)", "mi nombre es ([A-Za-z]+)", "^([A-Za-z]+)$", "soy ([A-Za-z]+)"]
    for pattern in patterns:
        try:
            name = re.findall(pattern, text)[0]
        except IndexError:
            pass
    return name


def message(name):
    if name:
        speak("Encantado de conocerte, {}.".format(name))
        print("Encantado de conocerte, {}.".format(name))
    else:
        print("No le he entendido.")


def main():
    # Engine asks name
    speak("Hola, ¿cómo te llamas?")

    # Voice recognition
    text = listen()
    name = identify_name(text)

    # Engine answers
    message(name)


if __name__ == "__main__":
    main()
