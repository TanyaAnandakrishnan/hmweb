from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import joblib
import numpy as np
import pywhatkit as kit
import os
import time
import pyautogui

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,user_id)

# Load trained ML model
model = joblib.load(os.path.join(os.getcwd(),"emotion_model.pkl"))

def send_alert():
    """Send emergency WhatsApp message."""
    phone_number = "+917373745562"
    message = "⚠ Emergency Alert: Panic detected! Immediate assistance required!"
    try:
        print("Trying to send message")
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=5)
        print("✅ Emergency alert sent!")
    except Exception as e:
        print("Error)")

import os
import time
import pyautogui

def make_phone_call():
    phone_number = "9750099955"  # Replace with your number
    
    # Open the "Phone Link" (Your Phone) app
    os.system("start shell:AppsFolder\\Microsoft.YourPhone_8wekyb3d8bbwe!App")
    time.sleep(10)  # Wait for the app to open

    # Click the search/contact field (Adjust coordinates based on your screen)
    pyautogui.click(x=400, y=200)  
    time.sleep(2)

    # Type the phone number
    pyautogui.write(phone_number, interval=0.2)
    time.sleep(1)

    # Press Enter to call
    pyautogui.press("enter")
    print(f"📞 Calling {phone_number}...")



@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        heart_rate = int(request.form["heart_rate"])
        systolic_bp = int(request.form["systolic_bp"])
        diastolic_bp = int(request.form["diastolic_bp"])
        pulse_rate = int(request.form["pulse_rate"])

        # Predict emotion
        input_data = np.array([[heart_rate, systolic_bp, diastolic_bp, pulse_rate]])
        prediction = model.predict(input_data)[0]

        emotions = ["Relaxed", "Calm", "Focused", "Happy", "Anxious", "Panic"]
        detected_emotion = emotions[prediction]

        if detected_emotion == "Panic":
            send_alert()
            make_phone_call()

        return render_template("index.html", emotion=detected_emotion)

    return render_template("index.html", emotion=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for("index"))
        else:
            return "❌ Invalid credentials, try again."

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "⚠ Username already taken!"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)