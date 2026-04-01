import os
import re
import sqlite3
import struct
import time
from urllib import response
import webbrowser

from playsound import playsound
import eel
import pyaudio
from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assisstant sound function
import pywhatkit as kit
import pvporcupine

import subprocess
import pyautogui
from urllib.parse import quote
import screen_brightness_control as sbc

waiting_for = None
# import time
# time.sleep(1)
# from engine.command import takecommand 
# import hugchat
# from google import genai
# from engine.config import GEMINI_API_KEY

# client = genai.Client(api_key=GEMINI_API_KEY)

# from google import genai
# from engine.config import GEMINI_API_KEY
# client = genai.Client(api_key=GEMINI_API_KEY)

# from openai import OpenAI
# from engine.config import OPENAI_API_KEY
# print("API:", OPENAI_API_KEY)

# client = OpenAI(api_key=OPENAI_API_KEY)

# # 👉 MEMORY LIST (GLOBAL)
# messages = [
#     {"role": "system", "content": "You are a smart voice assistant named Voca."}
# ]
from hugchat import hugchat
#chatBot = None
chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
# chatbot.new_conversation()

from engine.helper import extract_yt_term
def chat_response(text):
    return "You said: " + text

con = sqlite3.connect("voca.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
     music_dir = os.path.abspath("www/assets/audio/start_sound.mp3")
     playsound(music_dir)


# def openCommand(query):
#     query = query.lower()
#     query = query.replace("voca", "").replace("open", "").strip()

#     print("Opening:", query)

#     if query != "":
#         try:
#         #     if "whatsapp" in query:
#         #         speak("Opening WhatsApp")

#         #         # try:
#         #         #     import os
#         #         #     os.system("start whatsapp:")
#         #         # except:
#         #         import webbrowser
#         #         webbrowser.open("https://web.whatsapp.com")
#         #         return
#     #     # 👉 WHATSAPP FIX (ADD THIS BLOCK)
#             # if "whatsapp" in query:
#             #     speak("Opening WhatsApp")
#             #     subprocess.run(
#             #         '5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App',
#             #         shell=True
#             #     )
#             #     return

#         #     # Existing DB logic (leave as it is)
#             cursor.execute('SELECT path FROM sys_command WHERE name=?', (query,))
#             results = cursor.fetchall()

#             if results:
#                 speak("Opening " + query)
#                 os.startfile(results[0][0])

#             else:
#                 cursor.execute('SELECT url FROM web_command WHERE name=?', (query,))
#                 results = cursor.fetchall()

#                 if results:
#                     speak("Opening " + query)
#                     webbrowser.open(results[0][0])

#                 else:
#                     speak("Opening " + query)
#                     os.system('start ' + query)

#         except Exception as e:
#             print("Error:", e)
#             speak("Something went wrong")

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()

    if "whatsapp" in query:
        speak("Opening WhatsApp")
        os.system('explorer shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App')
        return

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except Exception as e:
            print("Error:", e)
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa","voca"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# FIXED CONTACT SEARCH
def findContact(query):
    words_to_remove = [
        ASSISTANT_NAME, 'make', 'a', 'to', 'phone',
        'call', 'send', 'message', 'whatsapp', 'video'
    ]

    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()

        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
            ('%' + query + '%', query + '%')
        )

        results = cursor.fetchall()

        if not results:   # FIXED
            speak("Contact not found")
            return 0, 0

        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query

    except Exception as e:
        print("Error:", e)
        speak('not exist in contacts')
        return 0, 0


# FIXED WHATSAPP FUNCTION
# FIXED WHATSAPP FUNCTION
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        jarvis_message = "message send successfully to " + name

        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(8)

        pyautogui.press("enter")
        speak(jarvis_message)
        return


    # NEW LOGIC FOR CALL / VIDEO (NO DEEP LINK)

    subprocess.run('start whatsapp:', shell=True)
    time.sleep(12)#(8)

    # Open search
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)

    # Type name
    pyautogui.write(name)
    time.sleep(2)

    # Select first result
    pyautogui.press('down')#('down')
    pyautogui.press('enter')#('enter')
    time.sleep(3)

    # # Click call button
    # pyautogui.click(1461, 234)
    # time.sleep(2)

    # if flag == "call":
    #     pyautogui.click(1181, 369)
    #     speak("calling to " + name)

# Open chat already done

