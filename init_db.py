import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'username',   
    'password': 'password'
}

def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS workout_db")
    cursor.execute("USE workout_db")

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            exercise VARCHAR(255),
            reps INT,
            sets INT,
            duration INT
        )
    ''')
    
    print("Database initialized successfully!")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
