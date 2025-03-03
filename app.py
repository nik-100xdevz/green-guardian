from flask import Flask, render_template, request, redirect, url_for, jsonify, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import random

from datetime import datetime


app = Flask(__name__)
app.secret_key = "your_secret_key_here"


# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///green_guardian.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)
    contributions = db.relationship('Contribution', backref='user', lazy=True)
    pickups = db.relationship('Pickup', backref='user', lazy=True)

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)
    pickup_number = db.Column(db.Integer, nullable=False)
    pickup_location = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create DB tables if they don't exist

with app.app_context():
    db.create_all()

# Routes
@app.context_processor
def inject_user():
    return dict(user=session.get("username"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash("User with this username already exits.", "danger")
            return redirect(url_for('signup'))
        else:
            user = User(username=username, password = password)
            db.session.add(user)
            db.session.commit()
        flash("User added successfully!", "success")
        return redirect(url_for('scan'))
    return render_template('signup.html')

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Invalid credentials if you are new to website please signup See below sign in button.", "danger")
            return redirect(url_for('signin'))
        else:
           if(password == user.password):   
            flash("Logged in successfully!", "success")
            session['username'] = username
            return redirect(url_for('scan'))
           else:
            flash("Invalid credentials if you are new to website please signup See below sign in button.", "danger")
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        session.pop('username')
        flash(f"Logged out of website {username}","success")
        return render_template('index.html')
    else:
        flash("No user found","danger")
        return render_template('index.html')

@app.route('/scan')
def scan():
    username = session.get('username')
    if not username:
        return render_template('signin.html')
    return render_template('scan.html')

# API endpoint to record a scan (contribution)
@app.route('/api/record_scan', methods=['POST'])
def record_scan():
    
    if not session.get("username"):
        return jsonify({"message": "you are not logged in"})
    

    user = User.query.filter_by(username=session.get("username")).first()

    user.points += random.randint(10, 100)  # Award 10 points per scan

    contribution = Contribution(user=user)
    db.session.add(contribution)
    db.session.commit()
    return jsonify({"message": "Contribution recorded", "points": user.points})

@app.route('/pickup', methods=['GET', 'POST'])
def pickup():
    if not session.get('username'):
        return render_template('signin.html')
    if request.method == 'POST':
        username = request.form.get('username')
        pickup_date = request.form.get('pickup_date')
        pickup_number = request.form.get('pickup_number')
        pickup_location = request.form.get('pickup_location')
        pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        
        if not username or not pickup_date:
            flash("Username and Pickup Date are required.", "danger")
            return redirect(url_for('pickup'))

        user = User.query.filter_by(username=session.get('username')).first()
        print(pickup_date)
        new_pickup = Pickup(user_id=user.id,username= username ,pickup_date=pickup_date, pickup_number=pickup_number,pickup_location=pickup_location )
        db.session.add(new_pickup)
        db.session.commit()
        flash("Pickup scheduled successfully!", "success")
        return redirect(url_for('pickup'))
    return render_template('pickup.html')

@app.route('/leaderboard')
def leaderboard():
    # Get top 10 users by points
    top_users = User.query.order_by(User.points.desc()).limit(10).all()
    return render_template('leaderboard.html', users=top_users)

@app.route('/pickup-details')
def pickupDetails():
    # Get top 10 users by points
    top_pickup = Pickup.query.all()
    return render_template('pickup_info.html', pickups= top_pickup)

if __name__ == '__main__':
    app.run(debug=True)
