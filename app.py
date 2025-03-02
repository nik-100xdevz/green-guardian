from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///green_guardian.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)
    contributions = db.relationship('Contribution', backref='user', lazy=True)
    pickups = db.relationship('Pickup', backref='user', lazy=True)

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pickup_date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create DB tables if they don't exist
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

# API endpoint to record a scan (contribution)
@app.route('/api/record_scan', methods=['POST'])
def record_scan():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, points=10)
        db.session.add(user)
    else:
        user.points += 10  # Award 10 points per scan

    contribution = Contribution(user=user)
    db.session.add(contribution)
    db.session.commit()
    return jsonify({"message": "Contribution recorded", "points": user.points})

@app.route('/pickup', methods=['GET', 'POST'])
def pickup():
    if request.method == 'POST':
        username = request.form.get('username')
        pickup_date = request.form.get('pickup_date')
        pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        print(type(pickup_date))
        print(pickup_date)  # printed in default format
        
        if not username or not pickup_date:
            flash("Username and Pickup Date are required.", "danger")
            return redirect(url_for('pickup'))

        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        new_pickup = Pickup(user_id=user.id, pickup_date=pickup_date)
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

if __name__ == '__main__':
    app.run(debug=True)
