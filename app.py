import os
import re
import smtplib
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_mail import Mail, Message

# Initialize Flask
app = Flask(__name__)

# ===== ENVIRONMENT SETUP =====
try:
    from dotenv import load_dotenv
    load_dotenv('.env')  # Explicitly load from .env file
    print("✅ .env loaded successfully")
except ImportError:
    print("⚠️ python-dotenv not installed, using system environment variables")

# ===== Configuration =====
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv('GMAIL_USER'),
    MAIL_PASSWORD=os.getenv('GMAIL_APP_PASSWORD'),
    MAIL_DEBUG=True
)
mail = Mail(app)

# ===== SQLi Detection =====
def is_malicious(query):
    patterns = [
        r"'.*--", r";\s*--", r"\/\*.*\*\/",
        r"\bOR\b.+\d+=\d+", r"\bUNION\b.*\bSELECT\b",
        r"\b(DROP|INSERT|EXEC)\b"
    ]
    return any(re.search(p, query, re.IGNORECASE) for p in patterns)

# ===== Logging Function =====
def log_attack(query):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] SQL Injection Attempt Detected - IP: {request.remote_addr} - Query: {query[:500]}\n"
    
    try:
        with open('attack_logs.txt', 'a') as log_file:
            log_file.write(log_entry)
        print(f"📝 Attack logged: {log_entry.strip()}")
    except Exception as e:
        print(f"❌ Failed to write to log file: {str(e)}")

# ===== Routes =====
@app.route('/check', methods=['GET', 'POST'])
def check_sql_injection():
    # Browser form
    if request.method == 'GET':
        return render_template_string('''
            <h2>SQL Injection Tester</h2>
            <form method="POST">
                <textarea name="query" rows="5" cols="50" 
                  placeholder="Enter SQL query">SELECT * FROM users</textarea><br>
                <input type="submit" value="Check">
            </form>
            <hr>
            <h3>Or test with cURL:</h3>
            <code>
            curl -X POST http://127.0.0.1:5000/check \<br>
              -H "Content-Type: application/json" \<br>
              -d '{"query":"your_query_here"}'
            </code>
        ''')

    # API processing
    try:
        if request.is_json:
            data = request.get_json()
            query = data.get('query', '')
        else:  # Form submission
            query = request.form.get('query', '')
        
        print(f"📥 Received query: {query[:100]}...")

        if is_malicious(query):
            # Log the attack
            log_attack(query)
            
            # Send email alert
            with app.app_context():
                msg = Message(
                    "🚨 SQLi Blocked",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[app.config['MAIL_USERNAME']],
                    body=f"""SQL Injection Attempt:
                        
                        IP: {request.remote_addr}
                        Time: {datetime.now()}
                        Full Query: {query[:1000]}... (truncated)
                        """
                )
                mail.send(msg)
            
            return jsonify({
                "status": "malicious",
                "detected": True,
                "action": "blocked_and_logged"
            }), 403
        
        return jsonify({"status": "safe"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create attack logs file if it doesn't exist
    if not os.path.exists('attack_logs.txt'):
        with open('attack_logs.txt', 'w') as f:
            f.write("=== SQL Injection Attack Log ===\n")
    
    app.run(host='127.0.0.1', port=5000, debug=True)