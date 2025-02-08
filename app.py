from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import matplotlib.pyplot as plt
import os
import subprocess

app = Flask(__name__)
DB_FILE = "workout.db"

# Initialize Database
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          exercise TEXT,
                          reps INTEGER,
                          sets INTEGER,
                          duration INTEGER)''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_workout():
    exercise = request.form['exercise']
    reps = request.form['reps']
    sets = request.form['sets']
    duration = request.form['duration']

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workouts (exercise, reps, sets, duration) VALUES (?, ?, ?, ?)",
                       (exercise, reps, sets, duration))
    
    return redirect(url_for('index'))

@app.route('/report')
def generate_report():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT exercise, SUM(reps) FROM workouts GROUP BY exercise")
        data = cursor.fetchall()

    if not data:
        return "No workout data available!"

    exercises, reps = zip(*data)

    # Ensure 'static' directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    # Generate bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(exercises, reps, color='blue')
    plt.xlabel("Exercise")
    plt.ylabel("Total Reps")
    plt.title("Workout Progress")
    plt.xticks(rotation=45)

    # Save chart image
    image_path = os.path.join("static", "report.png")
    plt.savefig(image_path)
    plt.close()

    return render_template('report.html', image=image_path)

@app.route('/push_to_github', methods=['POST'])
def push_to_github():
    try:
        subprocess.run(["git", "add", "--all"], check=True)
        subprocess.run(["git", "commit", "-m", "Updated workout tracker"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        return "Pushed to GitHub successfully!"
    except subprocess.CalledProcessError as e:
        return f"Error pushing to GitHub: {e}"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
