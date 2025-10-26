# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
from themes import THEMES

# Подключаем styles.kv
Builder.load_file('styles.kv')

# Настройка размера окна (для тестирования на ПК)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# Импорт экранов
from screens.welcome import WelcomeScreen
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.main_menu import MainMenuScreen
from screens.search_trips import SearchTripsScreen
from screens.create_trip import CreateTripScreen
from screens.trip_details import TripDetailsScreen
from screens.booking import BookingScreen
from screens.chat import ChatScreen
from screens.profile import ProfileScreen
from screens.my_trips import MyTripsScreen
from screens.settings import SettingsScreen
from screens.splash_screen import SplashScreen

# Импорт сервисов
from services.auth import AuthService
from services.database import DatabaseService
from services.chat import ChatService
from services.maps import MapsService

class CarpoolingApp(App):
    current_trip_id = None  # Для хранения ID выбранной поездки
    current_chat_id = None  # Для хранения ID чата (например, ID получателя)

    theme = StringProperty('light')
    THEMES = THEMES

    def on_start(self):
        # Применяем тему при запуске
        self.apply_theme()

    def toggle_theme(self):
        # Переключение между светлой и тёмной темой
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.apply_theme()

    def apply_theme(self):
        # Применение цветов темы ко всему окну
        theme = self.THEMES[self.theme]
        Window.clearcolor = theme['background']

        

    def build(self):
        # Инициализация сервисов
        self.auth = AuthService()
        self.db = DatabaseService()
        self.chat = ChatService()
        self.maps = MapsService()

        # Инициализация переменных
        self.current_trip_id = None
        self.current_chat_id = None

        # === Создаём менеджер экранов ===
        sm = ScreenManager()

        # 1️⃣ Сначала добавляем заставку — она должна быть первой!
        sm.add_widget(SplashScreen(name='splash'))
        sm.current = 'splash'

        # 2️⃣ Остальные экраны добавляем после
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(SearchTripsScreen(name='search_trips'))
        sm.add_widget(CreateTripScreen(name='create_trip'))
        sm.add_widget(TripDetailsScreen(name='trip_details'))
        sm.add_widget(BookingScreen(name='booking'))
        sm.add_widget(ChatScreen(name='chat'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(MyTripsScreen(name='my_trips'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm


if __name__ == '__main__':
    CarpoolingApp().run()