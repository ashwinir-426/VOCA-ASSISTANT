import pywhatkit as kit
import pyautogui
import time

CONTACTS = {
    "kevin": "+919138214118"
}

print("WhatsApp CLI ready")
print("Example:")
print("send message to kevin hello\n")

while True:
    cmd = input(">>> ").lower().strip()

    if not cmd:
        continue

    if cmd == "exit":
        break

    if cmd.startswith("send message to"):
        try:
            rest = cmd.replace("send message to", "").strip()
            name, message = rest.split(" ", 1)

            phone = CONTACTS.get(name)
            if not phone:
                print("contact not found")
                continue

            print("📨 opening whatsapp...")

            kit.sendwhatmsg_instantly(
                phone,
                message,
                wait_time=15,   # IMPORTANT
                tab_close=False
            )

            # wait for chat to fully load
            time.sleep(8)

            #  FORCE SEND
            pyautogui.press("enter")

            print(" message SENT (confirmed)")

        except Exception as e:
            print("error:", e)
    else:
        print(" invalid command")
