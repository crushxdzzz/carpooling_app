from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp


class SplashScreen(Screen):
    def on_enter(self):
        """Когда экран открывается — запускаем анимацию"""
        self.start_animation()

    def start_animation(self):
        # Текст логотипа
        label = Label(
            text='Carpooling App',
            font_size=dp(28),
            bold=True,
            opacity=0
        )
        self.add_widget(label)

        # Центрируем текст
        label.center_x = self.center_x
        label.center_y = self.center_y
        label.bind(size=self._update_pos, pos=self._update_pos)

        # Анимация появления и исчезновения
        anim = Animation(opacity=1, duration=1.2) + Animation(opacity=0, duration=0.8)
        anim.start(label)

        # После завершения анимации → переход на главное меню
        Clock.schedule_once(self.go_to_main_menu, 2)

    def go_to_main_menu(self, *args):
        if self.manager:
            self.manager.current = 'welcome'

    def _update_pos(self, instance, value):
        instance.center_x = self.center_x
        instance.center_y = self.center_y