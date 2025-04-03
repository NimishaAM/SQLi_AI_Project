from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='nimishatest56@gmail.com',
    MAIL_PASSWORD='kret ivzx bzes cweh'
)

mail = Mail(app)

with app.app_context():
    try:
        msg = Message('Test Email', sender='nimishatest56@gmail.com', recipients=['nimishatest56@gmail.com'])
        msg.body = "This is a test email from Flask."
        mail.send(msg)
        print("✅ Test email sent successfully!")
    except Exception as e:
        print(f"❌ Test email failed: {e}")
