from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
import re

# Sample malicious SQL patterns
malicious_patterns = [
    r"(--|#)",  # SQL comment patterns
    r"(\bOR\b|\bAND\b)\s+\d=\d",  # Boolean-based SQL injection
    r"UNION\s+SELECT",  # UNION-based SQL injection
    r"SLEEP\(\d+\)",  # Time-based SQL injection
    r"CONVERT\(",  # Error-based SQL injection
    r"EXEC\s+xp_",  # Out-of-band SQL injection
    r"\bDROP\b|\bDELETE\b|\bALTER\b",  # Dangerous SQL commands
    r"\bSELECT\b.*\bFROM\b.*\bWHERE\b.*\b\=\b.*\bOR\b|\bAND\b",  # Basic pattern for OR/AND based SQLi
    r"\bINSERT\b.*\bINTO\b.*\bVALUES\b.*;\s*DROP\b",  # Second-order SQL injection
    r"{\s*\"\$gt\":\s*\"\".*}",  # NoSQL Injection example pattern
]

def detect_sql_injection(sql_command):
    sql_command_lower = sql_command.lower()
    for pattern in malicious_patterns:
        if re.search(pattern, sql_command_lower):
            return "Malicious SQL detected!"
    return "SQL command appears to be legitimate."

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add actual authentication here
        session['email'] = email
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add actual registration here
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/about')
def about():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    sql_command = request.form.get('sql_command')
    result = detect_sql_injection(sql_command)
    return jsonify({"result": result})

@app.route('/predictor', methods=['GET', 'POST'])
def predictor():
    if request.method == 'POST':
        sql_command = request.form.get('sql_command')
        print(f"Received SQL command: {sql_command}")  # Debugging output
        result = detect_sql_injection(sql_command)
        return render_template('predictor.html', result=result)
    return render_template('predictor.html')


@app.route('/help')
def help():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('help.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)  # Remove the user session
    return redirect(url_for('login'))  # Redirect to the login page
