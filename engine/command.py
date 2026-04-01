import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    engine.setProperty('volume', 1.0)   
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()
 #new 


def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)  #timeout=10, phrase_time_limit=12)


    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        return query.lower()
    except Exception as e:
        print("Error:", e)
        return ""#Sorry, I didn't understand"

# @eel.expose
# def allCommands():
#     try:
#         query = takecommand()
#         print("User said:", query)

#         if query == "" or query is None:
#             return "No input"

#         if "open" in query:
#             openCommand(query)
#             return "done"

#         elif "youtube" in query:
#             PlayYoutube(query)
#             return "done"

#         else:
#             chatBot(query)
#             return "done"

#     except Exception as e:
#         print("Error in allCommands:", e)
#         return "error"


@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        eel.senderText(query)
    else:
        query = message.lower()
        eel.senderText(query)

    print("User:", query)   # 👈 DEBUG

    try:
        if "call" in query or "video" in query or "message" in query:
            print("WhatsApp command")

            from engine.features import findContact, whatsApp
            #from engine.command import takecommand, speak

            mobile_no, name = findContact(query)

            if mobile_no == 0:
                return

            if "video" in query:
                whatsApp(mobile_no, "", "video", name)

            elif "call" in query:
                whatsApp(mobile_no, "", "call", name)

            elif "message" in query:
                speak("What message should I send?")
                msg = takecommand()
                whatsApp(mobile_no, msg, "message", name)

        elif "open" in query:
            print("➡️ Open command")
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            print("➡️ YouTube command")
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif any(word in query for word in ["volume", "brightness", "shutdown", "restart", "mute"]):
            print("➡️ System control")
            from engine.features import systemControl
            systemControl(query)

        else:
            print("➡️ Going to chatbot")   # 👈 IMPORTANT
            from engine.features import chatBot
            chatBot(query)

    except Exception as e:
        print("❌ Error:", e)

    eel.ShowHood()