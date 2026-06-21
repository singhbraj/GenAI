import speech_recognition as sr

def main():
    r =sr.Recognizer() # Speech to Text

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        print("Speek Something....")
        audio = r.listen(source)

        print("Processing Audio...(STT)")
        stt = r.recognize_google(audio)

        print("You said:", stt)

main()