# Move cursor safely to top right (approx call area)
    screenWidth, screenHeight = pyautogui.size()

# Click near top right (call icon area)
    pyautogui.click(screenWidth - 100, 100)
    time.sleep(2)

    if flag == "call":
        pyautogui.press('tab', presses=5)
        pyautogui.press('enter')
        speak("calling to " + name)

    elif flag == "video":
        pyautogui.press('tab', presses=6)
        pyautogui.press('enter')
        speak("starting video call with " + name)

    
#chatbot
def chatBot(query):
    global chatbot
    global waiting_for

    query = query.lower()
    print("🔥 CHATBOT CALLED:", query)

    # ✅ HANDLE FOLLOW-UP RESPONSE
    if waiting_for == "music":
        waiting_for = None

        if "yes" in query:
            speak("Playing something on YouTube")
            import pywhatkit as kit
            kit.playonyt("trending songs")
        else:
            speak("Okay, no problem")
        return

    # if waiting_for == "relax":
    #     waiting_for = None

    if "bored" in query:
        waiting_for = "music"
        speak("Should I play something for you?")
        return


        #     speak("Playing something relaxing")
        #     import pywhatkit as kit
        #     kit.playonyt("relaxing music")
        # else:
        #     speak("Alright, I am here for you")
        # return

    # ✅ TRIGGERS
    # if "bored" in query:
    #     waiting_for = "music"
    #     speak("Should I play something for you?")
    #     return

    # if "sad" in query:
    #     waiting_for = "relax"
    #     speak("I am here for you. Do you want me to play something relaxing?")
    #     return

    # ✅ MAIN HUGCHAT CALL
    try:
        response = chatbot.chat(query)
        reply = str(response)

        print("Reply:", reply)

        if reply.strip() == "":
            raise Exception("Empty response")

        speak(reply)
        return reply

    except Exception as e:
        print("❌ Hugchat Error:", e)

        # 🔥 FALLBACK (VERY IMPORTANT)
        speak("Using backup AI")

        from google import genai
        from engine.config import GEMINI_API_KEY

        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-1.5-flash-001",
            contents=query
        )

        speak(response.text)
        return response.text    
# def chatBot(query):

#     global waiting_for
#     global chatbot
#     print("🔥 CHATBOT CALLED")
    
#     try:
#         response = chatbot.chat(query)
#         reply = str(response)

#         print("Reply:", reply)

#         if reply.strip() == "":
#             speak("No response received")
#         else:
#             speak(reply)

#     except Exception as e:
#         print("Hugchat Error:", e)
#         speak("Something went wrong")
#         # 🔥 FALLBACK (IMPORTANT)
#     speak("Using backup AI")

#     response = client.models.generate_content(
#         model="gemini-1.5-flash-001",
#         contents=query
#     )

#     speak(response.text)

        # print("User:", query)

    #     response = chatbot.chat(query)

    #     print("Raw response:", response)

    #     # 🔥 IMPORTANT FIX
    #     reply = str(response)

    #     print("Final reply:", reply)

    #     if reply.strip() == "":
    #         speak("Sorry, I didn't get any response")
    #     else:
    #         speak(reply)

    #     return reply

    # except Exception as e:
    #     print("Hugchat Error:", e)
    #     speak("Sorry, something went wrong")

    # # ✅ HANDLE FOLLOW-UP RESPONSE
    # if waiting_for == "music":
    #     waiting_for = None

    #     if any(word in query for word in ["yes", "yeah", "yup", "sure", "ok", "okay"]):
    #         speak("Playing something on YouTube")
    #         import pywhatkit as kit
    #         kit.playonyt("trending songs")
    #     else:
    #         speak("Okay, no problem")
    #     return

    # if waiting_for == "relax":
    #     waiting_for = None

    #     if any(word in query for word in ["yes", "yeah", "yup", "sure", "ok", "okay"]):
    #         speak("Playing something relaxing")
    #         import pywhatkit as kit
    #         kit.playonyt("relaxing music")
    #     else:
    #         speak("Alright, I am here for you")
    #     return

    # # ✅ TRIGGERS
    # if "bored" in query:
    #     waiting_for = "music"
    #     speak("Should I play something for you?")
    #     return

    # if "sad" in query:
    #     waiting_for = "relax"
    #     speak("I am here for you. Do you want me to play something relaxing?")
    #     # return

    # # ✅ NORMAL AI
    # try:
    #     response = client.models.generate_content(
    #         model="gemini-1.5-flash-001",
    #         contents=query
    #     )

    #     reply = response.text
    #     speak(reply)

    # except Exception as e:
    #     print("Error:", e)
    #     speak("Sorry, I am unable to respond")

