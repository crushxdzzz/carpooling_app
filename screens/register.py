# screens/register.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.app import App

class RegisterScreen(Screen):
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

        layout.add_widget(Label(text='Регистрация', font_size=20, bold=True))
        
        self.name_input = TextInput(hint_text='Имя')
        self.phone_input = TextInput(hint_text='Телефон')
        self.password_input = TextInput(hint_text='Пароль', password=True)
        self.role_input = Spinner(text='Роль', values=('Пассажир', 'Водитель'))
        layout.add_widget(self.name_input)
        layout.add_widget(self.phone_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.role_input)
        
        btn_register = Button(text='Зарегистрироваться')
        btn_register.bind(on_press=self.register)
        layout.add_widget(btn_register)
        
        self.error_label = Label(text='', color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)
        
        self.add_widget(layout)

    def register(self, instance):
        app = App.get_running_app()
        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()
        password = self.password_input.text.strip()
        role = self.role_input.text.lower()  # Приводим роль к нижнему регистру
        
        if not name or not phone or not password or not role:
            self.error_label.text = 'Заполните все поля!'
            return
        
        if app.db.get_user(name):
            self.error_label.text = 'Имя уже занято!'
            return
        
        if app.db.get_user_by_phone(phone):
            self.error_label.text = 'Телефон уже зарегистрирован!'
            return
        
        app.db.create_user(name, phone, password, role)
        self.error_label.text = 'Регистрация успешна! Войдите в систему.'
        self.manager.current = 'login'