# screens/welcome.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Добро пожаловать в приложение Карпулинг'))
        btn_login = Button(text='Войти')
        btn_login.bind(on_press=self.go_to_login)
        layout.add_widget(btn_login)
        btn_register = Button(text='Зарегистрироваться')
        btn_register.bind(on_press=self.go_to_register)
        layout.add_widget(btn_register)
        self.add_widget(layout)

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def go_to_register(self, instance):
        self.manager.current = 'register'