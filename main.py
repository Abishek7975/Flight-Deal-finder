#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from pprint import pprint
import datetime
from notification_manager import NotificationManager
from time import sleep
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


login_manager = LoginManager()

class RegisterForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField(label="Create Account")

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flight_deal.db"
app.config['SECRET_KEY'] = 'purvanchal'
db.init_app(app)
bootstrap = Bootstrap5(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

class User(UserMixin,db.Model):
    __tablename__ = "User_Info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String,nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String,nullable=False)

    destinations = relationship("Destination", back_populates = "user")

class Destination(db.Model):
    __tablename__ = "Destination_Info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_location: Mapped[str] = mapped_column(String, nullable=False)
    to_location: Mapped[str] = mapped_column(String, nullable=False)
    price:  Mapped[int] = mapped_column(Integer, nullable=False)
    code: Mapped[int] = mapped_column(Integer, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("User_Info.id"))

    user = relationship("User", back_populates = "destinations")







flight_search = FlightSearch()



depart_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
return_date = datetime.datetime.now().date() + datetime.timedelta(days=30*6)


with app.app_context():
    all_users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    print(all_users)

    for user in all_users:
        print(user.id)
        customer_email = user.email

        all_destinations = db.session.execute(db.select(Destination).where(Destination.user_id == user.id)).scalars()

        for destination in all_destinations:
            print(destination)
            from_city = destination.from_location
            to_city = destination.to_location

            from_city_iata = flight_search.get_iata_code(from_city)
            to_city_iata = flight_search.get_iata_code(to_city)
            lowest_price = destination.price

            flights = flight_search.find_flights(from_city_iata,to_city_iata, depart_date, return_date)
            cheapest_flight = find_cheapest_flight(flights)
            print(f"{to_city}: {cheapest_flight.price}")
            print(cheapest_flight.price)
            print(lowest_price)
            if cheapest_flight.price != 'N/A':
                if cheapest_flight.price < lowest_price:
                    notification_manager = NotificationManager(customer_email, cheapest_flight.price, from_city_iata, to_city_iata, depart_date,
                                                               return_date)
                    notification_manager.send_email()
            sleep(10)








@login_manager.user_loader
def load_user(id):
    return db.get_or_404(User,id)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password,method='pbkdf2:sha256', salt_length=8)

        new_user = User(
            username = username,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('locations'))


    return render_template('register.html', form=form)

@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = form.email.data
        password=form.password.data

        user = db.session.execute(db.select(User).where(User.email == email))
        user = user.scalar()
        if email:
            if check_password_hash(user.password,password):
                login_user(user)
                return redirect(url_for('locations'))



    return render_template('login.html',form=form)

@login_required
@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        current_city = request.form.get('current_city')
        destinations = request.form.getlist('destinations')
        prices = request.form.getlist('prices')  # Retrieve all prices as a list

        # Filter out empty destination entries and their corresponding prices
        destinations_prices = [
            (dest, price) for dest, price in zip(destinations, prices) if dest
        ]

        # Process the data (you can save it to a database, etc.)
        for (dest,price) in destinations_prices:
            new_dest = Destination(
                from_location = current_city,
                to_location = dest,
                price = price,
                code = current_user.id,
                user_id = current_user.id

            )
            db.session.add(new_dest)
            db.session.commit()
        
        return redirect(url_for('success'))

    return render_template('locations.html')


@login_required
@app.route("/success")
def success():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True)




