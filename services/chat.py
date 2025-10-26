# services/chat.py
from datetime import datetime
from kivy.app import App
from services.database import Message

class ChatService:
    def __init__(self):
        pass

    def send_message(self, sender_id, receiver_id, text):
        db = App.get_running_app().db
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = db.conn.cursor()
        cursor.execute('INSERT INTO messages (sender_id, receiver_id, text, time) VALUES (?, ?, ?, ?)',
                       (sender_id, receiver_id, text, time))
        db.conn.commit()

    def get_messages(self, user_id, other_user_id):
        db = App.get_running_app().db
        cursor = db.conn.cursor()
        cursor.execute('''
            SELECT * FROM messages
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY time
        ''', (user_id, other_user_id, other_user_id, user_id))
        return [Message(*row) for row in cursor.fetchall()]