from flask import Flask, render_template, request, redirect, url_for, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def ip_grabbing():
    ip_url = "https://geo.ipify.org/api/v2/country,city,vpn?apiKey=YOUR_API_KEY&ipAddress=8.8.8.8"
    response = requests.get(ip_url)


class Workout(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user = db.Column(db.String(), nullable = True)
    workout = db.Column(db.String(), nullable = True)
    date = db.Column(db.DateTime(), default = datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/<user>", methods=['GET', 'POST'])
def main(user):
    if request.method == 'POST':
        new_Workout = Workout(
            user = user,
            workout = request.form['content'],
        )
        db.session.add(new_Workout)
        db.session.commit()

        return redirect(url_for('main', user=user))
    
    if request.is_json:
        messages = Workout.query.order_by(Workout.date).all()
        workout_data = [
            {
                'user': workout.user,
                'content': workout.workout,
                'date': workout.date.strftime('%d.%m.%Y %H:%M')
            }
            for workout in messages
        ]
        return jsonify({'messages': workout_data})

    messages_ = Workout.query.order_by(Workout.date).all()
    return render_template('index.html', messages_=messages_, user=user)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

    
    
