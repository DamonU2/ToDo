from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create table of todo list items in database
class To_Do(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

# Create table of todo item steps in database
class steps(db.Model):
   id = db.Column(db.Integer)
   step_id = db.Column(db.Integer, primary_key = True)
   text = db.Column(db.String(200))
   complete = db.Column(db.Boolean)

@app.route('/')
def index():
    # Query ToDo table for complete and incomplete items
    incomplete = To_Do.query.filter_by(complete=False).all()
    complete = To_Do.query.filter_by(complete=True).all()
    # Query step table for complete and incomplete steps
    inc_step = steps.query.filter_by(complete=False).all()
    com_step = steps.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete=incomplete, complete=complete, inc_step=inc_step, com_step=com_step)

@app.route('/add', methods=['POST'])
def add():
    # Get text from todoitem input and add it to To_Do table
    todo = To_Do(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_step/<id>', methods=['POST'])
def add_step(id):
    # Get text from todotask input and add it to step table
    step = steps(id=id, text=request.form['todostep'], complete=False)
    db.session.add(step)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    # Find task by id and set complete to True
    todo = To_Do.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete_step/<id>')
def complete_step(id):
    # Find task by id and set complete to True
    step = steps.query.filter_by(step_id=int(id)).first()
    step.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_step/<id>')
def delete_step(id):
    # Find task by id and set complete to True
    step = steps.query.filter_by(step_id=int(id)).first()
    db.session.delete(step)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/uncheck/<id>')
def uncheck(id):
    # Find task by id and set complete back to false
    todo = To_Do.query.filter_by(id=int(id)).first()
    todo.complete = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    # Find task by id and delete it from table
    todo = To_Do.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)