# def chatBot(query):
    # try:
    #     print("User:", query)

    #             # 👉 SMART INTENT HANDLING
    #     if "i am bored" in query or "bored" in query:
            
    #         speak("Should I play something for you?")
    #         # import time
    #         # time.sleep(1)
    #         # from engine.command import takecommand
            
    #         print("Listening for confirmation...")
    #         ans = takecommand()
    #         print("user response:", ans)

    #         eel.ShowHood()

    #         if any(word in ans for word in ["yes", "yeah", "yup", "sure", "ok", "okay"]):
    #             speak("Playing something on YouTube")
    #             import pywhatkit as kit
    #             kit.playonyt("trending songs")
    #             return
    #         elif any(word in ans for word in ["no", "cancel"]):
    #             speak("Okay, no problem")
    #             return

    #         else:
    #             speak("I didn't understand, but I will not play anything")
    #             return

    #     if "i am sad" in query:
    #         speak("I am here for you. Do you want me to play something relaxing?")
    #         return


    #     response = client.models.generate_content(
    #         model="gemini-1.5-flash-001",   # ✅ correct
    #         contents=query
    #     )

    #     reply = response.text

    #     print("AI:", reply)
    #     speak(reply)

    #     return reply

    # except Exception as e:
    #     print("❌ Gemini Error:", e)
    #     speak("Sorry, I am unable to respond")


# def chatBot(query):
#     try:
#         print("User:", query)

#         response = client.models.generate_content(
#             model="gemini-1.5-pro",
#             contents=query
#         )

#         reply = response.text

#         print("AI:", reply)
#         speak(reply)

#         return reply

#     except Exception as e:
#         print("❌ Gemini Error:", e)
#         speak("Sorry, I am unable to respond")



# chatbot = None
# def chatBot(query):
#     try:
#         messages.append({"role": "user", "content": query})
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",   # fast + cheap
#             messages=[
#                 {"role": "system", "content": "You are a smart voice assistant named Voca."},
#                 {"role": "user", "content": query}
#             ],
#             max_tokens=150
#         )

#         reply = response.choices[0].message.content
#         print("AI:", reply)

#         speak(reply)
#         return reply

#     except Exception as e:
#         print("Error:", e)
#         speak("Sorry, I am unable to respond right now")
#         return "error"



# def init_chatbot():
#     global chatbot
#     if chatbot is None:
#         from hugchat import hugchat
#         chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")

# def chatBot(query):
#     init_chatbot()
#     response = chatbot.chat(query)
#     speak(response)

# # def chatBot(query):
# #     user_input = query.lower()
# #     chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
# #     id = chatbot.new_conversation()
# #     chatbot.change_conversation(id)
# #     response = chatbot.chat(user_input)
#     print(response)
#     # speak(response)
    #  return response


# SYSTEM SETTINGS
def systemControl(query):
    query = query.lower()

    # 🔊 Volume Control
    if "volume up" in query or "increase volume" in query:
        pyautogui.press("volumeup")
        speak("Volume increased")

    elif "volume down" in query or "decrease volume" in query:
        pyautogui.press("volumedown")
        speak("Volume decreased")

    elif "mute" in query:
        pyautogui.press("volumemute")
        speak("Muted")

# 💡 Brightness Control
    elif "brightness up" in query:
        sbc.set_brightness(100)
        speak("Brightness increased")

    elif "brightness down" in query:
        sbc.set_brightness(30)
        speak("Brightness decreased")

    # 🖥 System Control
    elif "shutdown" in query:
        speak("Are you sure you want to shutdown?")

        from engine.command import takecommand
        response = takecommand()

        if "yes" in response:
            speak("Shutting down system")
            os.system("shutdown /s /t 1")
        else:
            speak("Shutdown cancelled")

    elif "restart" in query:
        speak("Do you want to restart the system?")

        from engine.command import takecommand
        response = takecommand()

        if "yes" in response:
            speak("Restarting system")
            os.system("shutdown /r /t 1")
        else:
            speak("Restart cancelled")