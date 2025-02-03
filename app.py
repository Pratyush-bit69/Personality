from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Function to connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="duggi11#",  # Replace with your MySQL password
        database="personality_db"  # Replace with your database name
    )

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html matches your form's file name

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        personality = request.form['personality']

        # Insert the data into MySQL database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, personality) VALUES (%s, %s, %s)",
            (name, email, personality)
        )
        conn.commit()
        conn.close()

        # Redirect to the specific personality page
        personality_links = {
            "INTJ": "https://www.16personalities.com/intj-personality",
            "INTP": "https://www.16personalities.com/intp-personality",
            "ENTJ": "https://www.16personalities.com/entj-personality",
            "ENTP": "https://www.16personalities.com/entp-personality",
            "INFJ": "https://www.16personalities.com/infj-personality",
            "INFP": "https://www.16personalities.com/infp-personality",
            "ENFJ": "https://www.16personalities.com/enfj-personality",
            "ENFP": "https://www.16personalities.com/enfp-personality",
            "ISTJ": "https://www.16personalities.com/istj-personality",
            "ISFJ": "https://www.16personalities.com/isfj-personality",
            "ESTJ": "https://www.16personalities.com/estj-personality",
            "ESFJ": "https://www.16personalities.com/esfj-personality",
            "ISTP": "https://www.16personalities.com/istp-personality",
            "ISFP": "https://www.16personalities.com/isfp-personality",
            "ESTP": "https://www.16personalities.com/estp-personality",
            "ESFP": "https://www.16personalities.com/esfp-personality"
        }

        return redirect(personality_links.get(personality, '/'))

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your request.", 500

if __name__ == '__main__':
    app.run(debug=True)