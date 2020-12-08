from flask import Flask, render_template, redirect, request, make_response, jsonify, Blueprint
from flask_login import LoginManager
# Проверка gita
from data import db_session, products, users, loginform, registerform, addproductform, baseform

# проект
a = 2*2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
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
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()

    product = products.Product()
    product.seller_id = 1
    product.seller = "Scott"
    product.title = "first product"
    product.number = 15
    product.description = "description"
    product.price = "12"
    product.product_type = "Телефон"
    product.image = "/static/img/Nope.png"
    product.link = "/product_link/1"
    product.del_link = "/del_product/1"
    product.order_link = "/order_link/1"
    session.add(product)

    user1 = users.User()
    user1.name = "Scott"
    user1.email = "scott_chief@mars.org"
    user1.hashed_password = 123
    session.add(user1)

    session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerform.RegisterForm()
    db_session.global_init("db/online_shop.sqlite")
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
        user1.name = form.name.data
        user1.email = form.email.data
        user1.hashed_password = form.password1.data

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
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    session.commit()

    if form.validate_on_submit():
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user:
            if user.hashed_password == form.password.data:
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


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = addproductform.AddProductForm()
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()

    if form.validate_on_submit():
        if not form.number.data.isdigit():
            return render_template('addproduct.html',
                                   numbermassage="Неверно введено количество",
                                   form=form)
        if not form.price.data.isdigit():
            return render_template('addproduct.html',
                                   pricemassage="Неверно введена цена",
                                   form=form)

        product = products.Product()
        product.seller_id = request.cookies.get("user_id", 0)
        product.seller = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
        product.title = form.title.data
        product.number = form.number.data
        product.price = form.price.data
        product.description = form.description.data
        product.product_type = form.product_type.data
        product.image = "/static/img/Nope.png"

        idd = session.query(products.Product)
        if idd.count() > 0:
            product.link = "/product_link/" + str(int(idd[-1].id) + 1)
            product.del_link = "/del_product/" + str(int(idd[-1].id) + 1)
            product.order_link = "/order_link/" + str(int(idd[-1].id) + 1)
        else:
            product.link = "/product_link/1"
            product.del_link = "/del_product/1"
            product.order_link = "/order_link/1"
        session.add(product)
        session.commit()

        return redirect("/")
    username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
    return render_template('addproduct.html', title='Добавить товар', username=username, form=form)


@app.route('/product_link/<product_id>', methods=['GET', 'POST'])
def product_link(product_id="product_id"):
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    form = baseform.BaseForm()

    product = session.query(products.Product).filter(products.Product.id == product_id).first()
    if request.method == "GET":
        productes = session.query(products.Product)
        types = []
        for i in productes:
            if i.product_type not in types:
                types.append(i.product_type)

        if request.cookies.get("user_id", 0):
            username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
            userid = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().id
            return render_template('product.html', title=product.title, product=product, username=username, userid=userid, products_types=types)
        return render_template('product.html', title=product.title, product=product, products_types=types)

    elif request.method == "POST":
        product_type = request.form.get("product_type")
        word = None
        if form.search.data:
            word = request.form["search"]

        if word:
            return redirect("/filter_link/" + product_type + "/" + word)
        else:
            return redirect("/")


@app.route('/del_product/<id>', methods=['GET', 'POST'])
def del_product(id="id"):
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    product = session.query(products.Product).filter(products.Product.id == id).first()
    if product:
        session.delete(product)
        session.commit()
    return redirect("/")


@app.route('/order_link/<id>', methods=['GET', 'POST'])
def order_link(id="id"):
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    product = session.query(products.Product).filter(products.Product.id == id).first()
    if product:
        product.number -= 1
        session.commit()
    return redirect("/")


@app.route('/api_products', methods=['GET', 'POST'])
def api_products():
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    productes = session.query(products.Product)
    print(jsonify(
                {
                    'products':
                        [item.to_dict(only=('title', 'number', 'price', 'seller_id')) for item in productes]
                }
            ))
    return jsonify(
                {
                    'products':
                        [item.to_dict(only=('title', 'number', 'price', 'seller_id')) for item in productes]
                }
            )


@app.route('/filter_link/<product_type>/<word>', methods=['GET', 'POST'])
def filter_link(product_type="product_type", word="word"):
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    form = baseform.BaseForm()

    productes = session.query(products.Product)
    if request.method == "GET":

        arr = []
        if product_type != "Все" and word != "any":
            for item in productes:
                if product_type == item.product_type and word in item.title:
                    arr.append(item)
        elif product_type != "Все":
            for item in productes:
                if product_type == item.product_type:
                    arr.append(item)
        elif word != "any":
            for item in productes:
                if word in item.title and item not in arr:
                    arr.append(item)

        types = []
        for i in productes:
            if i.product_type not in types:
                types.append(i.product_type)

        if request.cookies.get("user_id", 0):
            username = session.query(users.User).filter(users.User.id == request.cookies.get("user_id", 0)).first().name
            return render_template('products.html', form=form, title="АлиАкспресс", products=arr, username=username, products_types=types)
        return render_template('products.html', form=form, title="АлиАкспресс", products=arr, products_types=types)

    elif request.method == "POST":

        product_type = request.form.get("product_type")
        word = None
        if form.search.data:
            word = request.form["search"]

        if word:
            return redirect("/filter_link/" + product_type + "/" + word)
        elif product_type != "Все":
            return redirect("/filter_link/" + product_type + "/any")
        else:
            return redirect("/")


@app.route('/', methods=['GET', 'POST'])
@app.route('/main_link', methods=['GET', 'POST'])
def main_link():
    db_session.global_init("db/online_shop.sqlite")
    session = db_session.create_session()
    form = baseform.BaseForm()
    productes = session.query(products.Product)

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
