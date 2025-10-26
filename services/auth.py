# services/auth.py
from kivy.app import App

class AuthService:
    def __init__(self):
        self.current_user = None

    def login(self, phone, password):
        db = App.get_running_app().db
        user = db.get_user_by_phone(phone)
        if user:
            cursor = db.conn.cursor()
            cursor.execute('SELECT password FROM users WHERE phone = ?', (phone,))
            stored_password = cursor.fetchone()[0]
            if stored_password == password:
                self.current_user = user
                return True
        return False

    def logout(self):
        self.current_user = None