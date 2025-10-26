# screens/search_trips.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle


class SearchTripsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Основной вертикальный layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Кнопка "Назад"
        btn_back = Button(
            text='Назад',
            size_hint=(0.3, None),
            height=dp(40),
            background_color=(0.6, 0.6, 0.6, 1)
        )
        btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(btn_back)

        # Заголовок
        self.layout.add_widget(Label(
            text='Доступные поездки',
            font_size=22,
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        # Прокручиваемая область
        self.scroll = ScrollView(size_hint=(1, 1))
        self.trips_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.trips_box.bind(minimum_height=self.trips_box.setter('height'))
        self.scroll.add_widget(self.trips_box)
        self.layout.add_widget(self.scroll)

        # Текст ошибок
        self.error_label = Label(
            text='',
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=dp(30)
        )
        self.layout.add_widget(self.error_label)

        self.add_widget(self.layout)

    def on_enter(self):
        """При входе на экран загружаем поездки."""
        app = App.get_running_app()
        if not app.auth.current_user:
            self.error_label.text = 'Ошибка: пользователь не авторизован!'
            self.manager.current = 'welcome'
            return

        trips = app.db.get_all_trips()
        print(f"Found {len(trips)} trips")

        # Очистим старые элементы
        self.trips_box.clear_widgets()

        if not trips:
            self.error_label.text = 'Поездки не найдены.'
            return

        self.error_label.text = ''

        theme = getattr(app, 'theme', 'light')
        if theme == 'dark':
            bg_color = (0.15, 0.15, 0.15, 1)  # тёмно-серый фон карточек
            text_color = (1, 1, 1, 1)          # белый текст
        else:
            bg_color = (0.4, 0.4, 0.4, 1)    # тёмно-серый фон карточек
            text_color = (0, 0, 0, 1)          # чёрный текст

        for trip in trips:
            display_route = trip.route.replace('-', ' - ').title()

            # Карточка поездки
            trip_card = BoxLayout(
                orientation='vertical',
                padding=10,
                spacing=5,
                size_hint_y=None,
                height=dp(120)
            )

            # Добавляем фон карточке
            with trip_card.canvas.before:
                Color(0.2, 0.2, 0.2, 0.2)
                trip_card.bg_rect = RoundedRectangle(radius=[10], pos=trip_card.pos, size=trip_card.size)
            trip_card.bind(pos=self.update_bg, size=self.update_bg)

            # Информация о поездке
            info_label = Label(
                text=f"[b]{display_route}[/b]\nДата: {trip.date} | Время: {trip.time}\nЦена: {trip.price} руб. | Мест: {trip.seats}",
                markup=True,
                halign='left',
                valign='middle',
                size_hint_y=None,
                height=dp(70),
                color=text_color
            )
            info_label.bind(size=lambda inst, val: inst.setter('text_size')(inst, val))

            # Кнопка "Выбрать"
            btn_select = Button(
                text="Выбрать поездку",
                size_hint_y=None,
                height=dp(35),
                background_color=(0.3, 0.5, 0.8, 1)
            )
            btn_select.trip_id = trip.id
            btn_select.bind(on_press=self.select_trip)

            # Добавляем всё в карточку
            trip_card.add_widget(info_label)
            trip_card.add_widget(btn_select)

            # Добавляем карточку в список
            self.trips_box.add_widget(trip_card)

    def update_bg(self, instance, value):
        """Обновление позиции и размера фона."""
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size

    def select_trip(self, instance):
        """Действие при выборе поездки."""
        app = App.get_running_app()
        app.current_trip_id = instance.trip_id
        print(f"Selected trip_id: {app.current_trip_id}")
        self.manager.current = 'trip_details'

    def go_back(self, instance):
        """Возврат в главное меню."""
        self.manager.current = 'main_menu'
