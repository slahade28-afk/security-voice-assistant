
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from datetime import datetime

KV = """
BoxLayout:
    orientation: "vertical"
    padding: 20
    spacing: 15

    Label:
        text: "[b]SECURITY VOICE ASSISTANT[/b]"
        markup: True
        font_size: "24sp"

    Label:
        id: status
        text: "Namaskar! Mi tumcha Security Assistant aahe."
        font_size: "18sp"
        halign: "center"
        valign: "middle"
        text_size: self.width, None

    Button:
        text: "HELLO"
        on_release: app.respond("hello")

    Button:
        text: "SECURITY TIPS"
        on_release: app.respond("security")

    Button:
        text: "TIME"
        on_release: app.respond("time")

    Button:
        text: "ABOUT APP"
        on_release: app.respond("about")
"""


class SecurityAssistant(App):
    def build(self):
        self.title = "Security Assistant"
        Window.clearcolor = (0.08, 0.12, 0.18, 1)
        return Builder.load_string(KV)

    def respond(self, command):
        if command == "hello":
            message = "Namaskar! Mi tumchi madat karen."
        elif command == "security":
            message = (
                "Phone surakshit theva. "
                "Anolakhi links ughadu naka. "
                "OTP ani password konalahi sangu naka."
            )
        elif command == "time":
            message = "Aata vel aahe " + datetime.now().strftime("%I:%M %p")
        elif command == "about":
            message = "Ha tumcha Security Assistant aahe."
        else:
            message = "Command samajli nahi."

        self.root.ids.status.text = message
        self.speak(message)

    def speak(self, message):
        if platform == "android":
            try:
                from jnius import autoclass

                activity = autoclass(
                    "org.kivy.android.PythonActivity"
                ).mActivity
                TextToSpeech = autoclass(
                    "android.speech.tts.TextToSpeech"
                )
                Locale = autoclass("java.util.Locale")

                if not hasattr(self, "tts"):
                    self.tts = TextToSpeech(activity, None)

                self.tts.setLanguage(Locale("mr", "IN"))
                self.tts.speak(
                    message, 0, None, "security_message"
                )
            except Exception as error:
                print("Voice error:", error)
        else:
            print("Assistant:", message)


SecurityAssistant().run()

