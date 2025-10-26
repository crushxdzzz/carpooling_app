import sqlite3
import os
from datetime import datetime

class User:
    def __init__(self, id, name, phone, role, rating):
        self.id = id
        self.name = name
        self.phone = phone
        self.role = role
        self.rating = rating

class Trip:
    def __init__(self, id, driver_id, route, date, time, price, seats):
        self.id = id
        self.driver_id = driver_id
        self.route = route
        self.date = date
        self.time = time
        self.price = price
        self.seats = seats

class Message:
    def __init__(self, id, sender_id, receiver_id, text, time):
        self.id = id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.text = text
        self.time = time

class Booking:
    def __init__(self, id, trip_id, passenger_id):
        self.id = id
        self.trip_id = trip_id
        self.passenger_id = passenger_id

class DatabaseService:
    def __init__(self):
        db_path = os.path.join('database', 'carpooling.db')
        os.makedirs('database', exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                phone TEXT UNIQUE,
                password TEXT,
                role TEXT,
                rating REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id INTEGER,
                route TEXT,
                date TEXT,
                time TEXT,
                price REAL,
                seats INTEGER,
                FOREIGN KEY (driver_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER,
                passenger_id INTEGER,
                FOREIGN KEY (trip_id) REFERENCES trips(id),
                FOREIGN KEY (passenger_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER,
                receiver_id INTEGER,
                text TEXT,
                time TEXT,
                FOREIGN KEY (sender_id) REFERENCES users(id),
                FOREIGN KEY (receiver_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    def create_user(self, name, phone, password, role):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (name, phone, password, role, rating) VALUES (?, ?, ?, ?, ?)',
                       (name, phone, password, role.lower(), 0.0))
        self.conn.commit()
        cursor.execute('SELECT id, name, phone, role, rating FROM users WHERE name = ?', (name,))
        return User(*cursor.fetchone())

    def get_user(self, name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, phone, role, rating FROM users WHERE name = ?', (name,))
        row = cursor.fetchone()
        return User(*row) if row else None

    def get_user_by_phone(self, phone):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, phone, role, rating FROM users WHERE phone = ?', (phone,))
        row = cursor.fetchone()
        return User(*row) if row else None

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, phone, role, rating FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return User(*row) if row else None

    def update_user_name(self, user_id, new_name):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET name = ? WHERE id = ?', (new_name, user_id))
        self.conn.commit()

    def create_trip(self, driver_id, route, date, time, price, seats):
        cursor = self.conn.cursor()
        route = route.strip().lower()  # Приводим маршрут к нижнему регистру
        cursor.execute('INSERT INTO trips (driver_id, route, date, time, price, seats) VALUES (?, ?, ?, ?, ?, ?)',
                       (driver_id, route, date, time, price, seats))
        self.conn.commit()
        cursor.execute('SELECT * FROM trips WHERE driver_id = ? AND route = ? AND date = ? AND time = ?',
                       (driver_id, route, date, time))
        return Trip(*cursor.fetchone())

    def get_trip(self, trip_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM trips WHERE id = ?', (trip_id,))
        row = cursor.fetchone()
        return Trip(*row) if row else None

    def search_trips(self, from_loc, to_loc, date):
        cursor = self.conn.cursor()
        # Приводим входные данные к нижнему регистру и убираем пробелы
        from_loc = from_loc.strip().lower()
        to_loc = to_loc.strip().lower()
        search_route = f'%{from_loc}%-%{to_loc}%'
        print(f"Searching for route: {search_route}, date: {date}")  # Отладочный вывод
        cursor.execute('''
            SELECT * FROM trips 
            WHERE lower(route) LIKE ? AND date = ? AND seats > 0
        ''', (search_route, date))
        results = [Trip(*row) for row in cursor.fetchall()]
        print(f"Found {len(results)} trips")  # Отладочный вывод
        return results

    def create_booking(self, trip_id, passenger_id):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO bookings (trip_id, passenger_id) VALUES (?, ?)',
                       (trip_id, passenger_id))
        self.conn.commit()
        cursor.execute('SELECT * FROM bookings WHERE trip_id = ? AND passenger_id = ?',
                       (trip_id, passenger_id))
        return Booking(*cursor.fetchone())

    def update_trip_seats(self, trip_id, new_seats):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE trips SET seats = ? WHERE id = ?', (new_seats, trip_id))
        self.conn.commit()

    def get_user_trips(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM trips WHERE driver_id = ?
            UNION
            SELECT trips.* FROM trips
            JOIN bookings ON trips.id = bookings.trip_id
            WHERE bookings.passenger_id = ?
        ''', (user_id, user_id))
        return [Trip(*row) for row in cursor.fetchall()]

    def get_all_trips(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM trips WHERE seats > 0')
        return [Trip(*row) for row in cursor.fetchall()]
    
    def add_booking(self, user_id, trip_id, seats=1):
        """Добавляет бронирование пользователя на поездку"""
        cursor = self.conn.cursor()

        # Проверяем, не существует ли уже такого бронирования
        cursor.execute("""
            SELECT id FROM bookings WHERE passenger_id = ? AND trip_id = ?
        """, (user_id, trip_id))
        existing = cursor.fetchone()
        if existing:
            print("⚠️ Пользователь уже забронировал эту поездку.")
            return False

        # Добавляем бронирование
        cursor.execute("""
            INSERT INTO bookings (trip_id, passenger_id)
            VALUES (?, ?)
        """, (trip_id, user_id))

        # Обновляем количество мест
        cursor.execute("""
            UPDATE trips SET seats = seats - ? WHERE id = ? AND seats >= ?
        """, (seats, trip_id, seats))

        self.conn.commit()
        print(f"✅ Бронирование добавлено: trip_id={trip_id}, user_id={user_id}, seats={seats}")
        return True
