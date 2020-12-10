from flask import Flask, render_template, redirect, request, make_response, jsonify, Blueprint, send_file
from flask_login import LoginManager
import json
import requests
from datetime import date

from fpdf import FPDF

from data import db_session, trips, users, loginform, registerform, addtrip, baseform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'project1'
login_manager = LoginManager()
login_manager.init_app(app)

blueprint = Blueprint('products_api', __name__, template_folder='templates')


@app.route('/cookie_drop')
def cookie_drop():
    res = make_response("Вы съели печенье :-(")
    res.set_cookie("user_id", str(0), max_age=0)
    return res


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


def main():
    pass
    # db_session.global_init("db/Buisness_trips.sqlite.sqlite")
    # session = db_session.create_session()
    #
    # product = products.Product()
    # product.seller_id = 1
    # product.seller = "Scott"
    # product.title = "first product"
    # product.number = 15
    # product.description = "description"
    # product.price = "12"
    # product.product_type = "Телефон"
    # product.image = "/static/img/Nope.png"
    # product.link = "/product_link/1"
    # product.del_link = "/del_product/1"
    # product.order_link = "/order_link/1"
    # session.add(product)
    #
    # user1 = users.User()
    # user1.name = "Scott"
    # user1.email = "scott_chief@mars.org"
    # user1.hashed_password = 123
    # session.add(user1)
    #
    # session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerform.RegisterForm()
    db_session.global_init("db/Buisness_trips.sqlite")
    session = db_session.create_session()
    if form.validate_on_submit():
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html',
                                   emailmassage="Этот email уже используется",
                                   form=form)
        if not form.password1.data == form.password2.data:
            return render_template('register.html',
                                   passwordmassage="Пароли не совпадают",
                                   form=form)
        user1 = users.User()

        q = -1
        for i in session.query(users.User).all():
            q = i
        user1.id = q.id + 1
        user1.secondname = form.secondname.data
        user1.name = form.name.data
        user1.email = form.email.data
        user1.password = form.password1.data
        user1.city = form.city.data

        session.add(user1)
        session.commit()

        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        res = make_response(redirect("/"))
        res.set_cookie("user_id", str(user.id), max_age=60 * 60)
        return res
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginform.LoginForm()
    db_session.global_init("db/Buisness_trips.sqlite")
    session = db_session.create_session()
    session.commit()

    if form.validate_on_submit():
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user:
            if user.password == form.password.data:
                res = make_response(redirect("/"))
                res.set_cookie("user_id", str(user.id), max_age=60 * 60)
                return res
            return render_template('login.html',
                                   messagepass="Неправильный пароль",
                                   form=form)
        return render_template('login.html',
                               messageemail="Неправильный email",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/log_out')
def log_out():
    res = make_response(redirect("/"))
    res.set_cookie("user_id", str(0), max_age=0)
    return res


def ExporToPDF(data, spacing=1):
    pdf = FPDF()
    pdf.set_font("Arial", size=14)
    pdf.add_page()

    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=1)
        pdf.ln(row_height * spacing)

    pdf.output('Depurt_City.pdf')



