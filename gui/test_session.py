"""Launch the complete session + dashboard + voice-recognition flow.

This used to open only ``SessionWindow``.  That was useful for a visual test,
but it had no attendance dashboard registered and no VoiceThread running.
"""

from speech.run_voice import start_application


if __name__ == "__main__":
    start_application()
