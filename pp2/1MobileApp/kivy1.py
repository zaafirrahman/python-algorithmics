# # 1 Membuat dan menjalankan aplikasi
# from kivy.app import App

# class MyApp(App):
#    pass
# app = MyApp()
# app.run()


# # 2 Tampilan di layar. Metode build
# from kivy.app import App
# from kivy.uix.label import Label

# class MyApp(App):
#     def build(self):
#         return Label(text="Hello Kivy!")

# app = MyApp()
# app.run()


# # 3 Program tata letak. Metode add_widget
# from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.boxlayout import BoxLayout

# class MyApp(App):
#     def build(self):
#         layout = BoxLayout(orientation='vertical')

#         label1 = Label(text="Hello")
#         label2 = Label(text="Kivy")

#         layout.add_widget(label1)
#         layout.add_widget(label2)

#         return layout

# app = MyApp()
# app.run()


# # 4 Event & Handling
# from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout

# class MyApp(App):
#     def build(self):
#         self.label = Label(text="Belum diklik")
#         button = Button(text="Klik aku")

#         button.bind(on_press=self.on_button_click)

#         layout = BoxLayout(orientation='vertical')
#         layout.add_widget(self.label)
#         layout.add_widget(button)

#         return layout

#     def on_button_click(self, instance):
#         self.label.text = "Tombol diklik!"

# app = MyApp()
# app.run()


# 5 Beralih Layar (ScreenManager)
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        btn = Button(text="Ke Screen 2")
        btn.bind(on_press=self.go_to_screen2)

        layout.add_widget(btn)
        self.add_widget(layout)

    def go_to_screen2(self, instance):
        self.manager.current = "screen2"

class Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        btn = Button(text="Balik ke Screen 1")
        btn.bind(on_press=self.go_to_screen1)

        layout.add_widget(btn)
        self.add_widget(layout)

    def go_to_screen1(self, instance):
        self.manager.current = "screen1"

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Screen1(name="screen1"))
        sm.add_widget(Screen2(name="screen2"))
        return sm

app = MyApp()
app.run()
