import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import re

from attendance.session_manager import (
    start_new_session,
    end_session,
    get_active_session
)

from attendance.attendance_service import mark_attendance

# =========================
# MODEL
# =========================
MODEL_PATH = "models/vosk-model-small-en-us-0.15"

# =========================
# NUMBER WORDS
# =========================
WORDS_TO_NUM = {
    "zero": "0",
    "oh": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

# =========================
# MIC SELECTION
# =========================
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

# =========================
# AUDIO CALLBACK
# =========================
def callback(indata, frames, time, status):
    if status:
        print("Audio status:", status)

    q.put(bytes(indata))


# =========================
# WORDS → DIGITS
# =========================
def words_to_number(text):
    digits = []

    for word in text.split():

        clean = word.lower()

        if clean in WORDS_TO_NUM:
            digits.append(WORDS_TO_NUM[clean])

        elif clean.isdigit():
            digits.append(clean)

    if digits:
        return "".join(digits)

    return None


# =========================
# HYBRID PARSER
# =========================
def parse_command(text):

    text = text.lower().strip()

    # ---------------------
    # SESSION COMMANDS
    # ---------------------
    if "start attendance" in text:
        return ("start_session", None, None, None)

    if (
        "end attendance" in text
        or "finish attendance" in text
        or "stop attendance" in text
    ):
        return ("end_session", None, None, None)

    # ---------------------
    # ACTION DETECTION
    # ---------------------
    action = None

    if any(word in text for word in [
        "present",
        "president",
        "preserved",
        "prison"
    ]):
        action = "Present"

    elif "absent" in text:
        action = "Absent"

    # ---------------------
    # ID EXTRACTION
    # ---------------------
    index_number = words_to_number(text)

    if not index_number:

        match = re.search(r"\b\d{3,12}\b", text)

        if match:
            index_number = match.group(0)

    # ---------------------
    # NAME EXTRACTION
    # ---------------------
    words = text.split()

    spoken_name = None

    for w in words:

        if (
            w not in WORDS_TO_NUM
            and not w.isdigit()
            and w not in [
                "present",
                "president",
                "preserved",
                "prison",
                "absent",
                "mark",
                "attendance"
            ]
        ):
            spoken_name = w
            break

    # ---------------------
    # ATTENDANCE COMMAND
    # ---------------------
    if index_number and action:
        return (
            "attendance",
            index_number,
            spoken_name,
            action
        )

    return (None, None, None, None)


# =========================
# MAIN LISTENER
# =========================
def start_listening():

    print("\n🎤 Listening (Hybrid Mode)...")
    print("👉 Say 'start attendance' to begin\n")

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    session_id = None

    with sd.RawInputStream(
        device=DEVICE_INDEX,
        samplerate=16000,
        blocksize=4000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):

        while True:

            data = q.get()

            if recognizer.AcceptWaveform(data):

                result = json.loads(
                    recognizer.Result()
                )

                text = result.get("text", "")

                if not text:
                    continue

                print("🗣️ Heard:", text)

                cmd, index_number, spoken_name, action = parse_command(text)

                # -------------------------
                # START SESSION
                # -------------------------
                if cmd == "start_session":

                    session_id = start_new_session(
                        course_id=1,
                        period="Morning"
                    )

                    print(
                        f"🟢 Session started: {session_id}"
                    )

                    print(
                        "👉 Start saying: Name ID Status"
                    )

                    print(
                        "👉 Example: Kims two three one zero zero zero present"
                    )

                    continue

                # -------------------------
                # END SESSION
                # -------------------------
                if cmd == "end_session":

                    if session_id:

                        end_session()

                        print(
                            f"🔴 Session ended: {session_id}"
                        )

                        session_id = None

                    else:
                        print("⚠️ No active session")

                    continue

                # -------------------------
                # ATTENDANCE
                # -------------------------
                if cmd == "attendance":

                    if not session_id:

                        print(
                            "⚠️ No active session. Say 'start attendance'"
                        )

                        continue

                    result = mark_attendance(
                        session_id=session_id,
                        index_number=index_number,
                        spoken_name=spoken_name,
                        status=action
                    )

                    print("🗄️ DB:", result)

                    continue

                # -------------------------
                # EXIT
                # -------------------------
                if "exit" in text:

                    print("🛑 Stopping...")
                    break

                print("⚪ Ignored noise")


if __name__ == "__main__":
    start_listening()