# Importowanie niezbędnych bibliotek
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Tworzenie instancji aplikacji Flask
app = Flask(__name__)

# Strona główna aplikacji
@app.route('/')
def home():
    # Renderowanie szablonu HTML dla strony głównej
    return render_template('app.html')

# Strona z filmami
@app.route('/video')
def video():
    # Renderowanie szablonu HTML dla strony z filmami
    return render_template("video.html")

# Strona z listą zadań
@app.route('/zadania')
def zadania():
    # Połączenie z bazą danych
    conn = sqlite3.connect('zadania.db')
    c = conn.cursor()
    
    # Wykonanie zapytania do bazy danych w celu pobrania tytułów zadań
    c.execute('SELECT id, tytul FROM zadania')
    zadania = c.fetchall()  # Pobranie wszystkich wyników zapytania
    
    # Zamknięcie połączenia z bazą danych
    conn.close()
    
    # Renderowanie szablonu HTML i przekazanie listy zadań do wyświetlenia
    return render_template('zadania.html', zadania=zadania)

# Strona z konkretnym zadaniem, wyświetlana po kliknięciu w zadanie
@app.route('/zadanie/<int:id>')
def zadanie(id):
    # Połączenie z bazą danych
    conn = sqlite3.connect('zadania.db')
    c = conn.cursor()
    
    # Wykonanie zapytania w celu pobrania szczegółów konkretnego zadania
    c.execute('SELECT tytul, tresc FROM zadania WHERE id = ?', (id,))
    zadanie = c.fetchone()  # Pobranie jednego wyniku zapytania
    
    # Zamknięcie połączenia z bazą danych
    conn.close()
    
    # Renderowanie szablonu HTML i przekazanie danych zadania do wyświetlenia
    return render_template('zadanie.html', zadanie=zadanie)

# Funkcja tworząca bazę danych i dodająca przykładowe zadania, jeśli baza jest pusta
def create_database():
    # Połączenie z bazą danych SQLite
    conn = sqlite3.connect('zadania.db')
    c = conn.cursor()
    
    # Tworzenie tabeli 'zadania' (jeśli nie istnieje)
    c.execute('''
        CREATE TABLE IF NOT EXISTS zadania (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tytul TEXT NOT NULL,
            tresc TEXT NOT NULL
        )
    ''')
    
    # Sprawdzenie, czy w tabeli są już jakieś zadania
    c.execute('SELECT COUNT(*) FROM zadania')
    count = c.fetchone()[0]
    
    # Jeśli tabela jest pusta, dodajemy przykładowe zadania
    if count == 0:
        zadania = [
            ('Pierwsze zadanie', 'Napisz program, który wypisze "Hello World" na ekranie.'),
            ('Drugie zadanie', 'Napisz funkcję, która dodaje dwie liczby.'),
            ('Trzecie zadanie', 'Napisz program, który sprawdza czy liczba jest parzysta.')
        ]
        
        # Dodanie przykładowych zadań do bazy danych
        c.executemany('INSERT INTO zadania (tytul, tresc) VALUES (?, ?)', zadania)
        
        # Zatwierdzenie zmian w bazie danych
        conn.commit()
    
    # Zamknięcie połączenia z bazą danych
    conn.close()

# Uruchomienie aplikacji Flask, jeśli jest uruchamiana bezpośrednio
if __name__ == "__main__":
    # Uruchomienie funkcji do tworzenia bazy danych
    # create_database()  # Odkomentuj, jeśli chcesz utworzyć bazę danych na starcie
    app.run(debug=True)  # Uruchomienie aplikacji Flask w trybie debugowania
    
    
            
        




    
    

    


