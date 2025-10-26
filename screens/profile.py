# screens/profile.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        self.layout.clear_widgets()
        
        # Кнопка "Назад" из styles.kv
        btn_back = Button(
            text='Назад',
            size_hint=(0.2, 0.1),
            pos_hint={'top': 1, 'left': 1},
            background_color=(0.5, 0.5, 0.5, 1),
            font_size=16
        )
        btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(btn_back)
        
        self.layout.add_widget(Label(text='Профиль', font_size=20, bold=True))
        
        if not app.auth.current_user:
            self.layout.add_widget(Label(text='Ошибка: пользователь не авторизован!', color=(1, 0, 0, 1)))
            return
        
        user = app.auth.current_user
        self.layout.add_widget(Label(text=f'Имя: {user.name}'))
        self.layout.add_widget(Label(text=f'Телефон: {user.phone}'))
        self.layout.add_widget(Label(text=f'Роль: {user.role}'))
        self.layout.add_widget(Label(text=f'Рейтинг: {user.rating:.1f}'))
        
        self.name_input = TextInput(hint_text='Новое имя', text=user.name)
        btn_update_name = Button(text='Обновить имя')
        btn_update_name.bind(on_press=self.update_name)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(btn_update_name)
        
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint_y=None, height=30)
        self.layout.add_widget(self.error_label)

    def update_name(self, instance):
        app = App.get_running_app()
        new_name = self.name_input.text.strip()
        if not new_name:
            self.error_label.text = 'Введите новое имя!'
            return
        
        if app.db.get_user(new_name):
            self.error_label.text = 'Имя уже занято!'
            return
        
        app.db.update_user_name(app.auth.current_user.id, new_name)
        app.auth.current_user.name = new_name
        self.error_label.text = 'Имя обновлено!'
        self.on_enter()

    def go_back(self, instance):
        self.manager.current = 'main_menu'