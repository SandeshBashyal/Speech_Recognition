import pyaudio
import pyttsx3 as tts
import speech_recognition as sr
import time
# from vosk import Model, KaldiRecognizer

# sample_rate = 16000

def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...', end = '', flush = True)
        # time.sleep(1)
        audio = r.listen(source)
        print('Audio Length:', len(audio.frame_data))
        # query = ""
        try:
            
            print('Recognizing...', end = '', flush = True)
            # model = Model("/vosk-model-small-en-us-0.15")
            # recognizer = KaldiRecognizer(model, sample_rate)
            # print('Intermediate Result:', recognizer.Result())
            # recognizer.AcceptWaveform(audio.frame_data)
            # query = recognizer.FinalResult() #Json file
            query = r.recognize_google(audio, language = 'en-US')
            # query = r.recognize_sphinx(audio, language = 'en-US')
            print(f'User said: {query}')

        except sr.UnknownValueError:
            print('Sorry, I did not hear your request.')
            query = ""

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            query = ""

    return query.lower()


#def speak(text):
#    engine = tts.init(driverName='espeak')
#    voices = engine.getProperty('voices')
#    engine.setProperty('voice', voices[0].id)
#    print('KYBS__NYHU: ' + text + '\n')
#    engine.say(text)
#    engine.runAndWait()
    
def speak(text):
    engine = tts.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    print('KYBS__NYHU: ' + text + '\n')
    engine.say(text)
    engine.runAndWait()


def main():
    Talk = True
    while Talk ==True:
        usersaid = takeCommand()
        if 'hello' in usersaid:
            speak('hello')

        if 'bye' in usersaid:
            speak('bye')

        if 'how are you' in usersaid:
            speak('doing well')

        if 'is this video good' in usersaid:
            speak('like and suscribe')

        if 'stop' in usersaid:
            speak('stopping')
            break

        if 'exit' in usersaid:
            speak('ending program')
            Talk = False

        if 'do function' in usersaid:
            speak('i will perform this function')

        time.sleep(2)
main()
