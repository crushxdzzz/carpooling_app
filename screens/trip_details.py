# screens/trip_details.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class TripDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        self.layout.clear_widgets()
        
        btn_back = Button(
            text='Назад',
            size_hint=(0.2, 0.1),
            pos_hint={'top': 1, 'left': 1},
            background_color=(0.5, 0.5, 0.5, 1),
            font_size=16
        )
        btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(btn_back)
        
        self.layout.add_widget(Label(text='Детали поездки', font_size=20, bold=True))
        
        if not app.current_trip_id:
            self.layout.add_widget(Label(text='Ошибка: поездка не выбрана!', color=(1, 0, 0, 1)))
            return
        
        trip = app.db.get_trip(app.current_trip_id)
        if not trip:
            self.layout.add_widget(Label(text='Ошибка: поездка не найдена!', color=(1, 0, 0, 1)))
            return
        
        driver = app.db.get_user_by_id(trip.driver_id)
        self.layout.add_widget(Label(text=f'Маршрут: {trip.route}'))
        self.layout.add_widget(Label(text=f'Дата: {trip.date}'))
        self.layout.add_widget(Label(text=f'Время: {trip.time}'))
        self.layout.add_widget(Label(text=f'Цена: {trip.price} руб.'))
        self.layout.add_widget(Label(text=f'Свободных мест: {trip.seats}'))
        self.layout.add_widget(Label(text=f'Водитель: {driver.name}' if driver else 'Водитель не найден'))
        
        btn_book = Button(text='Забронировать')
        btn_book.bind(on_press=self.go_to_booking)
        self.layout.add_widget(btn_book)
        
        btn_chat = Button(text='Чат с водителем')
        btn_chat.bind(on_press=self.go_to_chat)
        self.layout.add_widget(btn_chat)

    def go_to_chat(self, instance):
        app = App.get_running_app()
        trip = app.db.get_trip(app.current_trip_id)
        if trip:
            app.current_chat_id = trip.driver_id
            self.manager.current = 'chat'

    def go_back(self, instance):
        self.manager.current = 'main_menu'

    def go_to_booking(self, instance):
        app = App.get_running_app()
        trip = app.db.get_trip(app.current_trip_id)
        if not trip:
            return

        # получаем экран бронирования
        booking_screen = self.manager.get_screen('booking')
        # передаём выбранную поездку на экран бронирования
        booking_screen.trip = trip
        # переключаем экран
        self.manager.current = 'booking'