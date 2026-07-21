import json
import queue
import sounddevice as sd

from vosk import Model, KaldiRecognizer


# ==============================
# VOSK MODEL LOCATION
# ==============================

MODEL_PATH = "models/vosk-model-small-en-us-0.15"


# ==============================
# AUDIO SETTINGS
# ==============================

SAMPLE_RATE = 16000


audio_queue = queue.Queue()



# ==============================
# MICROPHONE CALLBACK
# ==============================

def callback(
    indata,
    frames,
    time,
    status
):

    if status:
        print(status)


    audio_queue.put(
        bytes(indata)
    )



# ==============================
# START LISTENING
# ==============================

def listen():

    print("🎤 Listening...")


    model = Model(
        MODEL_PATH
    )


    recognizer = KaldiRecognizer(
        model,
        SAMPLE_RATE
    )



    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):


        while True:


            data = audio_queue.get()


            if recognizer.AcceptWaveform(data):

                result = json.loads(
                    recognizer.Result()
                )


                text = result.get(
                    "text",
                    ""
                )


                if text:

                    print(
                        "Heard:",
                        text
                    )


                    return text