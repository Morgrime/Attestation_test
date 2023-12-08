from flask import *
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import *

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'journeys.db')
app = Flask(__name__)
app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)

class Journey(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    destination = db.Column(db.String(30))
    date = db.Column(db.Date)
    budget = db.Column(db.Integer)
    pref_services = db.Column(db.String(100))

    def __init__(self, destination, date, budget, pref_services):
        self.destination = destination
        self.date = date
        self.budget = budget
        self.pref_services = pref_services

with app.app_context():
    db.create_all()
    # test_journey = Journey('Canada', date(2023, 8, 7), 60000, 'Hotel, bar, tour')
    # db.session.add(test_journey)
    # db.session.commit()
    journeys = Journey.query.all()
    # for jour in journey:
    #     print(jour.destination, jour.date, jour.budget, jour.pref_services, sep='\n')


@app.route('/')
def journey():
    journeys = Journey.query.all()
    return render_template('journey.html', journeys=journeys)    

@app.route('/add-journey', methods=['POST'])
def add_journey():
    destination = request.form['destination']    
    date_str = request.form['date']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    budget = request.form['budget']
    pref_services = request.form['pref_services']

    new_journey = Journey(destination, date, budget, pref_services)
    db.session.add(new_journey)
    db.session.commit()

    return redirect(url_for('journey', refresh='true'))


if __name__ == '__main__':
    app.run()