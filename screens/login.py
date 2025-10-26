# screens/login.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        btn_back = Button(
            text='Назад',
            size_hint=(0.2, 0.1),
            pos_hint={'top': 1, 'left': 1},
            background_color=(0.5, 0.5, 0.5, 1),
            font_size=16
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'welcome'))
        layout.add_widget(btn_back)

        layout.add_widget(Label(text='Вход', font_size=20, bold=True))

        
        self.phone_input = TextInput(hint_text='Телефон')
        self.password_input = TextInput(hint_text='Пароль', password=True)
        layout.add_widget(self.phone_input)
        layout.add_widget(self.password_input)
        
        btn_login = Button(text='Войти')
        btn_login.bind(on_press=self.login)
        layout.add_widget(btn_login)
        
        self.error_label = Label(text='', color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)
        
        self.add_widget(layout)

    def login(self, instance):
        app = App.get_running_app()
        phone = self.phone_input.text.strip()
        password = self.password_input.text.strip()
        
        if not phone or not password:
            self.error_label.text = 'Введите телефон и пароль!'
            return
        
        if app.auth.login(phone, password):
            self.manager.current = 'main_menu'
            self.error_label.text = ''
        else:
            self.error_label.text = 'Неверный телефон или пароль!'