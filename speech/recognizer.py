import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import re

# ✅ MODEL PATH
MODEL_PATH = "models/vosk-model-small-en-us-0.15"

# ==============================
# 🔍 AUTO MIC SELECT (BEST INPUT)
# ==============================
def get_best_mic():
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0:
            name = d["name"].lower()
            if "microphone" in name or "mic" in name:
                print(f"🎯 Using mic: {i} -> {d['name']}")
                return i
    print("⚠️ Defaulting to mic 0")
    return 0


DEVICE_INDEX = get_best_mic()

q = queue.Queue()


# ==============================
# 🎙 AUDIO CALLBACK
# ==============================
def callback(indata, frames, time, status):
    if status:
        print("Audio status:", status)
    q.put(bytes(indata))


# ==============================
# 🧠 PARSE COMMAND
# ==============================
def parse_command(text):
    text = text.lower().strip()

    # extract number (student ID)
    match = re.search(r"\b\d{3,10}\b", text)
    student_id = match.group(0) if match else None

    # detect action
    if "present" in text:
        action = "present"
    elif "absent" in text:
        action = "absent"
    else:
        action = None

    return student_id, action


# ==============================
# 🚀 MAIN LISTENER
# ==============================
def start_listening():
    print("\n🎤 Listening (optimized mode)...\n")

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    with sd.RawInputStream(
        device=DEVICE_INDEX,
        samplerate=16000,
        blocksize=4000,   # 🔥 reduced lag
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    print("🗣️ Heard:", text)

                    student_id, action = parse_command(text)

                    if student_id and action:
                        print(f"✅ Parsed → ID: {student_id}, Action: {action}")

                        # 👉 CALL YOUR DB FUNCTION HERE
                        # mark_attendance(student_id, action)

                    else:
                        print("⚠️ Could not parse command properly")

                    if "exit" in text:
                        print("🛑 Stopping...")
                        break


if __name__ == "__main__":
    start_listening()