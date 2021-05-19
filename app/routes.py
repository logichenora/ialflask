from flask import render_template, jsonify, request, flash, redirect, url_for, abort, make_response
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from app.models import User, Region
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Bubbolo'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('login.html', title='Home', user=None)


@app.route('/login', methods=['POST'])
def dologin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    username = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=username).first()

    if user is None or not check_password_hash(user.password_hash, password):
        flash('Invalid username or password')
        return redirect(url_for('login'))
    login_user(user, remember=True)

    return render_template('backoffice.html', title='Welcome', user=username)


@app.route('/backoffice', methods=['GET'])
@login_required
def backoffice():
    return render_template('backoffice.html', title='Welcome', user=current_user.email)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    user = request.form.get('email')
    psw = request.form.get('password')
    psw_check = request.form.get('password2')
    if not user:
        return render_template('register.html')
    else:
        u = User.query.filter_by(email=user).first()
        if u:
            flash('User Already Exist')
            return redirect(url_for('register'))
        elif psw_check == psw:
            psw_hash = generate_password_hash(psw)
            u = User(email=user, password_hash=psw_hash)
            db.session.add(u)
            db.session.commit()
            return jsonify("User Added:" + user)
    return jsonify("Password Mismatch")

@app.route('/region', methods=['GET'])
@login_required
def region():
    return render_template('region.html', title='Welcome', user=current_user.email)

@app.route('/maps', methods=['GET'])
def maps():
    if current_user.is_authenticated:
        return render_template('maps.html', title='Maps', user=current_user.email)
    return render_template('maps.html', title='Maps', user=None)

@app.route('/api/region', methods=['POST'])
@login_required
def create_region():
    # get_regions = Region.query.all()
    if not request.form['name']:
        abort(400)
    name = request.form['name']
    color = request.form['color']
    if not color:
        color = 'white'
    region = Region(name=name, color=color)
    db.session.add(region)
    db.session.commit()
    regions = Region.query.all()
    return jsonify({"regions": [region.dto() for region in regions]}, 201)


@app.route('/api/region', methods=['GET'])
@login_required
def read_region():
    if 'id' in request.args:
        id = int(request.args['id'])
        regions = Region.query.get(id)
        if regions:
            return jsonify({"regions": [regions.dto()]}, 201)
        else:
            return jsonify({"regions": [{}]}, 404)
    else:
        regions = Region.query.all()
    return jsonify({"regions": [region.dto() for region in regions]}, 201)


@app.route('/api/region/<int:id>', methods=['DELETE'])
@login_required
def delete_region(id):
    region = Region.query.get(id)
    if region:
        db.session.delete(region)
        db.session.commit()
    else:
        abort(404)
    regions = Region.query.all()
    return jsonify({"regions": [region.dto() for region in regions]}, 201)


@app.route('/api/region/<int:id>', methods=['PUT'])
@login_required
def update_region(id):
    region = Region.query.get(id)
    if region:
        region.name = request.form['name']
        region.color = request.form['color']
        db.session.commit()
    else:
        abort(404)
    regions = Region.query.all()
    return jsonify({"regions": [region.dto() for region in regions]}, 201)
