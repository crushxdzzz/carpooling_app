# screens/settings.py
from kivy.uix.screenmanager import Screen
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.metrics import dp
from themes import THEMES


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # === Заголовок ===
        self.title_label = Label(
            text='Настройки',
            font_size=24,
            bold=True,
            size_hint_y=None,
            height=dp(60),
            halign='center',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        self.main_layout.add_widget(self.title_label)

        # === Кнопка "Назад" (под заголовком, слева) ===
        back_layout = AnchorLayout(anchor_x='left', anchor_y='top', size_hint_y=None, height=dp(50))
        self.btn_back = Button(
            text='Назад',
            size_hint=(None, None),
            size=(dp(100), dp(40))
        )
        self.btn_back.bind(on_press=self.go_back)
        back_layout.add_widget(self.btn_back)
        self.main_layout.add_widget(back_layout)

        # === Переключатель темы ===
        app = App.get_running_app()
        theme = self._get_active_theme(app)

        theme_box = AnchorLayout(anchor_x='left', size_hint_y=None, height=dp(60))
        theme_row = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(dp(300), dp(40)),  # ограничиваем ширину до ~половины экрана
            spacing=dp(10)
        )

        theme_label = Label(
            text='Тёмная тема',
            size_hint_x=None,
            width=dp(150),
            halign='left',
            valign='middle'
        )
        theme_label.bind(size=theme_label.setter('text_size'))

        theme_switch = Switch(active=(theme["background"][0] < 0.5))

        def on_switch(instance, value):
            app.toggle_theme()
            self.update_theme()

        theme_switch.bind(active=on_switch)

        theme_row.add_widget(theme_label)
        theme_row.add_widget(theme_switch)
        theme_box.add_widget(theme_row)
        self.main_layout.add_widget(theme_box)

        # 🔔 Переключатель "Уведомления"
        notifications_box = AnchorLayout(anchor_x='left', size_hint_y=None, height=dp(60))
        notifications_row = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(dp(300), dp(40)),  # ограничиваем ширину, чтобы выглядело аккуратно
            spacing=dp(10)
        )

        notifications_label = Label(
            text='Уведления',
            size_hint_x=None,
            width=dp(150),
            halign='left',
            valign='middle'
        )
        notifications_label.bind(size=notifications_label.setter('text_size'))

        notifications_switch = Switch(active=False)
        notifications_switch.bind(active=self.toggle_notify)  # если нужно сохранять настройку

        notifications_row.add_widget(notifications_label)
        notifications_row.add_widget(notifications_switch)
        notifications_box.add_widget(notifications_row)
        self.main_layout.add_widget(notifications_box)



        # === Растяжка (чтобы "Выйти" было внизу) ===
        self.main_layout.add_widget(Label(size_hint_y=1))

        # === Кнопка "Выйти из аккаунта" ===
        logout_layout = AnchorLayout(anchor_y='bottom')
        self.btn_logout = Button(
            text='Выйти из аккаунта',
            size_hint=(None, None),
            size=(dp(180), dp(40))
        )
        self.btn_logout.bind(on_press=self.logout)
        logout_layout.add_widget(self.btn_logout)
        self.main_layout.add_widget(logout_layout)

        # === Ошибки ===
        self.error_label = Label(
            text='',
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=dp(30)
        )
        self.main_layout.add_widget(self.error_label)

        self.add_widget(self.main_layout)
        self.update_theme()

    # === Методы ===

    def _get_active_theme(self, app):
        """Безопасно возвращает словарь темы"""
        try:
            if isinstance(app.theme, str):
                return getattr(app, "THEMES", {}).get(app.theme, {})
            return app.theme
        except Exception:
            return {
                "background": (1, 1, 1, 1),
                "text": (0, 0, 0, 1),
                "button": (0.9, 0.9, 0.9, 1),
            }

    def update_theme(self):
        """Обновляет цвета интерфейса под текущую тему"""
        app = App.get_running_app()
        theme = self._get_active_theme(app)

        text_color = theme.get("text", (0, 0, 0, 1))
        btn_color = theme.get("button", (0.9, 0.9, 0.9, 1))
        background_color = theme.get("background", (1, 1, 1, 1))

        # Фон
        self.main_layout.canvas.before.clear()
        from kivy.graphics import Color, Rectangle
        with self.main_layout.canvas.before:
            Color(*background_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_rect, size=self._update_rect)

        # Цвета элементов
        self.title_label.color = text_color
        self.btn_back.background_color = btn_color
        self.btn_back.color = text_color
        self.btn_logout.background_color = (0.7, 0.2, 0.2, 1)
        self.btn_logout.color = (1, 1, 1, 1)

    def toggle_notify(self, instance, value):
        """Сохраняем настройку уведомлений в конфиг приложения"""
        app = App.get_running_app()

        if not app.config.has_section('Settings'):
            app.config.add_section('Settings')

        app.config.set('Settings', 'notify_new_trips', str(value))
        app.config.write()

        # Если пользователь включил уведомления — показать запрос
        if value:
            self.ask_notification_permission()


    def ask_notification_permission(self):
        """Показывает диалог с запросом разрешения на уведомления"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text='Разрешить приложению отправлять уведомления?',
            halign='center',
            valign='middle'
        ))

        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_yes = Button(text='Да')
        btn_no = Button(text='Нет')
        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)

        content.add_widget(btn_layout)

        popup = Popup(
            title='Разрешения',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )

        def close_popup(instance):
            popup.dismiss()

        btn_yes.bind(on_press=close_popup)
        btn_no.bind(on_press=close_popup)

        popup.open()



    def _update_rect(self, *args):
        if hasattr(self, "bg_rect"):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size

    def logout(self, instance):
        app = App.get_running_app()
        app.auth.logout()
        app.current_trip_id = None
        app.current_chat_id = None
        self.manager.current = 'welcome'

    def go_back(self, instance):
        self.manager.current = 'main_menu'