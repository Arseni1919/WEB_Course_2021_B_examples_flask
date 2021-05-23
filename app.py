from flask import Flask, redirect, url_for, request
from flask import render_template, jsonify
from flask import session
import mysql.connector

app = Flask(__name__)
app.secret_key = '123'


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@app.route('/users')
def users():
    query = "select * from users"
    query_result = interact_db(query=query, query_type='fetch')
    return render_template('users.html', users=query_result)


# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------------- INSERT --------------------- #
# ------------------------------------------------- #
@app.route('/insert_user', methods=['GET', 'POST'])
def insert_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # recheck
        query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (name, email, password)
        interact_db(query=query, query_type='commit')
        return redirect('/users')
    return render_template('insert_user.html', req_method=request.method)


# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------------- DELETE --------------------- #
# ------------------------------------------------- #

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    interact_db(query, query_type='commit')
    return redirect('/users')


# ------------------------------------------------- #
# ------------------------------------------------- #

# ------------------------------------------------- #
# --------------- URL PARAMETERS ------------------ #
# ------------------------------------------------- #
# @app.route('/profile/<int:user_id>')
# def profile_func(user_id):
#     return f'user ID: {user_id}'
# ------------------------------------------------- #
# @app.route('/profile/<int:user_id>')
# def profile_func(user_id):
#     return render_template('profile.html', user_id=user_id)
# ------------------------------------------------- #
# @app.route('/profile', defaults={'user_id': 15})
# @app.route('/profile/<int:user_id>')
# def profile_func(user_id):
#     return render_template('profile.html', user_id=user_id)
# ------------------------------------------------- #
# @app.route('/profile', defaults={'user_id': 777, 'email': 'example@email.com'})
# @app.route('/profile/<int:user_id>/<email>')
# def profile_func(user_id, email):
#     return render_template('profile.html', user_id=user_id, email=email)
# ------------------------------------------------- #
@app.route('/profile', defaults={'user_id': -1}, methods=["GET", "POST"])
@app.route('/profile/<int:user_id>')
def profile_func(user_id):
    if user_id == -1:
        return render_template('profile.html', fill_form=True)
    else:
        query = "SELECT * FROM users WHERE id='%s';" % user_id
        query_result = interact_db(query=query, query_type='fetch')
        if len(query_result) == 0:
            return render_template('404.html'), 404
            # return jsonify({
            #                 'success': 'False',
            #                 "data": []
            #             })
        else:
            # return render_template('profile.html', user_id=user_id, query_result=query_result)
            return jsonify({
                'success': 'True',
                'data': query_result[0],
            })


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    user_id = request.form['user_id']
    return redirect(url_for('profile_func', user_id=user_id))
# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------- MULTIPLE ROUTES ------------------ #
# ------------------------------------------------- #
@app.route('/index')
@app.route('/main')
@app.route('/home')
@app.route('/')
def index():
    # return render_template('index.html') #, name='Ariel')
    # return render_template('index.html', name=name)
    # DB
    # curr_user = ''
    return render_template('index.html',
                           hobbies=['Prog', 'Paint', "IEM", "Swim", "Sleep"],
                           degree=('B.Sc', 'M.Sc'))


# ------------------------------------------------- #
# --------------- MULTIPLE METHODS ---------------- #
# ------------------------------------------------- #
@app.route('/catalog', methods=['POST', 'PUT', 'DELETE', 'GET'])
def catalog_func():
    curr_user = {'firstname': "Ariel", 'lastname': "Perchik", 'wok': 'BGU', 'adress': 'Israel'}

    current_method = request.method
    if 'username' in session:
        user_name, last_name = session['username'], session['lastname']
    else:
        if current_method == 'GET':
            if 'username' in request.args:
                user_name = request.args['username']
                last_name = request.args['lastname']
            else:
                user_name, last_name = '', ''
        elif current_method == 'POST':
            if 'username' in request.form:
                user_name = request.form['username']
                last_name = request.form['lastname']
            else:
                user_name, last_name = '', ''
        else:
            user_name, last_name = '', ''
        session['username'] = ''
        session['lastname'] = ''
    return render_template('catalog.html',
                           curr_user=curr_user,
                           user_name=user_name,
                           last_name=last_name,
                           current_method=current_method)


@app.route('/customers', methods=['GET', 'POST', 'DELETE', "PUT"])
def hello_cart():
    # do something
    customer_registrated = False
    if customer_registrated:

        return redirect(url_for('index'))
    else:
        return 'You need to LOGIN'


@app.route('/about')
def hello_about():
    # do something
    return render_template('about.html')


@app.route('/log_out')
def log_out():
    session['username'] = ''
    session['lastname'] = ''
    return redirect(url_for('index'))


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    if request.method == 'GET':
        return render_template('log_in.html')
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['lastname'] = request.form['lastname']
    return redirect(url_for('index'))


@app.route('/friends')
def hello_friends():
    # do something
    curr_user = {'firstname': "Ariel", 'lastname': "Perchik", 'wok': 'BGU', 'adress': 'Israel'}
    return render_template('friends.html',
                           curr_user=curr_user,
                           hobbies=['Prog', 'Paint', "IEM", "Swim", "Sleep"],
                           degree=('B.Sc', 'M.Sc')
                           )


@app.route('/menu', methods=['GET'])
def hello_menu():
    return 'Welcome to the MENU page'


if __name__ == '__main__':
    app.run(debug=True)
