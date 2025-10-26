# screens/my_trips.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class TripCard(BoxLayout):
    """Карточка одной поездки"""
    def __init__(self, trip_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(140)
        self.padding = [10, 10]
        self.spacing = 5

        # Цветная рамка для наглядности
        with self.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(0.2, 0.2, 0.2, 0.2)
            self.bg_rect = RoundedRectangle(radius=[10], pos=self.pos, size=self.size)
            self.bind(pos=self._update_rect, size=self._update_rect)

        # Информация о поездке
        self.add_widget(Label(
            text=f"Маршрут: {trip_data.get('route', 'N/A')}",
            halign="left", valign="middle", size_hint_y=None, height=25
        ))
        self.add_widget(Label(
            text=f"Дата: {trip_data.get('date', 'N/A')}  |  Время: {trip_data.get('time', 'N/A')}",
            halign="left", valign="middle", size_hint_y=None, height=25
        ))
        self.add_widget(Label(
            text=f"Цена: {trip_data.get('price', 'N/A')} руб.",
            halign="left", valign="middle", size_hint_y=None, height=25
        ))

        # Кнопка "Подробнее"
        btn_details = Button(
            text="Подробнее",
            size_hint_y=None,
            height=dp(40),
            background_color=(0.3, 0.5, 0.8, 1)
        )
        self.add_widget(btn_details)

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class MyTripsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Главный layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Заголовок
        self.title_label = Label(
            text='Мои поездки',
            font_size=22,
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )
        self.layout.add_widget(self.title_label)

        # Прокручиваемая область
        scroll_view = ScrollView()
        self.trips_container = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=5)
        self.trips_container.bind(minimum_height=self.trips_container.setter('height'))
        scroll_view.add_widget(self.trips_container)
        self.layout.add_widget(scroll_view)

        # Кнопка "Назад"
        btn_back = Button(
            text='Назад',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        self.trips_container.clear_widgets()

        # Пример данных (временно)
        trips = app.db.get_user_trips(app.auth.current_user.id)
        print("Загруженные поездки:", trips)

        # Если база возвращает объекты, преобразуем их в словари
        data_list = []
        if trips:
            for t in trips:
                data_list.append({
                    'route': getattr(t, 'route', 'N/A'),
                    'date': getattr(t, 'date', 'N/A'),
                    'time': getattr(t, 'time', 'N/A'),
                    'price': getattr(t, 'price', 'N/A'),
                    'seats': getattr(t, 'seats', 'N/A'),
                })
        else:
            data_list = [
                {'route': 'Данных нет', 'date': '', 'time': '', 'price': '', 'seats': ''}
            ]

        # Создаём карточки
        for trip in data_list:
            self.trips_container.add_widget(TripCard(trip))

    def go_back(self, instance):
        self.manager.current = 'main_menu'