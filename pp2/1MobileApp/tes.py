# Kivy Simple Cool App
# Features:
# - Gradient-like background
# - Counter with animation feel
# - Button interactions
# - Clean UI

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.core.window import Window

Window.clearcolor = (0.08, 0.08, 0.12, 1)

class MainApp(App):
    def build(self):
        self.counter = 0

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = Label(
            text=f"[b]{self.counter}[/b]",
            markup=True,
            font_size=72
        )

        btn_add = Button(
            text="Tambah",
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 1, 1)
        )

        btn_reset = Button(
            text="Reset",
            size_hint=(1, 0.3),
            background_color=(1, 0.3, 0.3, 1)
        )

        btn_add.bind(on_press=self.increment)
        btn_reset.bind(on_press=self.reset)

        layout.add_widget(self.label)
        layout.add_widget(btn_add)
        layout.add_widget(btn_reset)

        return layout

    def animate_label(self):
        anim = Animation(font_size=90, duration=0.1) + Animation(font_size=72, duration=0.1)
        anim.start(self.label)

    def increment(self, instance):
        self.counter += 1
        self.label.text = f"[b]{self.counter}[/b]"
        self.animate_label()

    def reset(self, instance):
        self.counter = 0
        self.label.text = f"[b]{self.counter}[/b]"
        self.animate_label()

if __name__ == '__main__':
    MainApp().run()
