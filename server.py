from flask import Flask, redirect, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, SelectField, StringField, FloatField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)

# CONNECT TO DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    Integer: Callable
    String: Callable
    Boolean: Callable


db = MySQLAlchemy(app)


# CONFIGURE TABLES
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    map_url = db.Column(db.String, unique=True, nullable=False)
    img_url = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, unique=True, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String, nullable=False)
    coffee_price = db.Column(db.String, nullable=False)


# db.create_all()


# WTFORM
class NewCafeForm(FlaskForm):
    style = {'class': 'ourClasses', 'style': 'margin: 1%; font-family: "DM Serif Display", serif; font-weight: 400;'}
    name = StringField("Name of the Cafe", validators=[DataRequired()], render_kw=style)
    map_url = StringField("Map URL", validators=[DataRequired(), URL()], render_kw=style)
    img_url = StringField("Image URL", validators=[DataRequired(), URL()], render_kw=style)
    location = StringField("Location (i.e. Peckham)", validators=[DataRequired()], render_kw=style)
    has_sockets = SelectField("Has Sockets?", validators=[DataRequired()], choices=["✔", "✖"], render_kw=style)
    has_toilet = SelectField("Has Toilet?", validators=[DataRequired()], choices=["✔", "✖"], render_kw=style)
    has_wifi = SelectField("Has Wifi?", validators=[DataRequired()], choices=["✔", "✖"], render_kw=style)
    can_take_calls = SelectField("Can it take calls?", validators=[DataRequired()], choices=["✔", "✖"], render_kw=style)
    seats = SelectField("Number of Seats", validators=[DataRequired()], choices=["0-10", "10-20", "20-30",
                                                                                 "30-40", "40-50", "50+"], render_kw=style)
    coffee_price = FloatField("Coffee Prize in € (i.e. 2.50)", validators=[DataRequired()], render_kw=style)
    submit = SubmitField("SUBMIT", render_kw=style)


@app.route("/")
def home():
    all_cafes = Cafe.query.all()
    return render_template("index.html", all_cafes=all_cafes)


@app.route("/show-cafe")
def show_cafe():
    cafe_id = request.args.get("id")
    the_cafe = Cafe.query.filter_by(id=cafe_id).first()
    return render_template("onecafe.html", cafe=the_cafe)


@app.route("/delete")
def delete_cafe():
    cafe_id = request.args.get("id")
    the_cafe = Cafe.query.filter_by(id=cafe_id).first()
    db.session.delete(the_cafe)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["POST", "GET"])
def add():
    form = NewCafeForm()
    if form.validate_on_submit():
        fun = lambda x: True if x == "✔" else False
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=fun(form.has_sockets.data),
            has_toilet=fun(form.has_toilet.data),
            has_wifi=fun(form.has_wifi.data),
            can_take_calls=fun(form.can_take_calls.data),
            seats=form.seats.data,
            coffee_price=f"€{form.coffee_price.data}"
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("addcafe.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
