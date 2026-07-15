import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

FILE_NAME = "words.json"


class LanguageLearningApp(App):

    def build(self):
        self.title = "Language Learning App"

        self.words = self.load_words()

        if not self.words:
            self.words = [
                {"english": "Hello", "meaning": "Namaste"},
                {"english": "Water", "meaning": "Pani"},
                {"english": "Book", "meaning": "Kitab"},
                {"english": "School", "meaning": "Vidyalaya"},
                {"english": "Thank You", "meaning": "Dhanyavaad"}
            ]
            self.save_words()

        self.index = 0

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.word_label = Label(font_size=28)
        self.meaning_label = Label(font_size=22)

        layout.add_widget(self.word_label)
        layout.add_widget(self.meaning_label)

        add_btn = Button(text="Add Word")
        delete_btn = Button(text="Delete Word")
        prev_btn = Button(text="Previous")
        next_btn = Button(text="Next")

        add_btn.bind(on_press=self.add_word)
        delete_btn.bind(on_press=self.delete_word)
        prev_btn.bind(on_press=self.previous_word)
        next_btn.bind(on_press=self.next_word)

        layout.add_widget(add_btn)
        layout.add_widget(delete_btn)
        layout.add_widget(prev_btn)
        layout.add_widget(next_btn)

        self.update_word()

        return layout

    def load_words(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        return []

    def save_words(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.words, f, indent=4)

    def update_word(self):
        if self.words:
            self.word_label.text = "Word: " + self.words[self.index]["english"]
            self.meaning_label.text = "Meaning: " + self.words[self.index]["meaning"]
        else:
            self.word_label.text = "No Words"
            self.meaning_label.text = ""

    def add_word(self, instance):

        english = TextInput(hint_text="English Word")
        meaning = TextInput(hint_text="Meaning")

        box = BoxLayout(
            orientation="vertical",
            spacing=10
        )

        box.add_widget(english)
        box.add_widget(meaning)

        save_btn = Button(text="Save")
        box.add_widget(save_btn)

        popup = Popup(
            title="Add Word",
            content=box,
            size_hint=(0.8, 0.6)
        )

        def save_data(btn):
            if not english.text or not meaning.text:
                return

            self.words.append({
                "english": english.text,
                "meaning": meaning.text
            })

            self.save_words()
            self.index = len(self.words) - 1
            self.update_word()
            popup.dismiss()

        save_btn.bind(on_press=save_data)
        popup.open()

    def delete_word(self, instance):
        if not self.words:
            return

        self.words.pop(self.index)

        if self.index >= len(self.words):
            self.index = 0

        self.save_words()
        self.update_word()

    def next_word(self, instance):
        if self.words:
            self.index = (self.index + 1) % len(self.words)
            self.update_word()

    def previous_word(self, instance):
        if self.words:
            self.index = (self.index - 1) % len(self.words)
            self.update_word()


LanguageLearningApp().run()