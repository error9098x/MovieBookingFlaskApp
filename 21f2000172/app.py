from datetime import datetime
from flask import Flask, redirect, render_template, url_for, flash
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = "secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
now = datetime.now()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=now)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Venues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=now)

    def __init__(self, name, address):
        self.name = name
        self.address = address

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    release_date = db.Column(db.DateTime, default=None)
    date_created = db.Column(db.DateTime, default=now)

    def __init__(self, name, genre, release_date):
        self.name = name
        self.genre = genre
        self.release_date = release_date

class Showtimes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.String(100), nullable=False)
    movie_name = db.Column(db.String(100), nullable=False)
    seat_avb = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    timeslot = db.Column(db.DateTime, default=None)

    def __init__(self, venue, movie_name, seat_avb, cost, timeslot):
        self.venue = venue
        self.movie_name = movie_name
        self.seat_avb = seat_avb
        self.cost = cost
        self.timeslot = timeslot

class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.String(100), nullable=False)
    movie = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    timeslot = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, venue, movie, cost, timeslot, user_id):
        self.venue = venue
        self.movie = movie
        self.cost = cost
        self.timeslot = timeslot
        self.user_id = user_id

@app.route('/admin/<int:id>')
def adminhome(id):
    global current_admin  # global variable
    current_admin = int(id)
    nameadmin = User.query.filter_by(id=id).first().name
    all_user = User.query.all()
    all_venue = Venues.query.all()
    all_movie = Movies.query.all()
    all_show = Showtimes.query.all()
    print(current_admin)
    return render_template('admin.html', nameadmin=nameadmin, users=all_user , venues=all_venue, movies=all_movie, shows=all_show)

@app.route('/admin')
def admin():
    return redirect(url_for('adminhome', id=current_admin))



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if email == 'admin@mba.com' and password == 'kalilinux' or email == 'admin2@mba.com' and password == 'ubuntu':
            return redirect(url_for('adminhome', id=user.id))
        elif user:
            return redirect(url_for('user', id=user.id))
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')
        

@app.route('/user/<int:id>')
def userhome(id):
    user = User.query.get_or_404(id)
    global current_user  # global variable
    current_user = int(id)
    all_show = Showtimes.query.all()
    all_booking = Bookings.query.all()
    all_movie = Movies.query.all()
    return render_template('user.html', user=user, shows=all_show, movies=all_movie, bookings=all_booking)


@app.route('/user')
def user():
    return redirect(url_for('userhome', id=current_user))





@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        my_data = User(name, email, password)
        db.session.add(my_data)
        db.session.commit()
        flash("User Added Successfully")
        return redirect(url_for('admin'))

