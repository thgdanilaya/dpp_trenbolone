from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import psycopg2
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


class MyForm(FlaskForm):
    host = StringField('Host')
    database = StringField('Database')
    user = StringField('User')
    password = StringField('Password')
    port = StringField('Port')
    submit = SubmitField('Отправить')


def connect_to_db(host, database, user, password, port):
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print("Успешное подключение к базе данных")
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print("Ошибка при подключении к базе данных", error)
        return None


def measure_query_performance(query, iterations, db_params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    total_time = 0
    for _ in range(iterations):
        start_time = time.time()
        cursor.execute(query)
        end_time = time.time()
        total_time += end_time - start_time

    cursor.close()
    conn.close()

    average_time = total_time / iterations
    return average_time, iterations


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        host = form.host.data
        database = form.database.data
        user = form.user.data
        password = form.password.data
        port = form.port.data
        db_params = {
            'host': host,
            'database': database,
            'user': user,
            'password': password,
            'port': port
        }
        query = "SELECT * FROM courier_actions"
        iterations_list = [10, 100, 1000]
        average_times = []
        for iterations in iterations_list:
            average_time, _ = measure_query_performance(query, iterations, db_params)
            average_times.append(average_time)
        cms = ','.join([str(i) for i in iterations_list])
        cms2 = ','.join([str(i) for i in average_times])
        print(cms, cms2)
        return redirect(url_for('chart', average_times=cms, iterations=cms2))
    return render_template('index.html', form=form)


@app.route('/chart')
def chart():
    params = request.args
    average_times = [int(i) for i in params.get('average_times').split(",")]
    iterations = [float(i) for i in params.get('iterations').split(",")]
    print(average_times, iterations)
    return render_template('chart.html', average_times=average_times, iterations=iterations)



if __name__ == '__main__':
    app.run(debug=True)
