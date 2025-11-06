from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aaronica@localhost:5432/aaron'
db=SQLAlchemy(app)

class User23(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)   
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/',methods=['POST','GET'])
def index():#returns the text within the index
    if request.method=='POST':
       content=request.form['one']
       new_user=User23(name=content)    
       try:
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/')
       except:
                    return 'There was an issue adding your task'
    else:
        tasks=User23.query.order_by(User23.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=User23.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=User23.query.get_or_404(id)
    
    if request.method=='POST':
       task.name= request.form['one']
       try:
                db.session.commit() 
                return redirect('/')
       except:
                return "Was unsuccessful"
    else:
        return render_template('up.html',task=task)
    
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()      # creates the table if it does not exist
    app.run(debug=True)