@app.route('/delete_user/<int:id>', methods = ['GET', 'POST'])
def delete_user(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User Deleted Successfully")

    return redirect(url_for('admin'))

@app.route('/update_user/', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        id = request.form['id']
        my_data = User.query.get(id)
        my_data.name = request.form['name']
        my_data.password = request.form['password']
        my_data.email = request.form['email']
        db.session.commit()
        flash("User Updated Successfully")
        return redirect(url_for('admin'))
    else:
        my_data = User.query.get(id)
        return render_template('admin.html')

@app.route('/add_venue', methods=['POST'])
def add_venue():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        my_data = Venues(name, address)
        db.session.add(my_data)
        db.session.commit()
        flash("Venue Added Successfully")
        return redirect(url_for('admin'))
    
@app.route('/delete_venue/<int:id>', methods = ['GET', 'POST'])
def delete_venue(id):
    my_data = Venues.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Venue Deleted Successfully")
    return redirect(url_for('admin'))

@app.route('/update_venue/', methods=['GET', 'POST'])
def update_venue():
    if request.method == 'POST':
        id = request.form['id']
        my_data = Venues.query.get(id)
        my_data.name = request.form['name']
        my_data.address = request.form['address']
        db.session.commit()
        flash("Venue Updated Successfully")
        return redirect(url_for('admin'))
    else:
        my_data = Venues.query.get(id)
        return render_template('admin.html')
    
@app.route('/add_movie/', methods=['POST'])
def add_movie():
    if request.method == 'POST':
        name = request.form['title']
        genre = request.form['genre']
        release_date_str = request.form['release_date']
        release_date = datetime.strptime(release_date_str, '%Y-%m-%dT%H:%M')
        my_data = Movies(name, genre, release_date)
        db.session.add(my_data)
        db.session.commit()
        flash("Movie Added Successfully")
        return redirect(url_for('admin'))
    

@app.route('/delete_movie/<int:id>', methods = ['GET', 'POST'])

def delete_movie(id):
    my_data = Movies.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Movie Deleted Successfully")
    return redirect(url_for('admin'))

@app.route('/update_movie/', methods=['GET', 'POST'])

def update_movie():
    if request.method == 'POST':
        id = request.form['id']
        my_data = Movies.query.get(id)
        my_data.name = request.form['title']
        my_data.genre = request.form['genre']
        release_date_str = request.form['release_date']
        my_data.release_date = datetime.strptime(release_date_str, '%Y-%m-%dT%H:%M')
        db.session.commit()
        flash("Movie Updated Successfully")
        return redirect(url_for('admin'))
    else:
        my_data = Movies.query.get(id)
        return render_template('admin.html')
    
@app.route('/add_show/', methods=['POST'])
def add_show():
    if request.method == 'POST':
        
        venue_id = request.form['venue_id']
        movie_id = request.form['movie_id']
        seat_avb = request.form['seat_avb']
        price = request.form['price']
        start_time_str = request.form['timeslot']
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        my_data = Showtimes( venue_id, movie_id, seat_avb, price, start_time )
        db.session.add(my_data)
        db.session.commit()
        flash("Show Added Successfully")
        return redirect(url_for('admin'))

@app.route('/delete_show/<int:id>', methods = ['GET', 'POST'])
def delete_show(id):
    my_data = Showtimes.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Show Deleted Successfully")
    return redirect(url_for('admin'))


@app.route('/update_show/', methods=['GET', 'POST'])
def update_show():
    
    if request.method == 'POST':
        id = request.args['id']
        my_data = Showtimes.query.get(id)
        my_data.movie_name = request.form['movie_id']
        my_data.venue = request.form['venue_id']
        my_data.seat_avb = request.form['seat_avb']
        my_data.cost = request.form['price']
        start_time_str = request.form['timeslot']
        my_data.timeslot = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        db.session.commit()
        flash("Show Updated Successfully")
        return redirect(url_for('admin'))
    else:
        my_data = Showtimes.query.get(id)
        return render_template('admin.html')

@app.route('/buy_tickets', methods=['POST'])
def buy_tickets():
    seats = int(request.form['seat_avb'])
   
    if request.method == 'POST' and seats > 0 :
        id = request.args['id']
        venue = str(request.args['venue_id'])
        movie = str(request.args['movie_name'])
        cost = int(request.args['cost'])
        timeslot_str = str(request.args['timeslot'])
        timeslot = datetime.strptime(timeslot_str, '%Y-%m-%d %H:%M:%S')        
        user_id = int(request.form['user_id'])
        my_data = Bookings(venue, movie, cost, timeslot, user_id)
        db.session.add(my_data)
        my_data = Showtimes.query.get(id)
        my_data.seat_avb -=1
        #dynamic pricing
        if(my_data.seat_avb <=50 and my_data.seat_avb > 20):
            my_data.cost = my_data.cost + my_data.cost*0.2
        elif(my_data.seat_avb <=20 and my_data.seat_avb > 0):
            my_data.cost = my_data.cost + my_data.cost*0.5
        db.session.commit()
        flash("Ticket Booked Successfully")
        return redirect(url_for('user'))
    else:
        id = request.args['id']
        flash('Sorry, there are no more seats available for this show.')
        return redirect(url_for('user'))

if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')