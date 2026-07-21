from speech.recognizer import listen


while True:

    text = listen()

    print(
        "OUTPUT:",
        text
    )