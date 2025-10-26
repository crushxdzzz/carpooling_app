# screens/booking.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.app import App

class BookingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)
        self.trip = None
        self.spinner = None

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
        
        self.layout.add_widget(Label(text='Бронирование поездки', font_size=20, bold=True))
        
        if not app.auth.current_user or app.auth.current_user.role.lower() != 'пассажир':
            self.layout.add_widget(Label(text='Только пассажиры могут бронировать поездки!', color=(1, 0, 0, 1)))
            return
        
        if not app.current_trip_id:
            self.layout.add_widget(Label(text='Ошибка: поездка не выбрана!', color=(1, 0, 0, 1)))
            return
        
        # Получаем данные поездки
        self.trip = app.db.get_trip(app.current_trip_id)
        if not self.trip:
            self.layout.add_widget(Label(text=f'Ошибка: поездка с ID {app.current_trip_id} не найдена в базе!', color=(1, 0, 0, 1)))
            return

        available = getattr(self.trip, 'seats', 0)


        if available <= 0:
            self.layout.add_widget(Label(text='Все места заняты. Бронирование невозможно!', color=(1, 0, 0, 1)))
            return
        
        self.layout.add_widget(Label(text=f'Доступно мест: {available}', font_size=16))
        self.spinner = Spinner(
            text='1',
            values=[str(i) for i in range(1, available + 1)],
            size_hint=(None, None),
            size=(120, 44),
            size_hint_y=None,
            height=44
        )
        self.layout.add_widget(self.spinner)

        self.layout.add_widget(Label(text=f'Маршрут: {self.trip.route}'))
        self.layout.add_widget(Label(text=f'Дата: {self.trip.date} | Время: {self.trip.time}'))
        self.layout.add_widget(Label(text=f'Цена: {self.trip.price} руб. | Мест: {self.trip.seats}'))
        
        btn_confirm = Button(text='Подтвердить бронирование')
        btn_confirm.bind(on_press=self.book)
        self.layout.add_widget(btn_confirm)
        
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint_y=None, height=30)
        self.layout.add_widget(self.error_label)

    def book(self, instance):
        app = App.get_running_app()

        if not self.trip:
            self.error_label.text = 'Ошибка: данные поездки не найдены!'
            return

        selected_seats = int(self.spinner.text)
        available = getattr(self.trip, 'seats', 0)

        if available <= 0:
            self.error_label.text = 'Нет свободных мест!'
            return

        if selected_seats > available:
            self.error_label.text = f'Доступно только {available} мест!'
            return

        # Вычисляем новое количество мест
        new_available = available - selected_seats

        # Обновляем поездку в базе
        app.db.update_trip_seats(self.trip.id, new_available)

        # Создаем бронирование
        app.db.add_booking(app.auth.current_user.id, self.trip.id, selected_seats)

        # Обновляем локальный объект
        self.trip.seats = new_available

        # Если мест больше нет — поездка "закрыта"
        if new_available <= 0:
        # Можно либо удалить поездку, либо скрыть из списка активных
            try:
                app.db.mark_trip_full(self.trip.id)  # см. ниже
            except Exception:
                pass

            self.error_label.color = (0, 1, 0, 1)
            self.error_label.text = f'Бронирование успешно! Поездка заполнена.'
        # возвращаем на главный экран
            self.manager.current = 'main_menu'
            return

        self.error_label.color = (0, 1, 0, 1)
        self.error_label.text = f'Бронирование успешно! ({selected_seats} мест)'

        # Возврат к главному экрану
        self.manager.current = 'main_menu'


    def go_back(self, instance):
        self.manager.current = 'main_menu'