@app.route('/', methods=['GET', 'POST'])
@app.route('/add_trip', methods=['GET', 'POST'])
def add_trip():

    form = addtrip.AddTripForm()
    db_session.global_init("db/Buisness_trips.sqlite")
    session = db_session.create_session()

    if form.validate_on_submit():
        trip = trips.Trip()

        datee = form.departure_time_city.data - date.today()
        if datee.days < 14:
            return render_template('addtrip.html', messagedate="Слишком рано, измените дату", form=form)

        datee = form.departure_time_home.data - form.departure_time_city.data
        if datee.days < 0:
            return render_template('addtrip.html', messageduration="Продолжительность поездки введена неверно", form=form)

        if request.cookies.get("user_id", 0):
            trip.traveler_id = request.cookies.get("user_id", 0)
            trip.traveler = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
            trip.city_from = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().city

        else:
            trip.city_from = form.city_from.data
        print(trip.city_from)
        trip.city_where = form.city_where.data
        trip.description = form.description.data
        trip.departure_time_city = form.departure_time_city.data
        trip.departure_time_home = form.departure_time_home.data

        URL_CITYES = f"https://www.travelpayouts.com/widgets_suggest_params?q=Из%20{trip.city_from}%20в%20{form.city_where.data}"
        response = requests.request("GET", URL_CITYES)
        todos = json.loads(response.text)
        if todos:
            data = [['City of depurter', trip.city_from ],
                    ['Destinatioin city',trip.city_where],
                    ['Flight price', str(trip.flight_price)],
                    ['Time in dep city ', str(trip.departure_time_city)],
                    ['Flight company dep', str(trip.flight_company)],
                    ['Flight company destin', 'Член'],
                    ['Hostel', str(trip.hostel)],
                    ['Hostel price', str(trip.hostel_price)]]
            ExporToPDF(data, spacing=8)
            print(trip.city_from)
            print(todos['destination']['iata'])
            print(trip.flight_price)
        else:
            return render_template('addtrip.html', messagecity="Название одного из городов введено неверно", form=form)


        URL_FLIGHT = 'http://engine.hotellook.com/api/v2/cache.json'
        querystring = {"location": todos['destination']['iata'],
                       "checkIn": str(trip.departure_time_city),
                       "checkOut": str(trip.departure_time_home),
                       "limit": "40",
                       "currency": "RUB",
                       "adults": "1"
                       }
        response = requests.request("GET", URL_FLIGHT, params=querystring)
        todos1 = json.loads(response.text)
        hostel = ["notname", 0.1, 0.1]
        max = -1
        for i in todos1:
            if max < int(i["priceFrom"]) < 7000:
                max = int(i["priceFrom"])
                hostel[0] = i["hotelName"]
                hostel[1] = i["location"]["geo"]["lon"]
                hostel[2] = i["location"]["geo"]["lat"]
        if max == -1:
            if request.cookies.get("user_id", 0):
                username = session.query(users.User).filter(
                    users.User.id == request.cookies.get("user_id", 0)).first().name
                username += ' ' + session.query(users.User).filter(
                    users.User.id == request.cookies.get("user_id", 0)).first().secondname
                usercity = session.query(users.User).filter(
                    users.User.id == request.cookies.get("user_id", 0)).first().city
                return render_template('addtrip.html', title='Добавить поездку', username=username, usercity=usercity,
                                       messagenotcomplite="Отели не найдены, повторите попытку", form=form)
            return render_template('addtrip.html', title='Добавить поездку', messagenotcomplite="Отели не найдены, повторите попытку",
                                   form=form)
        trip.hostel = hostel[0]
        trip.hostel_price = max
        trip.hostel_coordx = hostel[1]
        trip.hostel_coordy = hostel[2]

        return send_file('Depurt_City.pdf', attachment_filename='Depurt_City.pdf')



        URL_FLIGHT = 'http://min-prices.aviasales.ru/calendar_preload'
        querystring = {"origin": todos['origin']['iata'],
                       "destination": todos['destination']['iata'],
                       "depart_date": str(trip.departure_time_city),
                       "one_way": "true",
                       }
        response = requests.request("GET", URL_FLIGHT, params=querystring)
        todos2 = json.loads(response.text)
        company = '0'
        price = 9999999
        datetime_flight = 0
        for i in todos2["best_prices"]:
            if i["gate"] == "Aeroflot":
                if i['value'] < price:
                    company = "Aeroflot"
                    price = int(i["value"])
                    datetime_flight = i['found_at']
        if company == '0':
            for i in todos2["best_prices"]:
                    if i['value'] < price:
                        company = i["gate"]
                        price = int(i["value"])
                        datetime_flight = i['found_at']
        trip.flight_company1 = company
        trip.flight_price1 = price
        trip.flight_time1 = datetime_flight

        URL_FLIGHT = 'http://min-prices.aviasales.ru/calendar_preload'
        querystring = {"origin": todos['destination']['iata'],
                       "destination": todos['origin']['iata'],
                       "depart_date": str(trip.departure_time_home),
                       "one_way": "true",
                       }
        response = requests.request("GET", URL_FLIGHT, params=querystring)
        todos2 = json.loads(response.text)
        print(todos2)
        company = '0'
        price = 9999999
        datetime_flight = 0
        for i in todos2["best_prices"]:
            if i["gate"] == "Aeroflot":
                if i['value'] < price:
                    company = "Aeroflot"
                    price = int(i["value"])
                    datetime_flight = i['found_at']
        if company == '0':
            for i in todos2["best_prices"]:
                    if i['value'] < price:
                        company = i["gate"]
                        price = int(i["value"])
                        datetime_flight = i['found_at']
        trip.flight_company2 = company
        trip.flight_price2 = price
        trip.flight_time2 = datetime_flight
        print(trip.flight_company1, trip.flight_price1, trip.flight_time1)
        print(trip.flight_company2, trip.flight_price2, trip.flight_time2)
        # не работает ^
        # session.commit()
        if request.cookies.get("user_id", 0):
            username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
            username += ' ' + session.query(users.User).filter(
                users.User.id == request.cookies.get("user_id", 0)).first().secondname
            usercity = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().city
            return render_template('addtrip.html', title='Добавить поездку', username=username, usercity=usercity,
                                   messagecomplite="Форма поездки составлена", form=form)
        return render_template('addtrip.html', title='Добавить поездку', messagecomplite="Форма поездки составлена", form=form)

    if request.cookies.get("user_id", 0):
        username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
        username += ' ' + session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().secondname
        usercity = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().city
        return render_template('addtrip.html', title='Добавить поездку', username=username, usercity=usercity, form=form)
    return render_template('addtrip.html', title='Добавить поездку', form=form)


@app.route('/mytrips', methods=['GET', 'POST'])
def mytrips():
    db_session.global_init("db/Buisness_trips.sqlite")
    session = db_session.create_session()
    form = baseform.BaseForm()
    productes = session.query(trips.Trip)

    if request.method == "GET":
        productes = list(productes)

        types = []
        for i in productes:
            if i.product_type not in types:
                types.append(i.product_type)

        if request.cookies.get("user_id", 0):
            username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
            return render_template('products.html', title="АлиАкспресс", products=productes, username=username, products_types=types)
        return render_template('products.html', title="АлиАкспресс", products=productes, products_types=types)

    elif request.method == "POST":

        word = None
        if form.search.data:
            word = request.form["search"]

        product_type = request.form.get("product_type")
        if word:
            return redirect("/filter_link/" + product_type + "/" + word)
        elif product_type != "Все":
            return redirect("/filter_link/" + product_type + "/any")
        else:
            types = []
            for i in productes:
                if i.product_type not in types:
                    types.append(i.product_type)
            if request.cookies.get("user_id", 0):
                username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
                return render_template('products.html', title="АлиАкспресс", products=productes, username=username, products_types=types)
            return render_template('products.html', title="АлиАкспресс", products=productes, products_types=types)


if __name__ == '__main__':
    # main()
    # app.register_blueprint(products_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
