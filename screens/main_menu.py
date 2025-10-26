# screens/main_menu.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.app import App  # Для доступа к App, если нужно проверить роль или текущего пользователя
from themes import THEMES

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Главное меню', font_size=24, bold=True))
        
        # Кнопки для навигации
        btn_search = Button(text='Поиск поездок')
        btn_search.bind(on_press=self.go_to_search)
        layout.add_widget(btn_search)
        
        btn_create = Button(text='Создать поездку')
        btn_create.bind(on_press=self.go_to_create)
        layout.add_widget(btn_create)
        
        btn_profile = Button(text='Профиль')
        btn_profile.bind(on_press=self.go_to_profile)
        layout.add_widget(btn_profile)
        
        btn_my_trips = Button(text='Мои поездки')
        btn_my_trips.bind(on_press=self.go_to_my_trips)
        layout.add_widget(btn_my_trips)
        
        btn_settings = Button(text='Настройки')
        btn_settings.bind(on_press=self.go_to_settings)
        layout.add_widget(btn_settings)
        
        self.add_widget(layout)

    def on_enter(self):
        # При входе на экран проверяем текущего пользователя и, optionally, скрываем кнопки по роли
        app = App.get_running_app()
        if app.auth.current_user:
            user_role = app.auth.current_user.role.lower()
            for child in self.children[0].children:
                if isinstance(child, Button) and 'Создать поездку' in child.text:
                    if user_role == 'водитель':
                        # Водитель — включаем кнопку и возвращаем исходный текст
                        child.disabled = False
                        child.text = 'Создать поездку'
                    else:
                        # Не водитель — блокируем кнопку и меняем текст
                        child.disabled = True
                        child.text = 'Создать поездку (только для водителей)'
                    break
        else:
            # Если не авторизован, перенаправляем на welcome
            self.manager.current = 'welcome'

    def go_to_search(self, instance):
        self.manager.current = 'search_trips'

    def go_to_create(self, instance):
        app = App.get_running_app()

        # Получаем текущую тему
        theme = THEMES[getattr(app, 'theme', 'light')]
        # Основные цвета
        default_color = theme["button_bg"]
        text_color = theme["text"]
        # Цвет для кнопки "Создать поездку" — немного темнее стандартного
        create_color = tuple(max(0, c - 0.1) for c in default_color[:3]) + (1,)
        
        if app.auth.current_user and app.auth.current_user.role.lower() == 'водитель':
            self.manager.current = 'create_trip'
        else:
            # Можно добавить лейбл с ошибкой, но для простоты просто не переходим
            pass  # Или показать сообщение

    def go_to_profile(self, instance):
        self.manager.current = 'profile'

    def go_to_my_trips(self, instance):
        self.manager.current = 'my_trips'

    def go_to_settings(self, instance):
        self.manager.current = 'settings'

    def on_enter(self):
        # Анимация плавного появления экрана
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.4)
        anim.start(self)