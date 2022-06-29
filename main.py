from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite3'
app.config['SECRET_KEY'] = "students"

db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    fees = db.Column(db.Float(50))
    age = db.Column(db.String(200))
    reg_no = db.Column(db.String(10))

    def __init__(self, name, fees, age, reg_no):
        self.name = name
        self.fees = fees
        self.age = age
        self.reg_no = reg_no


@app.route('/')
def list_students():
    return render_template('student_list.html', Students=Students.query.all())


@app.route('/add', methods=['GET', 'POST'])
def addStudent():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['fees'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(request.form['name'], request.form['fees'],
                               request.form['age'], request.form['reg_no'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('list_students'))
    return render_template('add.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
