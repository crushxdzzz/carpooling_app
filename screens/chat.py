# screens/chat.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        btn_back = Button(
            text='Назад',
            size_hint=(0.2, 0.1),
            pos_hint={'top': 1, 'left': 1},
            background_color=(0.5, 0.5, 0.5, 1),
            font_size=16
        )
        btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(btn_back)
        
        self.chat_log = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.chat_log.bind(minimum_height=self.chat_log.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.chat_log)
        self.layout.add_widget(scroll)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.message_input = TextInput(hint_text='Введите сообщение', multiline=False)
        btn_send = Button(text='Отправить', size_hint_x=0.3)
        btn_send.bind(on_press=self.send_message)
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(btn_send)
        
        self.layout.add_widget(input_layout)
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint_y=None, height=30)
        self.layout.add_widget(self.error_label)
        
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        if not app.auth.current_user or not app.current_chat_id:
            self.error_label.text = 'Ошибка: пользователь или собеседник не выбран!'
            self.chat_log.clear_widgets()
            return
        
        self.chat_log.clear_widgets()
        messages = app.chat.get_messages(app.auth.current_user.id, app.current_chat_id)
        for msg in messages:
            sender = app.db.get_user_by_id(msg.sender_id)
            sender_name = sender.name if sender else f"Пользователь {msg.sender_id}"
            text = f"{sender_name}: {msg.text} ({msg.time})"
            self.chat_log.add_widget(Label(text=text, size_hint_y=None, height=40))

    def send_message(self, instance):
        app = App.get_running_app()
        if not app.auth.current_user or not app.current_chat_id:
            self.error_label.text = 'Ошибка: пользователь или собеседник не выбран!'
            return
        
        message = self.message_input.text.strip()
        if not message:
            self.error_label.text = 'Введите сообщение!'
            return
        
        app.chat.send_message(app.auth.current_user.id, app.current_chat_id, message)
        self.message_input.text = ''
        self.error_label.text = ''
        self.on_enter()

    def go_back(self, instance):
        self.manager.current = 'main_menu'