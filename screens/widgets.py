# screens/widgets.py
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from datetime import datetime

class DatePicker(ModalView):
    def __init__(self, callback, **kwargs):
        super().__init__(size_hint=(0.8, 0.5), **kwargs)
        self.callback = callback
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Текущая дата для начальных значений
        today = datetime.now()
        year_values = [str(y) for y in range(2023, 2030)]
        month_values = [f'{m:02d}' for m in range(1, 13)]
        day_values = [f'{d:02d}' for d in range(1, 32)]
        
        layout.add_widget(Label(text='Выберите дату', font_size=20))
        
        date_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.year = Spinner(text=str(today.year), values=year_values)
        self.month = Spinner(text=f'{today.month:02d}', values=month_values)
        self.day = Spinner(text=f'{today.day:02d}', values=day_values)
        date_layout.add_widget(self.year)
        date_layout.add_widget(self.month)
        date_layout.add_widget(self.day)
        layout.add_widget(date_layout)
        
        btn_confirm = Button(text='Подтвердить', size_hint=(1, 0.2))
        btn_confirm.bind(on_press=self.confirm)
        layout.add_widget(btn_confirm)
        
        self.add_widget(layout)

    def confirm(self, instance):
        try:
            date = f"{self.year.text}-{self.month.text}-{self.day.text}"
            # Валидация даты
            datetime.strptime(date, '%Y-%m-%d')
            self.callback(date)
            self.dismiss()
        except ValueError:
            # Можно добавить лейбл с ошибкой, но для простоты просто не закрываем
            pass

class TimePicker(ModalView):
    def __init__(self, callback, **kwargs):
        super().__init__(size_hint=(0.6, 0.4), **kwargs)
        self.callback = callback
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Текущее время для начальных значений
        now = datetime.now()
        hour_values = [f'{h:02d}' for h in range(0, 24)]
        minute_values = [f'{m:02d}' for m in range(0, 60, 5)]  # Шаг 5 минут
        
        layout.add_widget(Label(text='Выберите время', font_size=20))
        
        time_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.hour = Spinner(text=f'{now.hour:02d}', values=hour_values)
        self.minute = Spinner(text=f'{now.minute // 5 * 5:02d}', values=minute_values)
        time_layout.add_widget(self.hour)
        time_layout.add_widget(self.minute)
        layout.add_widget(time_layout)
        
        btn_confirm = Button(text='Подтвердить', size_hint=(1, 0.2))
        btn_confirm.bind(on_press=self.confirm)
        layout.add_widget(btn_confirm)
        
        self.add_widget(layout)

    def confirm(self, instance):
        time = f"{self.hour.text}:{self.minute.text}"
        try:
            # Валидация времени
            datetime.strptime(time, '%H:%M')
            self.callback(time)
            self.dismiss()
        except ValueError:
            pass