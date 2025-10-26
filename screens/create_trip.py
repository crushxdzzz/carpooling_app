# screens/create_trip.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from screens.widgets import DatePicker, TimePicker
from datetime import datetime

class CreateTripScreen(Screen):
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
        
        self.layout.add_widget(Label(text='Создать поездку', font_size=20, bold=True))
        
        self.from_loc = TextInput(hint_text='Откуда')
        self.to_loc = TextInput(hint_text='Куда')
        self.date_label = Label(text='Дата: Не выбрана', size_hint_y=None, height=30)
        self.date_button = Button(
            text='Выбрать дату',
            size_hint=(0.3, 0.1),
            background_color=(0.4, 0.4, 0.8, 1)
        )
        self.date_button.bind(on_press=self.open_date_picker)
        self.time_label = Label(text='Время: Не выбрано', size_hint_y=None, height=30)
        self.time_button = Button(
            text='Выбрать время',
            size_hint=(0.3, 0.1),
            background_color=(0.4, 0.4, 0.8, 1)
        )
        self.time_button.bind(on_press=self.open_time_picker)
        self.price = TextInput(hint_text='Цена за место (руб.)')
        self.seats = TextInput(hint_text='Количество мест')
        
        self.layout.add_widget(self.from_loc)
        self.layout.add_widget(self.to_loc)
        self.layout.add_widget(self.date_label)
        self.layout.add_widget(self.date_button)
        self.layout.add_widget(self.time_label)
        self.layout.add_widget(self.time_button)
        self.layout.add_widget(self.price)
        self.layout.add_widget(self.seats)
        
        btn_create = Button(text='Создать')
        btn_create.bind(on_press=self.create)
        self.layout.add_widget(btn_create)
        
        self.error_label = Label(text='', color=(1, 0, 0, 1))
        self.layout.add_widget(self.error_label)
        
        self.add_widget(self.layout)
        self.selected_date = None
        self.selected_time = None

    def on_enter(self):
        app = App.get_running_app()
        if not app.auth.current_user:
            self.error_label.text = 'Ошибка: пользователь не авторизован!'
            self.manager.current = 'main_menu'
            return
        role = app.auth.current_user.role.lower().strip()
        print(f"User role: {role}")  # Отладочная информация
        if role != 'водитель':
            self.error_label.text = f'Только водители могут создавать поездки! Ваша роль: {role}'
            self.manager.current = 'main_menu'
            return
        self.error_label.text = ''  # Очищаем ошибку, если всё в порядке

    def open_date_picker(self, instance):
        date_picker = DatePicker(callback=self.set_date)
        date_picker.open()

    def set_date(self, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            self.selected_date = date
            self.date_label.text = f'Дата: {date}'
        except ValueError:
            self.error_label.text = 'Неверный формат даты!'

    def open_time_picker(self, instance):
        time_picker = TimePicker(callback=self.set_time)
        time_picker.open()

    def set_time(self, time):
        try:
            datetime.strptime(time, '%H:%M')
            self.selected_time = time
            self.time_label.text = f'Время: {time}'
        except ValueError:
            self.error_label.text = 'Неверный формат времени!'

    # screens/create_trip.py (фрагмент)
    def create(self, instance):
        app = App.get_running_app()
        from_loc = self.from_loc.text.strip()
        to_loc = self.to_loc.text.strip()
        date = self.selected_date
        time = self.selected_time
        price = self.price.text.strip()
        seats = self.seats.text.strip()
        
        if not all([from_loc, to_loc, date, time, price, seats]):
            self.error_label.text = 'Заполните все поля!'
            return
        
        try:
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(time, '%H:%M')
        except ValueError:
            self.error_label.text = 'Неверный формат даты или времени!'
            return
        
        try:
            price = float(price)
            seats = int(seats)
            if price < 0 or seats <= 0:
                self.error_label.text = 'Цена и количество мест должны быть положительными!'
                return
        except ValueError:
            self.error_label.text = 'Цена и количество мест должны быть числами!'
            return
        
        app.db.create_trip(
            driver_id=app.auth.current_user.id,
            route=f"{from_loc}-{to_loc}",
            date=date,
            time=time,
            price=price,
            seats=seats
        )
        self.error_label.text = 'Поездка создана!'
        self.manager.current = 'main_menu'

    def go_back(self, instance):
        self.manager.current = 'main_menu'